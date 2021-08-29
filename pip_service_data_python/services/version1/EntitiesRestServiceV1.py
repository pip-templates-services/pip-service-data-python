# -*- coding: utf-8 -*-
import json
import pathlib

import bottle
from pip_services3_commons.refer import Descriptor, IReferences
from pip_services3_rpc.services import RestService

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.IEntitiesController import IEntitiesController


class EntitiesRestServiceV1(RestService):
    __controller: IEntitiesController

    def __init__(self):
        super().__init__()
        self._base_route = "v1/entities"
        self._dependency_resolver.put("controller",
                                      Descriptor("pip-service-data", "controller", "default", "*", "*"))

    def set_references(self, references: IReferences):
        super().set_references(references)
        self.__controller = self._dependency_resolver.get_one_required('controller')

    def get_entities(self, ):
        correlation_id = self._get_correlation_id()
        filter = bottle.request.query.get('filter')
        paging = bottle.request.query.get('paging')

        timing = self._instrument(correlation_id, 'get_entities')
        try:
            result = self.__controller.get_entities(correlation_id, filter, paging)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def get_entity_by_id(self, id):
        correlation_id = self._get_correlation_id()

        timing = self._instrument(correlation_id, 'get_entity_by_id')
        try:
            result = self.__controller.get_entities_by_id(correlation_id, id)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def get_entity_by_name(self, name):
        correlation_id = self._get_correlation_id()

        timing = self._instrument(correlation_id, 'get_entity_by_name')
        try:
            result = self.__controller.get_entity_by_name(correlation_id, name)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def create_entity(self):
        correlation_id = self._get_correlation_id()
        data = json.loads(bottle.request.json)
        entity = EntityV1(**data)

        timing = self._instrument(correlation_id, 'create_entity')
        try:
            result = self.__controller.create_entity(correlation_id, entity)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def update_entity(self):
        correlation_id = self._get_correlation_id()
        data = json.loads(bottle.request.json)
        entity = EntityV1(**data)

        timing = self._instrument(correlation_id, 'update_entity')
        try:
            result = self.__controller.update_entity(correlation_id, entity)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def delete_entity_by_id(self, id):
        correlation_id = self._get_correlation_id()

        timing = self._instrument(correlation_id, 'delete_entity_by_id')
        try:
            result = self.__controller.delete_entity_by_id(correlation_id, id)
            return self.send_result(result)
        except Exception as err:
            timing.end_failure(err)
            return self.send_error(err)
        finally:
            timing.end_success()

    def register(self):
        self.register_route('get', '/entities', None, self.get_entities)
        self.register_route('get', '/entities/<id>', None, self.get_entity_by_id)
        self.register_route('get', '/entities/name/<name>', None, self.get_entity_by_name)
        self.register_route('post', '/entities', None, self.create_entity)
        self.register_route('put', '/entities', None, self.update_entity)
        self.register_route('delete', '/entities/<id>', None, self.delete_entity_by_id)
        self._register_open_api_spec_from_file(
            str(pathlib.Path(__file__).parent.parent.parent.joinpath('./swagger/entities_v1.yaml')))
