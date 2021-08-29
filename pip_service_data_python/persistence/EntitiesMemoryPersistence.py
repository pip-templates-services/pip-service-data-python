# -*- coding: utf-8 -*-
from typing import Optional, Any, Callable

from pip_services3_commons.data import FilterParams, PagingParams, DataPage
from pip_services3_data.persistence import IdentifiableMemoryPersistence

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence


class EntitiesMemoryPersistence(IdentifiableMemoryPersistence, IEntitiesPersistence):

    def __init__(self):
        super().__init__()

        self._max_page_size = 1000

    def __compose_filter(self, filter_params: FilterParams) -> Callable[[EntityV1], bool]:
        filter_params = filter_params or FilterParams()

        id = filter_params.get_as_nullable_string('id')
        site_id = filter_params.get_as_nullable_string('site_id')
        name = filter_params.get_as_nullable_string('name')
        names = filter_params.get_as_nullable_string('names')

        if isinstance(names, str):
            names = names.split(',')
        if not isinstance(names, list):
            names = None

        def filter_action(item: EntityV1) -> bool:
            if id is not None and item.id != id:
                return False
            if site_id is not None and item.site_id != site_id:
                return False
            if name is not None and item.name != name:
                return False
            if names is not None and item.name not in names:
                return False
            return True

        return filter_action

    def get_page_by_filter(self, correlation_id: Optional[str], filter: Any, paging: PagingParams,
                           sort: Any = None, select: Any = None) -> DataPage:
        return super().get_page_by_filter(correlation_id, self.__compose_filter(filter), paging, None, None)

    def get_one_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        filtered = list(filter(lambda item: item.name == entity_name, self._items))
        item = None if len(filtered) < 1 else filtered[0]

        if item is None:
            self._logger.trace(correlation_id, "Cannot find entity with name=%s", entity_name)
        else:
            self._logger.trace(correlation_id, "Found entity with name=%s", entity_name)

        return item
