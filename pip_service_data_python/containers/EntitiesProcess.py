# -*- coding: utf-8 -*-

from pip_services3_container import ProcessContainer
from pip_services3_datadog.build.DefaultDataDogFactory import DefaultDataDogFactory
from pip_services3_elasticsearch.build.DefaultElasticSearchFactory import DefaultElasticSearchFactory
from pip_services3_grpc.build.DefaultGrpcFactory import DefaultGrpcFactory
from pip_services3_prometheus.build.DefaultPrometheusFactory import DefaultPrometheusFactory
from pip_services3_rpc.build.DefaultRpcFactory import DefaultRpcFactory
from pip_services3_swagger.build.DefaultSwaggerFactory import DefaultSwaggerFactory

from pip_service_data_python.build.EntitiesServiceFactory import EntitiesServiceFactory


class EntitiesProcess(ProcessContainer):
    def __init__(self):
        super().__init__('pip-service-data', 'Entities data microservice')

        self._factories.add(EntitiesServiceFactory())
        self._factories.add(DefaultElasticSearchFactory())
        self._factories.add(DefaultPrometheusFactory())
        self._factories.add(DefaultDataDogFactory())
        self._factories.add(DefaultRpcFactory())
        self._factories.add(DefaultSwaggerFactory())
        self._factories.add(DefaultGrpcFactory())
