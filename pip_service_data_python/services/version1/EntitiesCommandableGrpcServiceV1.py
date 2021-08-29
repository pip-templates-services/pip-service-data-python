# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_grpc.services.CommandableGrpcService import CommandableGrpcService


class EntitiesCommandableGrpcServiceV1(CommandableGrpcService):
    def __init__(self):
        super().__init__('v1.entities')

        self._dependency_resolver.put('controller', Descriptor('pip-service-data', 'controller', '*', '*', '1.0'))
