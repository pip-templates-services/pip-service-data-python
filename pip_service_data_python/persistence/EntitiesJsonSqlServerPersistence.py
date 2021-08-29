# -*- coding: utf-8 -*-
from typing import Any, Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage
from pip_services3_sqlserver.persistence.IdentifiableJsonSqlServerPersistence import \
    IdentifiableJsonSqlServerPersistence

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence


class EntitiesJsonSqlServerPersistence(IdentifiableJsonSqlServerPersistence, IEntitiesPersistence):

    def __init__(self):
        super().__init__('entities_json')

        self._max_page_size = 1000

    def _define_schema(self):
        self._clear_schema()
        self._ensure_table()
        self._ensure_schema("ALTER TABLE [entities_json] ADD [data_key] AS JSON_VALUE([data],'$.id')")
        self._ensure_index('entities_json_key', {'data_key': 1}, {'unique': True})

    def __compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()

        filters = []

        id = filter_params.get_as_nullable_string('id')
        if id is not None:
            filters.append("JSON_VALUE([data],'$.id')='" + id + "'")

        site_id = filter_params.get_as_nullable_string('site_id')
        if site_id is not None:
            filters.append("JSON_VALUE([data],'$.site_id')='" + site_id + "'")

        temp_ids = filter_params.get_as_nullable_string('ids')
        if temp_ids is not None:
            ids = temp_ids.split(',')
            filters.append("JSON_VALUE([data], '$.id') IN ('" + "','".join(ids) + "')")

        name = filter_params.get_as_nullable_string('name')
        if name is not None:
            filters.append("JSON_VALUE([data],'$.name')='" + name + "'")

        temp_names = filter_params.get_as_nullable_string('names')
        if temp_names is not None:
            names = temp_names.split(',')
            filters.append("JSON_VALUE([data], '$.name') IN ('" + "','".join(names) + "')")

        return None if len(filters) < 1 else " AND ".join(filters)

    def get_page_by_filter(self, correlation_id: Optional[str], filter: Any, paging: PagingParams,
                           sort: Any = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, 'id', None)

    def get_one_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        query = "SELECT * FROM " + self._quote_identifier(
            self._table_name) + " WHERE JSON_VALUE([data],'$.name')=?"

        params = [entity_name]

        items = self._request(query, params)

        item = None if items is None or len(items) < 1 else items[0]

        if item is None:
            self._logger.trace(correlation_id, "Nothing found from %s with name = %s", self._table_name, entity_name)
        else:
            self._logger.trace(correlation_id, "Retrieved from %s with name = %s", self._table_name, entity_name)

        item = self._convert_to_public(item)
        return item
