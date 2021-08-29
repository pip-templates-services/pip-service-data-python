# -*- coding: utf-8 -*-
from typing import Optional, Any

from pip_services3_commons.data import FilterParams, PagingParams, DataPage
from pip_services3_mongodb.persistence import IdentifiableMongoDbPersistence

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence


class EntitiesMongoDbPersistence(IdentifiableMongoDbPersistence, IEntitiesPersistence):

    def __init__(self):
        super().__init__('entities')

        self._max_page_size = 1000

    def __compose_filter(self, filter_params: FilterParams):
        filter_params = filter_params or FilterParams()

        filters = []

        id = filter_params.get_as_nullable_string('id')
        if id is not None:
            filters.append({'_id': id})

        site_id = filter_params.get_as_nullable_string('site_id')
        if site_id is not None:
            filters.append({'site_id': site_id})

        name = filter_params.get_as_nullable_string('name')
        if name is not None:
            filters.append({'name': name})

        temp_names = filter_params.get_as_nullable_string('names')
        if temp_names is not None:
            names = temp_names.split(',')
            filters.append({'name': {'$in': names}})

        return None if len(filters) < 1 else {'$and': filters}

    def get_page_by_filter(self, correlation_id: Optional[str], filter: Any, paging: PagingParams,
                           sort: Any = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, None, None)

    def get_one_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        criteria = {
            'name': entity_name
        }
        item = self._collection.find_one(criteria)

        if item is None:
            self._logger.trace(correlation_id, "Cannot find entity with name=%s", entity_name)
        else:
            self._logger.trace(correlation_id, "Found entity with name=%s", entity_name)

        item = self._convert_to_public(item)
        return item
