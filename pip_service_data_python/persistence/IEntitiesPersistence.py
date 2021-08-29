# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from pip_services3_commons.data import FilterParams, PagingParams, DataPage

from pip_service_data_python.data.EntityV1 import EntityV1


class IEntitiesPersistence(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def get_page_by_filter(self, correlation_id: Optional[str], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        pass

    def get_one_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        pass

    def get_one_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        pass

    def create(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        pass

    def update(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        pass

    def delete_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        pass
