# -*- coding: utf-8 -*-
import http.client
import json

import requests
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import DataPage
from pip_services3_commons.refer import References, Descriptor

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from pip_service_data_python.services.version1.EntitiesRestServiceV1 import EntitiesRestServiceV1

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
url = 'http://localhost:3000'


class TestEntitiesRestServiceV1:
    service: EntitiesRestServiceV1
    rest: http.client.HTTPConnection

    @classmethod
    def setup_class(cls):
        persistence = EntitiesMemoryPersistence()
        controller = EntitiesController()

        cls.service = EntitiesRestServiceV1()
        cls.service.configure(http_config)

        references: References = References.from_tuples(
            Descriptor('pip-service-data', 'persistence', 'memory', 'default', '1.0'), persistence,
            Descriptor('pip-service-data', 'controller', 'default', 'default', '1.0'), controller,
            Descriptor('pip-service-data', 'service', 'http', 'default', '1.0'), cls.service
        )
        controller.set_references(references)
        cls.service.set_references(references)

        cls.service.open(None)

    @classmethod
    def teardown_class(cls):
        cls.service.close(None)

    def test_crud_operations(self):
        # Create the first entity
        response = requests.post(url + '/v1/entities/entities', json=ENTITY1.to_dict())
        entity = EntityV1(**json.loads(response.text))
        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        # Create the first entity
        response = requests.post(url + '/v1/entities/entities', json=ENTITY2.to_dict())
        entity = EntityV1(**json.loads(response.text))
        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Get all entities
        response = requests.get(url + '/v1/entities/entities')
        page = DataPage(**json.loads(response.text))

        assert len(page.data) == 2

        entity1 = EntityV1(**page.data[0])

        # Update the entity
        entity1.name = 'ABC'

        response = requests.put(url + '/v1/entities/entities', json=entity1.to_dict())
        entity = EntityV1(**json.loads(response.text))

        assert entity1.id == entity.id
        assert 'ABC' == entity.name

        # Get entity by name
        response = requests.get(url + '/v1/entities/entities/name/' + entity1.name)
        entity = EntityV1(**json.loads(response.text))

        assert entity1.id == entity.id

        # Delete the entity
        response = requests.delete(url + '/v1/entities/entities/' + entity1.id)
        entity = EntityV1(**json.loads(response.text))

        assert entity1.id == entity.id

        # Try to get deleted entity
        response = requests.get(url + '/v1/entities/entities/' + entity1.id)

        assert response.status_code == 204
