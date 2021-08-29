# -*- coding: utf-8 -*-
from typing import Any

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.refer import References, Descriptor
from pip_services3_grpc.test.TestCommandableGrpcClient import TestCommandableGrpcClient

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from pip_service_data_python.services.version1.EntitiesCommandableGrpcServiceV1 import EntitiesCommandableGrpcServiceV1

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


class TestEntitiesCommandableGrpcServiceV1:
    persistence: EntitiesMemoryPersistence
    controller: EntitiesController
    service: EntitiesCommandableGrpcServiceV1
    client: TestCommandableGrpcClient

    @classmethod
    def setup_class(cls):
        cls.persistence = EntitiesMemoryPersistence()
        cls.persistence.configure(ConfigParams())

        cls.controller = EntitiesController()
        cls.controller.configure(ConfigParams())

        cls.service = EntitiesCommandableGrpcServiceV1()
        cls.service.configure(grpc_config)

        cls.client = TestCommandableGrpcClient('v1.entities')
        cls.client.configure(grpc_config)

        references = References.from_tuples(
            Descriptor('pip-service-data', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('pip-service-data', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('pip-service-data', 'service', 'grpc', 'default', '1.0'), cls.service
        )

        cls.controller.set_references(references)
        cls.service.set_references(references)

        cls.persistence.open(None)
        cls.service.open(None)
        cls.client.open(None)

    @classmethod
    def teardown_class(cls):
        cls.persistence.close(None)
        cls.service.close(None)
        cls.client.close(None)

    def test_crud_operations(self):
        # Create the first entity
        entity = self.client.call_command('create_entity', None, {'entity': ENTITY1})

        entity = self._from_plain_to_entity(entity)

        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        entity = self.client.call_command('create_entity', None, {'entity': ENTITY2})

        entity = self._from_plain_to_entity(entity)

        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Get all entities
        page = self.client.call_command('get_entities',
                                        None,
                                        {
                                            'filter': FilterParams(),
                                            'paging': PagingParams()
                                        })

        assert page is not None
        assert len(page.data) == 2

        # Update the entity
        entity1 = self._from_plain_to_entity(page.data[0])
        entity1.name = 'ABC'

        entity = self.client.call_command('update_entity',
                                          None,
                                          {
                                              'entity': entity1
                                          })

        assert entity is not None
        assert entity.id == entity1.id
        assert 'ABC' == entity.name

        # Get entity by name
        entity = self.client.call_command('get_entity_by_name',
                                          None,
                                          {
                                              'entity_name': entity1.name
                                          })

        entity = self._from_plain_to_entity(entity)

        assert entity is not None
        assert entity1.id == entity.id

        # Delete the entity
        entity = self.client.call_command('delete_entity_by_id',
                                          None,
                                          {
                                              'entity_id': entity1.id
                                          })

        entity = self._from_plain_to_entity(entity)

        assert entity is not None
        assert entity.id == entity1.id

        # Try to get deleted entity
        entity = self.client.call_command('get_entity_by_id',
                                          None,
                                          {
                                              'entity_id': entity1.id
                                          })

        assert entity is None

    def _from_plain_to_entity(self, plain_obj: Any) -> EntityV1:
        entity = EntityV1(id=plain_obj.id,
                          site_id=plain_obj.site_id,
                          type=plain_obj.type,
                          name=plain_obj.name,
                          content=plain_obj.content
                          )
        return entity
