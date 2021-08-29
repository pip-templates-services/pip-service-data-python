# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import DataPage

from pip_service_data_python.containers.EntitiesLambdaFunction import EntitiesLambdaFunction
from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1

ENTITY1 = EntityV1(
    id='1',
    name='00001',
    type=EntityTypeV1.Type1,
    site_id='1',
    content='ABC'
)

ENTITY2 = EntityV1(
    id='2',
    name='00002',
    type=EntityTypeV1.Type2,
    site_id='1',
    content='XYZ'
)


class TestEntitiesLambdaServiceV1:
    lambda_func: EntitiesLambdaFunction

    @classmethod
    def setup_class(cls):
        config = ConfigParams.from_tuples(
            'logger.descriptor', 'pip-services:logger:console:default:1.0',
            'persistence.descriptor', 'pip-service-data:persistence:memory:default:1.0',
            'controller.descriptor', 'pip-service-data:controller:default:default:1.0',
            'service.descriptor', 'pip-service-data:service:lambda:default:1.0'
        )

        cls.lambda_func = EntitiesLambdaFunction()
        cls.lambda_func.configure(config)

        cls.lambda_func.open(None)

    @classmethod
    def teardown_class(cls):
        cls.lambda_func.close(None)

    def test_crud_operations(self):
        # Create one entity
        entity = self.lambda_func.act({
            'cmd': 'v1.entities.create_entity',
            'entity': ENTITY1
        })

        assert entity is not None
        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        entity1 = entity

        # Create another entity
        entity = self.lambda_func.act({
            'cmd': 'v1.entities.create_entity',
            'entity': ENTITY2
        })

        assert entity is not None
        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Get all entities
        page: DataPage = self.lambda_func.act({
            'cmd': 'v1.entities.get_entities',
            'filter': {}
        })

        assert page is not None
        assert len(page.data) == 2

        # Update the entity
        entity1.name = 'Updated Entity 1'

        entity = self.lambda_func.act({
            'cmd': 'v1.entities.update_entity',
            'entity': entity1
        })

        assert entity is not None
        assert entity1.id == entity.id
        assert 'Updated Entity 1' == entity.name

        # Delete account
        entity = self.lambda_func.act({
            'cmd': 'v1.entities.delete_entity_by_id',
            'entity_id': entity1.id,
        })

        # Try to get delete entity
        entity = self.lambda_func.act({
            'cmd': 'v1.entities.get_entity_by_id',
            'entity_id': entity1.id,
        })

        assert entity is None
