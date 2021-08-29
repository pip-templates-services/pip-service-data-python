# -*- coding: utf-8 -*-
from pip_services3_commons.data import FilterParams, PagingParams

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.persistence.IEntitiesPersistence import IEntitiesPersistence

ENTITY1 = EntityV1(
    id='1',
    name='00001',
    type=EntityTypeV1.Type1,
    site_id='1',
    content='ABC'
)

ENTITY2 = EntityV1(
    id='2',
    name='00001',
    type=EntityTypeV1.Type2,
    site_id='1',
    content='XYZ'
)

ENTITY3 = EntityV1(
    id='3',
    name='00002',
    type=EntityTypeV1.Type1,
    site_id='2',
    content='DEF'
)


class EntitiesPersistenceFixture:
    _persistence: IEntitiesPersistence

    def __init__(self, persistence: IEntitiesPersistence):
        assert persistence is not None
        self._persistence = persistence

    def test_create_entities(self):
        # Create the first entity
        entity = self._persistence.create(None, ENTITY1)
        assert ENTITY1.name == entity.name
        assert ENTITY1.site_id == entity.site_id
        assert ENTITY1.type == entity.type
        assert ENTITY1.name == entity.name
        assert entity.content is not None

        # Create the second entity
        entity = self._persistence.create(None, ENTITY2)
        assert ENTITY2.name == entity.name
        assert ENTITY2.site_id == entity.site_id
        assert ENTITY2.type == entity.type
        assert ENTITY2.name == entity.name
        assert entity.content is not None

        # Create the third entity
        entity = self._persistence.create(None, ENTITY3)
        assert ENTITY3.name == entity.name
        assert ENTITY3.site_id == entity.site_id
        assert ENTITY3.type == entity.type
        assert ENTITY3.name == entity.name
        assert entity.content is not None

    def test_crud_operations(self):
        # Create items
        self.test_create_entities()

        # Get all entities
        page = self._persistence.get_page_by_filter(None, FilterParams(), PagingParams())
        assert page is not None
        assert len(page.data) == 3

        entity1: EntityV1 = page.data[0]

        # Update the entity
        entity1.name = 'ABC'

        entity = self._persistence.update(None, entity1)
        assert entity1.id == entity.id
        assert 'ABC' == entity.name

        # Get entity by name
        entity = self._persistence.get_one_by_name(None, entity1.name)
        assert entity1.id == entity.id

        # Delete the entity
        entity = self._persistence.delete_by_id(None, entity1.id)
        assert entity1.id == entity.id

        # Try to get deleted entity
        entity = self._persistence.get_one_by_id(None, entity1.id)
        assert entity is None

    def test_get_with_filters(self):
        # Create items
        self.test_create_entities()

        # Filter by id
        page = self._persistence.get_page_by_filter(None, FilterParams.from_tuples('id', '1'), PagingParams())
        assert len(page.data) == 1

        # Filter by name
        page = self._persistence.get_page_by_filter(None,
                                                    FilterParams.from_tuples('names', '00001,00003'),
                                                    PagingParams())
        assert len(page.data) == 2

        # Filter by site_id
        page = self._persistence.get_page_by_filter(None,
                                                    FilterParams.from_tuples('site_id', '1'),
                                                    PagingParams())
        assert len(page.data) == 2
