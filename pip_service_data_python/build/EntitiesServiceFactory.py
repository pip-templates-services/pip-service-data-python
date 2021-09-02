# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory
from pip_services3_prometheus.build.DefaultPrometheusFactory import DefaultPrometheusFactory

from pip_service_data_python.logic.EntitiesController import EntitiesController
from pip_service_data_python.persistence.EntitiesFilePersistence import EntitiesFilePersistence
# from pip_service_data_python.persistence.EntitiesJsonMySqlPersistence import EntitiesJsonMySqlPersistence
from pip_service_data_python.persistence.EntitiesJsonPostgresPersistence import EntitiesJsonPostgresPersistence
# from pip_service_data_python.persistence.EntitiesJsonSqlServerPersistence import EntitiesJsonSqlServerPersistence
from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence
from pip_service_data_python.persistence.EntitiesMongoDbPersistence import EntitiesMongoDbPersistence
# from pip_service_data_python.persistence.EntitiesMySqlPersistence import EntitiesMySqlPersistence
from pip_service_data_python.persistence.EntitiesPostgresPersistence import EntitiesPostgresPersistence
# from pip_service_data_python.persistence.EntitiesSqlServerPersistence import EntitiesSqlServerPersistence
from pip_service_data_python.services.version1.EntitiesCommandableGrpcServiceV1 import EntitiesCommandableGrpcServiceV1
from pip_service_data_python.services.version1.EntitiesCommandableHttpServiceV1 import EntitiesCommandableHttpServiceV1
from pip_service_data_python.services.version1.EntitiesCommandableLambdaServiceV1 import \
    EntitiesCommandableLambdaServiceV1
from pip_service_data_python.services.version1.EntitiesGrpcServiceV1 import EntitiesGrpcServiceV1
from pip_service_data_python.services.version1.EntitiesLambdaServiceV1 import EntitiesLambdaServiceV1
from pip_service_data_python.services.version1.EntitiesRestServiceV1 import EntitiesRestServiceV1


class EntitiesServiceFactory(Factory):
    __MemoryPersistenceDescriptor = Descriptor('pip-service-data', 'persistence', 'memory', '*', '1.0')
    __FilePersistenceDescriptor = Descriptor('pip-service-data', 'persistence', 'file', '*', '1.0')
    __MongoDbPersistenceDescriptor = Descriptor('pip-service-data', 'persistence', 'mongodb', '*', '1.0')
    __EntitiesPostgresPersistence = Descriptor('pip-service-data', 'persistence', 'postgres', '*', '1.0')
    __EntitiesJsonPostgresPersistence = Descriptor('pip-service-data', 'persistence', 'json-postgres', '*', '1.0')
    __EntitiesMySqlPersistence = Descriptor('pip-service-data', 'persistence', 'mysql', '*', '1.0')
    __EntitiesJsonMySqlPersistence = Descriptor('pip-service-data', 'persistence', 'json-mysql', '*', '1.0')
    __EntitiesSqlServerPersistence = Descriptor('pip-service-data', 'persistence', 'sqlserver', '*', '1.0')
    __EntitiesJsonSqlServerPersistence = Descriptor('pip-service-data', 'persistence', 'json-sqlserver', '*', '1.0')
    __ControllerDescriptor = Descriptor('pip-service-data', 'controller', 'default', '*', '1.0')
    __CommandableHttpServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'commandable-http', '*', '1.0')
    __CommandableGrpcServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'commandable-grpc', '*', '1.0')
    __CommandableLambdaServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'commandable-lambda', '*', '1.0')
    __GrpcServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'grpc', '*', '1.0')
    __RestServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'rest', '*', '1.0')
    __LambdaServiceV1Descriptor = Descriptor('pip-service-data', 'service', 'lambda', '*', '1.0')

    def __init__(self):
        super().__init__()

        self.register_as_type(self.__MemoryPersistenceDescriptor, EntitiesMemoryPersistence)
        self.register_as_type(self.__FilePersistenceDescriptor, EntitiesFilePersistence)
        self.register_as_type(self.__MongoDbPersistenceDescriptor, EntitiesMongoDbPersistence)
        self.register_as_type(self.__EntitiesPostgresPersistence, EntitiesPostgresPersistence)
        self.register_as_type(self.__EntitiesJsonPostgresPersistence, EntitiesJsonPostgresPersistence)
        # self.register_as_type(self.__EntitiesMySqlPersistence, EntitiesMySqlPersistence)
        # self.register_as_type(self.__EntitiesJsonMySqlPersistence, EntitiesJsonMySqlPersistence)
        # self.register_as_type(self.__EntitiesSqlServerPersistence, EntitiesSqlServerPersistence)
        # self.register_as_type(self.__EntitiesJsonSqlServerPersistence, EntitiesJsonSqlServerPersistence)
        self.register_as_type(self.__ControllerDescriptor, EntitiesController)
        self.register_as_type(self.__CommandableHttpServiceV1Descriptor, EntitiesCommandableHttpServiceV1)
        self.register_as_type(self.__CommandableGrpcServiceV1Descriptor, EntitiesCommandableGrpcServiceV1)
        self.register_as_type(self.__CommandableLambdaServiceV1Descriptor, EntitiesCommandableLambdaServiceV1)
        self.register_as_type(self.__GrpcServiceV1Descriptor, EntitiesGrpcServiceV1)
        self.register_as_type(self.__RestServiceV1Descriptor, EntitiesRestServiceV1)
        self.register_as_type(self.__LambdaServiceV1Descriptor, EntitiesLambdaServiceV1)
