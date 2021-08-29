# -*- coding: utf-8 -*-
from typing import Any, Optional

from pip_services3_commons.data import FilterParams, DataPage, PagingParams
from pip_services3_mysql.persistence.IdentifiableMySqlPersistence import IdentifiableMySqlPersistence

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence


class EntitiesMySqlPersistence(IdentifiableMySqlPersistence, IEntitiesPersistence):

    def __init__(self):
        super().__init__('entities')

        self._max_page_size = 1000

    def _define_schema(self):
        self._clear_schema()
        self._ensure_schema("CREATE TABLE entities (id VARCHAR(32), site_id VARCHAR(32), type VARCHAR(15), "
                            "name VARCHAR(50), content VARCHAR(150))")
        self._ensure_index("entities_site_id", {'site_id': 1})

    def __compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()

        filters = []

        id = filter_params.get_as_nullable_string('id')
        if id is not None:
            filters.append("id='" + id + "'")

        site_id = filter_params.get_as_nullable_string('site_id')
        if site_id is not None:
            filters.append("site_id='" + site_id + "'")

        temp_ids = filter_params.get_as_nullable_string('ids')
        if temp_ids is not None:
            ids = temp_ids.split(',')
            filters.append("id IN ('" + "','".join(ids) + "')")

        name = filter_params.get_as_nullable_string('name')
        if name is not None:
            filters.append("name='" + name + "'")

        temp_names = filter_params.get_as_nullable_string('names')
        if temp_names is not None:
            names = temp_names.split(',')
            filters.append("name IN ('" + "','".join(names) + "')")

        return None if len(filters) < 1 else " AND ".join(filters)

    def get_page_by_filter(self, correlation_id: Optional[str], filter: Any, paging: PagingParams,
                           sort: Any = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, 'id', None)

    def get_one_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        query = "SELECT * FROM " + self._quote_identifier(self._table_name) + " WHERE name=%s"

        params = [entity_name]
        result = self._request(query, params)

        items = result['items']
        item = items[0] if items is not None and len(items) > 0 else None

        if item is None:
            self._logger.trace(correlation_id, "Nothing found from %s with name = %s", self._table_name, entity_name)
        else:
            self._logger.trace(correlation_id, "Retrieved from %s with name = %s", self._table_name, entity_name)

        item = self._convert_to_public(item)
        return item
