# -*- coding: utf-8 -*-
from typing import Any

import grpc
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from pip_service_data_python.protos import entities_v1_pb2_grpc, entities_v1_pb2
from pip_service_data_python.services.version1.EntitiesGrpcConverterV1 import EntitiesGrpcConverterV1
from pip_service_data_python.services.version1.EntitiesGrpcServiceV1 import EntitiesGrpcServiceV1

ENTITY1 = EntityV1(id='1',
                   name='00001',
                   type=EntityTypeV1.Type1,
                   site_id='1',
                   content='ABC')

ENTITY2 = EntityV1(id='2',
                   name='00002',
                   type=EntityTypeV1.Type2,
                   site_id='1',
                   content='XYZ')

grpc_config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost",
    "connection.port", 3000
)
url = 'http://localhost:3000'


class TestEntitiesGrpcServiceV1:
    persistence: EntitiesMemoryPersistence
    controller: EntitiesController
    service: EntitiesGrpcServiceV1
    client: Any
    channel: grpc.Channel

    @classmethod
    def setup_class(cls):
        cls.persistence = EntitiesMemoryPersistence()
        cls.persistence.configure(ConfigParams())

        cls.controller = EntitiesController()
        cls.controller.configure(ConfigParams())

        cls.service = EntitiesGrpcServiceV1()
        cls.service.configure(grpc_config)

        references: References = References.from_tuples(
            Descriptor('pip-service-data', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('pip-service-data', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-service-data', 'service', 'http', 'default', '1.0'), cls.service
        )
        cls.controller.set_references(references)
        cls.service.set_references(references)

        cls.persistence.open(None)
        cls.service.open(None)

    @classmethod
    def teardown_class(cls):
        cls.service.close(None)

    def setup_method(self):
        self.channel = grpc.insecure_channel('localhost:3000')
        self.client = entities_v1_pb2_grpc.EntitiesStub(self.channel)

    def test_crud_operations(self):
        # Create the first entity
        request = entities_v1_pb2.EntityRequest(
            entity=EntitiesGrpcConverterV1.from_entity(ENTITY1))

        response = self.client.create_entity(request)
        entity = None if not response.entity.id else response.entity
        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        # Create the first entity
        request = entities_v1_pb2.EntityRequest(
            entity=EntitiesGrpcConverterV1.from_entity(ENTITY2))

        response = self.client.create_entity(request)
        entity = None if not response.entity.id else response.entity
        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Get all entities
        request = entities_v1_pb2.EntitiesPageRequest(
            paging=entities_v1_pb2.PagingParams())

        response = self.client.get_entities(request)
        page = None if not response.page.data else response.page

        assert len(page.data) == 2

        entity1 = page.data[0]

        # Update the entity
        entity1.name = 'ABC'
        request = entities_v1_pb2.EntityRequest(entity=entity1)

        response = self.client.update_entity(request)

        entity = None if not response.entity.id else response.entity

        assert entity1.id == entity.id
        assert 'ABC' == entity.name

        # Get entity by name
        request = entities_v1_pb2.EntityNameRequest(name=entity1.name)

        response = self.client.get_entity_by_name(request)
        entity = None if not response.entity.id else response.entity

        assert entity is not None
        assert entity1.id == entity.id

        # Delete the entity
        request = entities_v1_pb2.EntityIdRequest(entity_id=entity1.id)

        response = self.client.delete_entity_by_id(request)
        entity = None if not response.entity.id else response.entity

        assert entity is not None
        assert entity1.id == entity.id

        # Try to get deleted entity
        request = entities_v1_pb2.EntityIdRequest(entity_id=entity1.id)

        response = self.client.get_entity_by_id(request)
        entity = None if not response.entity.id else response.entity

        assert entity is None
