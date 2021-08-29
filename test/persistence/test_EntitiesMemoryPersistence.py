# -*- coding: utf-8 -*-

from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from test.persistence.EntitiesPersistenceFixture import EntitiesPersistenceFixture


class TestEntitiesMemoryPersistence:
    persistence: EntitiesMemoryPersistence
    fixture: EntitiesPersistenceFixture

    def setup_method(self):
        self.persistence = EntitiesMemoryPersistence()

        self.fixture = EntitiesPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filters(self):
        self.fixture.test_get_with_filters()
