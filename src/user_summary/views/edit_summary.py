import requests
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Function fetches the information regarding all edits
# of the user using MediaWiki API
def getEditSummary(username):
    message = 'Edit summary fetched Successfully for' + username
    result = True
    pagesContributed = []
    userId = -1
    firstContributionTimestamp = ''
    lastContributionTimestamp = ''
    bytesAdded = 0
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'usercontribs',
                  'uclimit': 'max',
                  'ucnamespace': 0,  # As we want to track
                                     # authorship only in articles
                  'ucuser': username,
                  'ucdir': 'newer'}

    while True:
        url = 'https://en.wikipedia.org/w/api.php'
        responseObject = requests.get(url, params=parameters)
        if responseObject.status_code == 200:
            # Loading the response data into a dict variable
            jsonData = json.loads(responseObject.text)
            if 'error' in jsonData:
                result = False
                message = 'Execution Failed at MediaWiki web service API,' \
                          + 'Error:' + str(jsonData['error']['info']) \
                          + '. Hence, edit summary for ' \
                          + username + 'could not be loaded.'
                break
            else:
                contributionData = [i for i in
                                    jsonData['query']['usercontribs']]
                if len(contributionData) > 0:
                    userId = contributionData[0]['userid']
                    if firstContributionTimestamp == '':
                        firstContributionTimestamp = \
                            contributionData[0]['timestamp']
                    lastContributionTimestamp = \
                        contributionData[-1]['timestamp']
                    for contributionDetails in contributionData:
                        pagesContributed.append(contributionDetails['pageid'])
                        bytesAdded = bytesAdded + contributionDetails['size']
                    # maintaining unique pages to which user contributed
                    pagesContributed = list(set(pagesContributed))
                    # Continuing if there're more results
                    if 'continue' in jsonData:
                        parameters['uccontinue'] = \
                            jsonData['continue']['uccontinue']
                        parameters['continue'] = \
                            jsonData['continue']['continue']
                    else:
                        break
        else:
            # If response code is not ok
            result = False
            message = 'Execution Failed at MediaWiki web service API,' \
                      + 'HTTP Response Code: '\
                      + str(responseObject.status_code) \
                      + '. Hence, edit summary for ' + username \
                      + 'could not be loaded.'
            break

    logger.info(message)
    return {"result": result, "pagesContributed": pagesContributed,
            "userId": userId,
            "firstContributionTimestamp": firstContributionTimestamp,
            "lastContributionTimestamp": lastContributionTimestamp,
            "bytesAdded": bytesAdded}


# Function to fetch information regarding the articles created by the user
def getArticlesCreatedSummary(username):
    message = 'Articles created summary fetched successfully for' + username
    numberOfArticlesCreated = 0
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'usercontribs',
                  'uclimit': 'max',
                  'ucnamespace': 0,  # As we want to track only articles
                  'ucuser': username,
                  'ucdir': 'older',
                  'ucshow': 'new'}
    result = True
    url = 'https://en.wikipedia.org/w/api.php'
    while True:
        responseObject = requests.get(url, params=parameters)
        if responseObject.status_code == 200:
                # Loading the response data into a dict variable
                jsonData = json.loads(responseObject.text)
                if 'error' in jsonData:
                    result = False
                    message = 'Execution Failed at MediaWiki web' \
                              + 'service API,Error: ' \
                              + str(jsonData['error']['info'])
                    break
                else:
                    contributionData = [i for i in
                                        jsonData['query']['usercontribs']]
                    numberOfArticlesCreated = numberOfArticlesCreated
                    + len(contributionData)
                    if 'continue' in jsonData:
                        parameters['uccontinue'] = \
                            jsonData['continue']['uccontinue']
                        parameters['continue'] = \
                            jsonData['continue']['continue']
                    else:
                        break
        else:
                # If response code is not ok (200)
                result = False
                message = 'Execution Failed at MediaWiki web service API,' \
                          + 'HTTP Response Code:'\
                          + str(responseObject.status_code) \
                          + '. Hence, cannot fetch articles created summary.'
                break
    logger.info(message)
    return {"result": result,
            "numberOfArticlesCreated": numberOfArticlesCreated}
