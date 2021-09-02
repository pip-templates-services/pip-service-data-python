# -*- coding: utf-8 -*-
import json
import os
import sys

from pip_services3_commons.convert import JsonConverter

from pip_service_data_python.containers.EntitiesLambdaFunction import EntitiesLambdaFunction

# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

handler = EntitiesLambdaFunction().get_handler()


def lambda_handler(event, context):
    if isinstance(event, (str, bytes, bytearray)):
        event = json.loads(event)

    result = handler(event)
    return JsonConverter.to_json(result)
