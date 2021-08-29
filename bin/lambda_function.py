# -*- coding: utf-8 -*-

from pip_service_data_python.containers.EntitiesLambdaFunction import EntitiesLambdaFunction


def lambda_handler(event, context):
    return EntitiesLambdaFunction().get_handler()(event)
