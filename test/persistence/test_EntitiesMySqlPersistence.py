# -*- coding: utf-8 -*-
import os

import pytest
from pip_services3_commons.config import ConfigParams

from pip_service_data_python.persistence.EntitiesMySqlPersistence import EntitiesMySqlPersistence
from test.persistence.EntitiesPersistenceFixture import EntitiesPersistenceFixture

mysql_uri = os.environ.get('MYSQL_URI')
mysql_host = os.environ.get('MYSQL_HOST') or 'localhost'
mysql_port = os.environ.get('MYSQL_PORT') or 3306
mysql_database = os.environ.get('MYSQL_DB') or 'test'
mysql_user = os.environ.get('MYSQL_USER') or 'user'
mysql_password = os.environ.get('MYSQL_PASSWORD') or 'password'


@pytest.mark.skipif(not mysql_uri and not mysql_host, reason="MySql connection is not set")
class TestEntitiesMySqlPersistence:
    persistence: EntitiesMySqlPersistence
    fixture: EntitiesPersistenceFixture

    def setup_method(self):
        self.persistence = EntitiesMySqlPersistence()
        self.persistence.configure(ConfigParams.from_tuples(
            'connection.uri', mysql_uri,
            'connection.host', mysql_host,
            'connection.port', mysql_port,
            'connection.database', mysql_database,
            'credential.username', mysql_user,
            'credential.password', mysql_password
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
