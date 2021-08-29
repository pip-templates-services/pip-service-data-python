# -*- coding: utf-8 -*-
from pip_services3_aws.services.LambdaService import LambdaService
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import DataPage, FilterParams, PagingParams
from pip_services3_commons.refer import Descriptor, IReferences
from pip_services3_commons.validate import PagingParamsSchema, FilterParamsSchema, ObjectSchema

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.data.EntityV1Schema import EntityV1Schema
from pip_service_data_python.logic.IEntitiesController import IEntitiesController


class EntitiesLambdaServiceV1(LambdaService):
    __controller: IEntitiesController

    def __init__(self):
        super(EntitiesLambdaServiceV1, self).__init__('v1.entities')
        self._dependency_resolver.put('controller', Descriptor("pip-service-data", "controller", "default", "*", "*"))

    def set_references(self, references: IReferences):
        super().set_references(references)
        self.__controller = self._dependency_resolver.get_one_required('controller')

    def get_entities(self, params: dict) -> DataPage:
        timing = self._instrument(params.get('correlation_id'), "get_entities")
        try:
            return self.__controller.get_entities(params.get('correlation_id'),
                                                  FilterParams(params.get('filter')),
                                                  PagingParams(params.get('paging'))
                                                  )
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def get_entity_by_id(self, params: dict) -> EntityV1:
        timing = self._instrument(params.get('correlation_id'), "get_entity_by_id")
        try:
            return self.__controller.get_entities_by_id(params.get('correlation_id'),
                                                        params.get('entity_id'))
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def get_entity_by_name(self, params: dict) -> EntityV1:
        timing = self._instrument(params.get('correlation_id'), "get_entity_by_name")
        try:
            return self.__controller.get_entity_by_name(params.get('correlation_id'),
                                                        params.get('name'))
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def create_entity(self, params: dict) -> EntityV1:
        timing = self._instrument(params.get('correlation_id'), "create_entity")
        try:
            return self.__controller.create_entity(params.get('correlation_id'),
                                                   params.get('entity'))
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def update_entity(self, params: dict) -> EntityV1:
        timing = self._instrument(params.get('correlation_id'), "update_entity")
        try:
            return self.__controller.update_entity(params.get('correlation_id'),
                                                   params.get('entity'))
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def delete_entity_by_id(self, params: dict) -> EntityV1:
        timing = self._instrument(params.get('correlation_id'), "delete_entity_by_id")
        try:
            return self.__controller.delete_entity_by_id(params.get('correlation_id'),
                                                         params.get('entity_id'))
        except Exception as err:
            timing.end_failure(err)
        finally:
            timing.end_success()

    def register(self):
        self._register_action('get_entities', ObjectSchema(True)
                              .with_optional_property("filter", FilterParamsSchema())
                              .with_optional_property("paging", PagingParamsSchema()),
                              self.get_entities)

        self._register_action('get_entity_by_id', ObjectSchema(True)
                              .with_optional_property("entity_id", TypeCode.String),
                              self.get_entity_by_id)

        self._register_action('get_entity_by_name', ObjectSchema(True)
                              .with_optional_property("name", TypeCode.String),
                              self.get_entity_by_name)

        self._register_action('create_entity', ObjectSchema(True)
                              .with_required_property("entity", EntityV1Schema()),
                              self.create_entity)

        self._register_action('update_entity', ObjectSchema(True)
                              .with_required_property("entity", EntityV1Schema()),
                              self.update_entity)

        self._register_action('delete_entity_by_id', ObjectSchema(True)
                              .with_optional_property("entity_id", TypeCode.String),
                              self.delete_entity_by_id)
