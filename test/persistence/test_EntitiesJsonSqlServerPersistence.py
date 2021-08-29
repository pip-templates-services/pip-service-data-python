# -*- coding: utf-8 -*-
import os

import pytest
from pip_services3_commons.config import ConfigParams

from pip_service_data_python.persistence.EntitiesJsonSqlServerPersistence import EntitiesJsonSqlServerPersistence
from test.persistence.EntitiesPersistenceFixture import EntitiesPersistenceFixture

sqlserver_uri = os.environ.get('SQLSERVER_URI')
sqlserver_host = os.environ.get('SQLSERVER_HOST')  # or 'localhost'
sqlserver_port = os.environ.get('SQLSERVER_PORT') or 1433
sqlserver_database = os.environ.get('SQLSERVER_DB') or 'master'
sqlserver_user = os.environ.get('SQLSERVER_USER') or 'sa'
sqlserver_password = os.environ.get('SQLSERVER_PASSWORD') or 'sqlserver_123'


@pytest.mark.skipif(not sqlserver_uri and not sqlserver_host, reason="JsonSqlServer connection is not set")
class TestEntitiesJsonSqlServerPersistence:
    persistence: EntitiesJsonSqlServerPersistence
    fixture: EntitiesPersistenceFixture

    def setup_method(self):
        self.persistence = EntitiesJsonSqlServerPersistence()
        self.persistence.configure(ConfigParams.from_tuples(
            'connection.uri', sqlserver_uri,
            'connection.host', sqlserver_host,
            'connection.port', sqlserver_port,
            'connection.database', sqlserver_database,
            'credential.username', sqlserver_user,
            'credential.password', sqlserver_password
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
