# -*- coding: utf-8 -*-
from grpc import ServicerContext
from pip_services3_commons.data import FilterParams
from pip_services3_commons.refer import Descriptor, IReferences
from pip_services3_grpc.protos.commandable_pb2 import InvokeRequest
from pip_services3_grpc.services.GrpcService import GrpcService

import pip_service_data_python.protos.entities_v1_pb2 as messages
from pip_service_data_python.logic.IEntitiesController import IEntitiesController
from pip_service_data_python.protos import entities_v1_pb2_grpc
from pip_service_data_python.services.version1.EntitiesGrpcConverterV1 import EntitiesGrpcConverterV1


class EntitiesGrpcServiceV1(GrpcService):
    __controller: IEntitiesController

    def __init__(self, name: str = None):
        super().__init__(name or 'entities_v1')

        self._dependency_resolver.put('controller', Descriptor("pip-service-data", "controller", "*", "*", "*"))

    def set_references(self, references: IReferences):
        super().set_references(references)
        self.__controller = self._dependency_resolver.get_one_required('controller')

    def add_servicer_to_server(self, server):
        entities_v1_pb2_grpc.add_EntitiesServicer_to_server(self, server)

    def __get_entities(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        filter = FilterParams()
        EntitiesGrpcConverterV1.set_map(filter, request.filter)
        paging = EntitiesGrpcConverterV1.to_paging_params(request.paging)

        response = messages.EntitiesPageReply()
        timing = self._instrument(correlation_id, "get_entities")

        try:
            result = self.__controller.get_entities(correlation_id, filter, paging)
            page = EntitiesGrpcConverterV1.from_entities_page(result)

            response.page.total = page.total

            for item in page.data:
                response.page.data.append(item)

        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def __get_entity_by_id(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        id = request.entity_id

        response = messages.EntityReply()
        timing = self._instrument(correlation_id, 'get_entity_by_id')

        try:
            result = self.__controller.get_entities_by_id(correlation_id, id)
            entity = EntitiesGrpcConverterV1.from_entity(result)
            EntitiesGrpcConverterV1.set_map(response.entity, entity)
        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def __get_entity_by_name(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        name = request.name

        response = messages.EntityReply()
        timing = self._instrument(correlation_id, 'get_entity_by_name')

        try:
            result = self.__controller.get_entity_by_name(correlation_id, name)
            entity = EntitiesGrpcConverterV1.from_entity(result)
            EntitiesGrpcConverterV1.set_map(response.entity, entity)
        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def __create_entity(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        entity = request.entity
        entity = EntitiesGrpcConverterV1.to_entity(entity)

        response = messages.EntityReply()
        timing = self._instrument(correlation_id, 'create_entity')

        try:
            result = self.__controller.create_entity(correlation_id, entity)
            entity = EntitiesGrpcConverterV1.from_entity(result)
            EntitiesGrpcConverterV1.set_map(response.entity, entity)
        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def __update_entity(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        entity = request.entity
        entity = EntitiesGrpcConverterV1.to_entity(entity)

        response = messages.EntityReply()
        timing = self._instrument(correlation_id, 'update_entity')

        try:
            result = self.__controller.update_entity(correlation_id, entity)
            entity = EntitiesGrpcConverterV1.from_entity(result)
            EntitiesGrpcConverterV1.set_map(response.entity, entity)
        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def __delete_entity_by_id(self, request: InvokeRequest, context: ServicerContext):
        correlation_id = request.correlation_id
        id = request.entity_id

        response = messages.EntityReply()
        timing = self._instrument(correlation_id, 'delete_entity_by_id')

        try:
            result = self.__controller.delete_entity_by_id(correlation_id, id)
            entity = EntitiesGrpcConverterV1.from_entity(result)
            EntitiesGrpcConverterV1.set_map(response.entity, entity)
        except Exception as err:
            error = EntitiesGrpcConverterV1.from_error(err)
            response.error = error
            timing.end_failure(err)
        finally:
            timing.end_success()

        return response

    def register(self):
        self._register_method(
            'get_entities',
            None,
            self.__get_entities
        )

        self._register_method(
            'get_entity_by_id',
            None,
            self.__get_entity_by_id
        )

        self._register_method(
            'get_entity_by_name',
            None,
            self.__get_entity_by_name
        )

        self._register_method(
            'create_entity',
            None,
            self.__create_entity
        )

        self._register_method(
            'update_entity',
            None,
            self.__update_entity
        )

        self._register_method(
            'delete_entity_by_id',
            None,
            self.__delete_entity_by_id
        )
