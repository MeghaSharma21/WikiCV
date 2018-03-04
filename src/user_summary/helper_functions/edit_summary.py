import logging
from user_summary.utility import fetch_data_from_mediawiki_api

# Get an instance of a logger
logger = logging.getLogger('django')


# Function fetches the information regarding all edits
# of the user using MediaWiki API
def getEditSummary(username):
    message = 'Edit summary fetched Successfully for' + username
    pagesContributed = []
    editsArray = []
    userId = -1
    firstContributionTimestamp = ''
    lastContributionTimestamp = ''
    bytesAdded = 0
    editCount = 0
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'usercontribs',
                  'uclimit': 'max',
                  'ucnamespace': 0,  # As we want to track
                                     # authorship only in articles
                  'ucuser': username,
                  'ucdir': 'newer',
                  'ucprop': 'sizediff|timestamp|ids'}

    while True:
        results = fetch_data_from_mediawiki_api(parameters)
        if not results['result']:
            message = ''
            break
        jsonData = results['json_data']
        contributionData = jsonData['query']['usercontribs']
        editCount = editCount + len(contributionData)
        editsArray = editsArray + contributionData
        if len(contributionData) > 0:
            userId = contributionData[0]['userid']
            if firstContributionTimestamp == '':
                firstContributionTimestamp = \
                    contributionData[0]['timestamp']
            lastContributionTimestamp = \
                contributionData[-1]['timestamp']
            for contributionDetails in contributionData:
                pagesContributed.append(contributionDetails['pageid'])
                bytesAdded = bytesAdded + abs(contributionDetails['sizediff'])
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

    logger.info(message)
    return {"result": results['result'], "pagesContributed": pagesContributed,
            "userId": userId,
            "firstContributionTimestamp":  firstContributionTimestamp,
            "lastContributionTimestamp":   lastContributionTimestamp,
            "bytesAdded": bytesAdded, "editsArray": editsArray,
            "editCount": editCount}


# Function to fetch information regarding the articles created by the user
def getArticlesCreatedSummary(username):
    message = 'Articles created summary fetched successfully for' + username
    numberOfArticlesCreated = 0
    articlesCreatedArray = []
    parameters = {'action': 'query',
                  'format': 'json',
                  'list': 'usercontribs',
                  'uclimit': 'max',
                  'ucnamespace': 0,  # As we want to track only articles
                  'ucuser': username,
                  'ucdir': 'older',
                  'ucshow': 'new',
                  'ucprop': 'sizediff|timestamp|ids'}
    while True:
        results = fetch_data_from_mediawiki_api(parameters)
        if not results['result']:
            message = ''
            break
        jsonData = results['json_data']
        contributionData = jsonData['query']['usercontribs']
        articlesCreatedArray = articlesCreatedArray + contributionData
        numberOfArticlesCreated = \
            numberOfArticlesCreated + len(contributionData)
        if 'continue' in jsonData:
            parameters['uccontinue'] = \
                jsonData['continue']['uccontinue']
            parameters['continue'] = \
                jsonData['continue']['continue']
        else:
            break

    logger.info(message)
    return {"result": results['result'],
            "numberOfArticlesCreated": numberOfArticlesCreated,
            "articlesCreatedArray": articlesCreatedArray}
