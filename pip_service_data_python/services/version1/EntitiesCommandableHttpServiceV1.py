# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_rpc.services import CommandableHttpService


class EntitiesCommandableHttpServiceV1(CommandableHttpService):
    def __init__(self):
        super().__init__('v1/entities')

        self._dependency_resolver.put('controller', Descriptor('pip-service-data', 'controller', '*', '*', '1.0'))
