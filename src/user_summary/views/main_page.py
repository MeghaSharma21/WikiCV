from django.shortcuts import render

from user_summary.modules.badges_module import Badges_module
from user_summary.modules.wikipedia_summary_module \
    import Wikipedia_summary_module


# View that corresponds to the main page of WikiCV
def wiki_cv(request, username=''):
    summary_content = {}
    message = ''
    if username is not '':
        wikipedia_summary_object = Wikipedia_summary_module()
        success = \
            wikipedia_summary_object\
            .wikipediaSummaryStarterFunction(username)
        if success == 1:
            badges_object = Badges_module()
            badges_object.badgesStarterFunction(wikipedia_summary_object
                                                .editSummary,
                                                wikipedia_summary_object
                                                .userInfo)

            summary_content['firstContributionTimestamp'] = \
                wikipedia_summary_object.editSummary[
                    'firstContributionTimestamp']
            summary_content['lastContributionTimestamp'] = \
                wikipedia_summary_object.editSummary[
                    'lastContributionTimestamp']
            summary_content['bytesAdded'] = \
                wikipedia_summary_object.editSummary['bytesAdded']

            summary_content['pagesAboveContributionThreshold'] = \
                wikipedia_summary_object.pagesAboveContributionThreshold

            summary_content['numberOfArticlesCreated'] = \
                wikipedia_summary_object.articlesCreatedSummary[
                    'numberOfArticlesCreated']
            summary_content['editcount'] = \
                wikipedia_summary_object.userInfo['editcount']
            summary_content['name'] = \
                wikipedia_summary_object.userInfo['name']
            summary_content['specialGroups'] = \
                wikipedia_summary_object.userInfo['specialGroups']
            summary_content['userLanguages'] = \
                wikipedia_summary_object.userLanguages

            # Populate badges for the user
            summary_content['badges'] = badges_object.badges
        else:
            message = "CV could not be loaded properly"
    return render(request, 'user_summary/summary.html',
                  {'wikipedia_summary_content': summary_content,
                   'message': message})
