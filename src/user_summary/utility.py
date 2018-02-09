import json
import requests


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
