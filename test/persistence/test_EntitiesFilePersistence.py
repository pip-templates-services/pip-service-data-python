# -*- coding: utf-8 -*-

from pip_service_data_python.persistence.EntitiesFilePersistence import EntitiesFilePersistence
from test.persistence.EntitiesPersistenceFixture import EntitiesPersistenceFixture


class TestEntitiesFilePersistence:
    persistence: EntitiesFilePersistence
    fixture: EntitiesPersistenceFixture

    def setup_method(self):
        self.persistence = EntitiesFilePersistence('data/entities.test.json')

        self.fixture = EntitiesPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filters(self):
        self.fixture.test_get_with_filters()
