from user_summary.helper_functions.edit_summary import \
    getArticlesCreatedSummary, getEditSummary
from user_summary.helper_functions.user_authorship_mapping import \
    calculateUserAuthorishipMapping
from user_summary.helper_functions.user_information import \
    getUserInfoFromAPI, getUserLanguages


# Contains data and functions related to the summary section of WikiCV
class WikipediaSummaryModule:
    editSummary = {}
    userInfo = {}
    articlesCreatedSummary = {}
    pagesAboveContributionThreshold = 0
    userLanguages = []
    userAuthorshipMapping = {}

    # Starter function for fetching all the relevant data
    def wikipediaSummaryStarterFunction(self, username):
        content = {}
        contributionThreshold = 15
        content['username'] = username
        # Get information regarding all the edits by
        # the user from MediaWiki API
        editSummary = getEditSummary(username)

        if editSummary['result'] is True:
            self.editSummary = editSummary

            # Calculate no. of articles which are
            # above the contribution threshold
            userAuthorshipMapping = \
                calculateUserAuthorishipMapping(editSummary[
                                                    'pagesContributed'],
                                                editSummary['userId'])
            if userAuthorshipMapping['result'] is True:
                self.userAuthorshipMapping = userAuthorshipMapping
                pagesAboveContributionThreshold = 0
                for key, value in \
                        self.userAuthorshipMapping['percentageContribution'] \
                        .items():
                    if value >= contributionThreshold:
                        pagesAboveContributionThreshold = \
                            pagesAboveContributionThreshold + 1
                self.pagesAboveContributionThreshold = \
                    pagesAboveContributionThreshold

        # Get summary of the articles created by the user
        articlesCreatedSummary = getArticlesCreatedSummary(username)
        if articlesCreatedSummary['result'] is True:
            self.articlesCreatedSummary = articlesCreatedSummary

        # Get information regarding the user
        userInfo = getUserInfoFromAPI(username)
        if userInfo['result'] is True:
            self.userInfo = userInfo

        # Get the languages known to the user
        userLanguages = getUserLanguages(username)
        if userLanguages['result'] is True:
            self.userLanguages = userLanguages['languagesKnown']

        # Check for exceptions
        if editSummary['result'] is False or \
                articlesCreatedSummary['result'] is False or \
                userInfo['result'] is False or \
                userAuthorshipMapping['result'] is False or \
                userLanguages['result'] is False:
            return -1

        return 1
