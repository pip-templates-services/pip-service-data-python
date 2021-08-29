# -*- coding: utf-8 -*-
import os

import pytest
from pip_services3_commons.config import ConfigParams

from pip_service_data_python.persistence.EntitiesPostgresPersistence import EntitiesPostgresPersistence
from test.persistence.EntitiesPersistenceFixture import EntitiesPersistenceFixture

postgres_uri = os.environ.get('POSTGRES_SERVICE_URI')
postgres_host = os.environ.get('POSTGRES_SERVICE_HOST') or 'localhost'
postgres_port = os.environ.get('POSTGRES_SERVICE_PORT') or 5432
postgres_database = os.environ.get('POSTGRES_SERVICE_DB') or 'test'
postgres_user = os.environ.get('POSTGRES_USER') or 'postgres'
postgres_password = os.environ.get('POSTGRES_PASS') or 'postgres'


@pytest.mark.skipif(not postgres_uri and not postgres_host, reason="Postgres connection is not set")
class TestEntitiesPostgresPersistence:
    persistence: EntitiesPostgresPersistence
    fixture: EntitiesPersistenceFixture

    def setup_method(self):
        self.persistence = EntitiesPostgresPersistence()
        self.persistence.configure(ConfigParams.from_tuples(
            'connection.uri', postgres_uri,
            'connection.host', postgres_host,
            'connection.port', postgres_port,
            'connection.database', postgres_database,
            'credential.username', postgres_user,
            'credential.password', postgres_password
        ))

        self.fixture = EntitiesPersistenceFixture(self.persistence)

        self.persistence.open(None)
        self.persistence.clear(None)

    def teardown_method(self):
        self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filters(self):
        self.fixture.test_get_with_filters()
