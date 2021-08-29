# -*- coding: utf-8 -*-

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.refer import References, Descriptor
from pip_services3_rpc.test.TestCommandableHttpClient import TestCommandableHttpClient

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from pip_service_data_python.services.version1.EntitiesCommandableHttpServiceV1 import EntitiesCommandableHttpServiceV1

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

http_config = ConfigParams.from_tuples(
    "connection.protocol", "http",
    "connection.host", "localhost",
    "connection.port", 3000
)


class TestEntitiesCommandableHttpServiceV1:
    persistence: EntitiesMemoryPersistence
    controller: EntitiesController
    service: EntitiesCommandableHttpServiceV1
    client: TestCommandableHttpClient

    def setup_method(self):
        self.persistence = EntitiesMemoryPersistence()
        self.persistence.configure(ConfigParams())

        self.controller = EntitiesController()
        self.controller.configure(ConfigParams())

        self.service = EntitiesCommandableHttpServiceV1()
        self.service.configure(http_config)

        self.client = TestCommandableHttpClient('v1/entities')
        self.client.configure(http_config)

        references = References.from_tuples(
            Descriptor('pip-service-data', 'persistence', 'memory', 'default', '1.0'), self.persistence,
            Descriptor('pip-service-data', 'controller', 'default', 'default', '1.0'), self.controller,
            Descriptor('pip-service-data', 'service', 'http', 'default', '1.0'), self.service
        )

        self.controller.set_references(references)
        self.service.set_references(references)

        self.persistence.open(None)
        self.service.open(None)
        self.client.open(None)

    def teardown_method(self):
        self.persistence.close(None)
        self.service.close(None)
        self.client.close(None)

    def test_crud_operations(self):
        # Create the first entity
        response = self.client.call_command('create_entity', None, {'entity': ENTITY1})

        entity = EntityV1(**response)

        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        response = self.client.call_command('create_entity', None, {'entity': ENTITY2})

        entity = EntityV1(**response)

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
        assert len(page['data']) == 2

        # Update the entity
        entity1 = EntityV1(**page['data'][0])
        entity1.name = 'ABC'

        response = self.client.call_command('update_entity',
                                            None,
                                            {
                                                'entity': entity1
                                            })
        entity = EntityV1(**response)

        assert entity is not None
        assert entity.id == entity1.id
        assert 'ABC' == entity.name

        # Get entity by name
        response = self.client.call_command('get_entity_by_name',
                                            None,
                                            {
                                                'entity_name': entity1.name
                                            })

        entity = EntityV1(**response)

        assert entity is not None
        assert entity1.id == entity.id

        # Delete the entity
        response = self.client.call_command('delete_entity_by_id',
                                            None,
                                            {
                                                'entity_id': entity1.id
                                            })

        entity = EntityV1(**response)

        assert entity is not None
        assert entity.id == entity1.id

        # Try to get deleted entity
        entity = self.client.call_command('get_entity_by_id',
                                          None,
                                          {
                                              'entity_id': entity1.id
                                          })

        assert entity is None
