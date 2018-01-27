import toolforge
import logging
from .edit_summary import getEditSummary, getArticlesCreatedSummary
from .user_information import getUserInfoFromAPI, getUserLanguages
from .badges_module import assignBadges
from django.shortcuts import render

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Function calculates authorship of the user in
# every article he/she has contributed
def calculateUserAuthorishipMapping(pagesContributed, userId):
    message = 'Authorship calculated Successfully for all articles'
    result = True
    if len(pagesContributed) > 0:
        # Dictionary which will map pageId and contributions to it
        contributionByAll = {}
        contributionByUsername = {}
        # Dictionary which will map articleName and
        # percentage contribution to it by username
        percentageContribution = {}
        pages = ', '.join(str(page) for page in pagesContributed)
        try:
            conn = toolforge.connect('enwiki')
            with conn.cursor() as cursor:
                cursor.execute('SELECT rev_page, SUM(ABS(rev_len))'
                               + 'FROM revision WHERE rev_page IN'
                               + '(%s) AND rev_deleted <>'
                               + '1 GROUP BY rev_page' % (pages))
                results = cursor.fetchall()
                for result in results:
                    contributionByAll[result[0]] = result[1]
                cursor.execute('SELECT rev_page, SUM(ABS(rev_len))'
                               + 'FROM revision WHERE rev_page IN'
                               + '(%s) AND rev_user = %s AND'
                               + 'rev_deleted <> 1 GROUP BY'
                               + 'rev_page' % (pages, str(userId)))
                results = cursor.fetchall()
                for result in results:
                    contributionByUsername[result[0]] = result[1]
        except Exception as e:
            message = 'Exception occured while establishing' \
                      + 'connection with database for calculating' \
                      + 'user-authorship mapping. Exception: ' + str(e)
            result = False
        finally:
            cursor.close()
            conn.close()
        for page in pagesContributed:
            percentageContribution[page] = \
                (contributionByUsername[page]*100)/contributionByAll[page]
    else:
        message = 'The user does not have any contributions. Hence,'
        + 'can not calculate user-authorship mapping'
        result = False

    logger.info(message)
    return {'percentageContribution': percentageContribution, 'result': result}


# Function corresponds to the Wikimedia Summary section of the design
def wikipediaSummaryModule(request):
    content = {}
    if request.method == 'POST':
        username = request.POST['username']
        contributionThreshold = 15
        content['username'] = username

        # Get information regarding all the edits by
        # the user from MediaWiki API
        editSummary = getEditSummary(username)
        if editSummary['result'] is True:
            content['firstContributionTimestamp'] = \
                editSummary['firstContributionTimestamp']
            content['lastContributionTimestamp'] = \
                editSummary['lastContributionTimestamp']
            content['bytesAdded'] = editSummary['bytesAdded']
            userAuthorshipMapping = \
                calculateUserAuthorishipMapping(editSummary[
                                                    'pagesContributed'],
                                                editSummary['userId'])
            # Calculate no. of articles which are
            # above the contribution threshold
            if userAuthorshipMapping['result'] is True:
                pagesAboveContributionThreshold = 0
                for key, value in \
                        userAuthorshipMapping['percentageContribution'] \
                        .items():
                    if value >= contributionThreshold:
                        pagesAboveContributionThreshold = \
                            pagesAboveContributionThreshold + 1
                content['pagesAboveContributionThreshold'] = \
                    pagesAboveContributionThreshold

        # Get summary of the articles created by the user
        articlesCreatedSummary = getArticlesCreatedSummary(username)
        if articlesCreatedSummary['result'] is True:
            content['numberOfArticlesCreated'] = \
                articlesCreatedSummary['numberOfArticlesCreated']

        # Get information regarding the user
        userInfo = getUserInfoFromAPI(username)
        if userInfo['result'] is True:
            content['editcount'] = userInfo['editcount']
            content['name'] = userInfo['name']
            content['specialGroups'] = userInfo['specialGroups']

        # Get the languages known to the user
        userLanguages = getUserLanguages(username)
        if userLanguages['result'] is True:
            content['userLanguages'] = userLanguages['languagesKnown']

        # Check for exceptions
        if editSummary['result'] is False or \
                articlesCreatedSummary['result'] is False or \
                userInfo['result'] is False or \
                userAuthorshipMapping['result'] is False or \
                userLanguages['result'] is False:
            content['message'] = 'All elements of CV could not be loaded' \
                                 + 'properly. If the problem persists,' \
                                 + 'contact meghasharma4910@gmail.com'

        # Populate badges for the user
        content['badges'] = assignBadges(editSummary['userId'],
                                         content.get(
                                             'firstContributionTimestamp'),
                                         content.get(
                                             'lastContributionTimestamp'),
                                         content.get('bytesAdded'),
                                         content.get('specialGroups'))

    return render(request, 'user_summary/summary.html', {'content': content})
