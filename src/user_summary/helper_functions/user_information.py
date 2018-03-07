import requests
import json
import langcodes
import logging
import toolforge

# Get an instance of a logger
logger = logging.getLogger('django')


# Function that fetches User information
# (mainly name, special groups) using API
def getUserInfoFromAPI(username):
    message = "User info was successfully fetched" \
              + "for username:" + str(username)
    name = ''
    specialGroups = ''
    result = True
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'users',
                  'ususers': username,
                  'usprop': 'groupmemberships'}
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
            name = userData['name']
            specialGroups = [i['group'] for i in userData['groupmemberships']]
    else:
        # If response code is not ok
        result = False
        message = 'Execution Failed at MediaWiki web service API,'
        + 'HTTP Response Code: ' + str(responseObject.status_code)

    logger.info(message)
    return {'name': name, 'specialGroups': specialGroups,
            'result': result}


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


# Function to calculate user's rank based on the contributions
def calculateUserContributionRank(username):
    results = {'success': True, 'user_rank': -1, 'complete_edit_count': -1}
    message = "User's contribution rank calculated successfully. Results:"
    try:
        conn = toolforge.connect('enwiki')
        with conn.cursor() as cursor:
            # finding how many users have greater editcount
            #  than that of given username
            cursor.execute(
                'SELECT count(*), useredits.user_editcount FROM user, '
                '(SELECT * FROM user WHERE user_name = %s ) AS useredits  '
                'WHERE user.user_editcount > useredits.user_editcount',
                [username])
            result = cursor.fetchone()

    except Exception:
        results['success'] = False
        message = 'Error occurred while calculating contribution ' \
                  'distribution for all users. Results:'
    finally:
        cursor.close()
        conn.close()

    if results['success']:
        results['user_rank'] = result[0] + 1
        results['complete_edit_count'] = result[1]

    logger.info("{0}{1}".format(message, str(results)))
    return results
