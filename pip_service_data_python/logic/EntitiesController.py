# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.commands import ICommandable, CommandSet
from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams, DataPage, IdGenerator
from pip_services3_commons.refer import IReferenceable, Descriptor, IReferences

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesCommandSet import EntitiesCommandSet
from pip_service_data_python.logic.IEntitiesController import IEntitiesController
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence


class EntitiesController(IEntitiesController, IConfigurable, IReferenceable, ICommandable):
    __persistence: IEntitiesPersistence = None
    __command_set: EntitiesCommandSet = None

    def configure(self, config: ConfigParams):
        pass

    def set_references(self, references: IReferences):
        self.__persistence = references.get_one_required(Descriptor('pip-service-data', 'persistence', '*', '*', '1.0'))

    def get_command_set(self) -> CommandSet:
        if self.__command_set is None:
            self.__command_set = EntitiesCommandSet(self)

        return self.__command_set

    def get_entities(self, correlation_id: Optional[str], filter_params: FilterParams,
                     paging: PagingParams) -> DataPage:
        return self.__persistence.get_page_by_filter(correlation_id, filter_params, paging)

    def get_entities_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        return self.__persistence.get_one_by_id(correlation_id, entity_id)

    def get_entity_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        return self.__persistence.get_one_by_name(correlation_id, entity_name)

    def create_entity(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        entity.id = entity.id or IdGenerator.next_long()
        entity.type = entity.type or EntityTypeV1.Unknown

        return self.__persistence.create(correlation_id, entity)

    def update_entity(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        entity.type = entity.type or EntityTypeV1.Unknown

        return self.__persistence.update(correlation_id, entity)

    def delete_entity_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        return self.__persistence.delete_by_id(correlation_id, entity_id)
