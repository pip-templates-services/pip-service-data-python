# -*- coding: utf-8 -*-
from pip_services3_aws.containers.LambdaFunction import LambdaFunction
from pip_services3_prometheus.build.DefaultPrometheusFactory import DefaultPrometheusFactory

from pip_service_data_python.build.EntitiesServiceFactory import EntitiesServiceFactory


class EntitiesLambdaFunction(LambdaFunction):
    def __init__(self):
        super().__init__("pip-service-data", "Entities data microservice")
        self._factories.add(EntitiesServiceFactory())
        self._factories.add(DefaultPrometheusFactory())
