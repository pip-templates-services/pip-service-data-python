# -*- coding: utf-8 -*-

from pip_services3_commons.config import ConfigParams
from pip_services3_data.persistence import JsonFilePersister

from pip_service_data_python.persistence.EntitiesMemoryPersistence import EntitiesMemoryPersistence


class EntitiesFilePersistence(EntitiesMemoryPersistence):

    def __init__(self, path: str = None):
        super().__init__()

        self._persister = JsonFilePersister(path)
        self._loader = self._persister
        self._saver = self._persister

    def configure(self, config: ConfigParams):
        super().configure(config)
        self._persister.configure(config)
