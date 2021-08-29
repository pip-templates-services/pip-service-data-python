# -*- coding: utf-8 -*-
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.refer import References, Descriptor

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence

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


class TestEntitiesController:
    persistence: EntitiesMemoryPersistence
    controller: EntitiesController

    def setup_method(self):
        self.persistence = EntitiesMemoryPersistence()
        self.persistence.configure(ConfigParams())

        self.controller = EntitiesController()
        self.controller.configure(ConfigParams())

        references = References.from_tuples(
            Descriptor('pip-service-data', 'persistence', 'memory', 'default', '1.0'), self.persistence,
            Descriptor('pip-service-data', 'controller', 'default', 'default', '1.0'), self.controller
        )

        self.controller.set_references(references)

        self.persistence.open(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        # Create the first entity
        entity = self.controller.create_entity(None, ENTITY1)
        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        # Create the second entity
        entity = self.controller.create_entity(None, ENTITY2)
        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Get all entities
        page = self.controller.get_entities(None, FilterParams(), PagingParams())
        assert page is not None
        assert len(page.data) == 2

        entity1: EntityV1 = page.data[0]

        # Update the entity
        entity1.name = 'ABC'

        entity = self.controller.update_entity(None, entity1)
        assert entity1.id == entity.id
        assert 'ABC' == entity.name

        # Get entity by name
        entity = self.controller.get_entity_by_name(None, entity1.name)
        assert entity1.id == entity.id

        # Delete the entity
        entity = self.controller.delete_entity_by_id(None, entity1.id)
        assert entity1.id == entity.id

        # Try to get deleted entity
        entity = self.controller.get_entities_by_id(None, entity1.id)
        assert entity is None
