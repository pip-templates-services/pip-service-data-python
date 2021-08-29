# -*- coding: utf-8 -*-
import os
import sys

# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pip_service_data_python.containers.EntitiesProcess import EntitiesProcess


proc = EntitiesProcess()
proc._config_path = "./config/config.yml"
proc.run()

