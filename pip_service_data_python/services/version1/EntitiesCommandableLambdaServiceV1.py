# -*- coding: utf-8 -*-
from pip_services3_aws.services.CommandableLambdaService import CommandableLambdaService
from pip_services3_commons.refer import Descriptor


class EntitiesCommandableLambdaServiceV1(CommandableLambdaService):
    def __init__(self):
        super().__init__('v1.entities')

        self._dependency_resolver.put('controller', Descriptor('pip-service-data', 'controller', '*', '*', '1.0'))
