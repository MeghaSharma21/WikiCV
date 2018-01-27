import requests
import json
import langcodes
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Function that fetches User information
# (mainly name, edit count, special groups) using API
def getUserInfoFromAPI(username):
    message = "User info was successfully fetched" \
              + "for username:" + str(username)
    editcount = ''
    name = ''
    specialGroups = ''
    result = True
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'users',
                  'ususers': username,
                  'usprop': 'groupmemberships|editcount'}
    url = 'https://en.wikipedia.org/w/api.php'
    responseObject = requests.get(url, params=parameters)
    if responseObject.status_code == 200:
        # Loading the response data into a dict variable
        jsonData = json.loads(responseObject.text)
        if 'error' in jsonData:
            result = False
            message = 'Execution Failed at MediaWiki web service API,' \
                      + 'Error: ' + str(jsonData['error']['info'])
        else:
            userData = jsonData['query']['users'][0]
            editcount = userData['editcount']
            name = userData['name']
            specialGroups = [i['group'] for i in userData['groupmemberships']]
    else:
        # If response code is not ok
        result = False
        message = 'Execution Failed at MediaWiki web service API,'
        + 'HTTP Response Code: ' + str(responseObject.status_code)

    logger.info(message)
    return {'editcount': editcount, 'name': name,
            'specialGroups': specialGroups, 'result': result}


# Function to fetch user's languages using MediaWiki API
def getUserLanguages(username):
    result = True
    message = "User's languages were successfully fetched for username:" \
              + str(username)
    languagesKnown = []
    parameters = {'action': 'query',
                  'format': 'json',
                  'meta': 'babel',
                  'babuser': username
                  }
    url = 'https://en.wikipedia.org/w/api.php'
    responseObject = requests.get(url, params=parameters)
    if responseObject.status_code == 200:
        # Loading the response data into a dict variable
        jsonData = json.loads(responseObject.text)
        if 'error' in jsonData:
            result = False
            message = 'Execution Failed at MediaWiki web service API,' \
                      + 'Error: ' + str(jsonData['error']['info'])
        else:
            languages = [i for i in jsonData['query']['babel']]
            for key in languages:
                # Converts language code into full english name of the language
                languagesKnown.append(langcodes.Language
                                      .make(language=str(key))
                                      .language_name())

    logger.info(message)
    return {"languagesKnown": languagesKnown, "result": result}
