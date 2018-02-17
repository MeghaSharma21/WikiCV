import json
import requests
import user_summary.constants as constants
import datetime


# General function to call MediaWiki API and fetch data from it
def fetch_data_from_mediawiki_api(parameters):
    message = ''
    result = True
    json_data = {}
    url = 'https://en.wikipedia.org/w/api.php'
    response_object = requests.get(url, params=parameters)
    if response_object.status_code == 200:
        # Loading the response data into a dict variable
        json_data = json.loads(response_object.text)
        if 'error' in json_data:
            result = False
            message = 'Execution Failed at MediaWiki web service API,' \
                      + 'Error:' + str(json_data['error']['info'])
    else:
        # If response code is not ok
        result = False
        message = 'Execution Failed at MediaWiki web service API,' \
                  + 'HTTP Response Code: ' \
                  + str(response_object.status_code)

    return {"result": result, "message": message, "json_data": json_data}


# General function to assign datetime object to time filters
def evaluate_time_filters():
    filters_time_dict = {}
    for key, value in constants.TIME_FILTER_MAPPING.items():
        filters_time_dict[key] = \
            (datetime.datetime.today() - datetime.timedelta(value))
    return filters_time_dict


# Utility function to convert string into datetime object
def convert_string_to_datetime(date_string):
    return datetime.datetime.strptime(str(date_string), '%Y-%m-%dT%H:%M:%SZ')
