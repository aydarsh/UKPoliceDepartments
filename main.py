#!/usr/bin/env python3

import pandas as pd
import json
import requests
import logging
from pandas.core.common import flatten

logging.basicConfig(level=logging.WARNING)


class ApiError(Exception):
    """
    Exception raised for API errors.
    Attributes:
        message - explanation of the error
    """

    def __init__(self, message):
        self.message = message


api_url_base_value = 'https://data.police.uk/api'
headers_value = {'Content-Type': 'application/json'}


def get_police_forces(api_url_base, headers):
    """
    Gets all police forces
    """
    api_url_request = '/forces'

    response = requests.get(f'{api_url_base}{api_url_request}', headers=headers)
    if response.status_code != 200:
        raise ApiError(f'GET {api_url_request} {response.status_code}')

    #     loads response json into a pandas dataframe
    result_response = json.loads(response.content.decode('utf-8'))
    df_result = pd.DataFrame(result_response)

    return df_result


def get_social_engagement_methods(api_url_base, headers, police_force):
    """
    Gets social engagement methods for the specified police_force
    """
    api_url_request = f'/forces/{police_force}'

    response = requests.get(f'{api_url_base}{api_url_request}', headers=headers)
    if response.status_code != 200:
        raise ApiError(f'GET {api_url_request} {response.status_code}')

    #     loads response json into a pandas dataframe
    result_response = json.loads(response.content.decode('utf-8'))['engagement_methods']
    df_result = pd.DataFrame(result_response)

    return df_result


def has_social_engagement_method(api_url_base, headers, social_engagement_method, police_force):
    """
    Checks if a police force has specified social engagement method
    """
    df_social_engagement_methods = get_social_engagement_methods(api_url_base, headers, police_force)
    #     gets all values for the social engagement methods
    list_of_dataframe_string_values = flatten(df_social_engagement_methods.values)
    #     filters out None values
    filtered_list = filter(None, list_of_dataframe_string_values)
    #     checks if there is any specified social among retrieved values
    #     this is needed, since not all police forces have a specified engagement method of type
    has_result = any([social_engagement_method.lower() in values.lower() for values in filtered_list])
    return has_result


def get_police_forces_by_social_engagement_method(api_url_base, headers, social_engagement_method):
    """
    Gets all police forces that have the specified social engagement method
    """
    #     gets all police forces
    df_police_forces = get_police_forces(api_url_base, headers)
    #     adds a column with bool values if a police force has the specified social engagement method
    df_police_forces[social_engagement_method] = df_police_forces.apply(
        lambda x: has_social_engagement_method(api_url_base, headers, social_engagement_method, x['id']), axis=1)
    #     filters out rows with False value
    df_police_forces = df_police_forces[df_police_forces[social_engagement_method]]
    #     drops the social_engagement_method from the return values
    df_police_forces.drop(columns=[social_engagement_method], inplace=True)
    #     resets the index
    df_police_forces.reset_index(drop=True, inplace=True)

    return df_police_forces


if __name__ == '__main__':

    social_engagement_method_value = 'facebook'

    logger = logging.getLogger(f'police forces that have {social_engagement_method_value}: ')
    logger.setLevel(logging.INFO)

    try:
        police_forces_result = get_police_forces_by_social_engagement_method(api_url_base_value, headers_value,
                                                                             social_engagement_method_value)
        logger.info(f"\n{police_forces_result}")

    except ApiError as e:
        logger.exception(f'API Error: \n{e}')
