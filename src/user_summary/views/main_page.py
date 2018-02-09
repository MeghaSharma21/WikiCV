from django.shortcuts import render

from user_summary.modules.achievements_module import AchievementsModule
from user_summary.modules.badges_module import BadgesModule
from user_summary.modules.wikipedia_summary_module \
    import WikipediaSummaryModule


# View that corresponds to the main page of WikiCV
def wiki_cv(request, username):
    summary_content = {}
    achievements_content = []
    message = ''
    if username is not None:
        wikipedia_summary_object = WikipediaSummaryModule()
        success = \
            wikipedia_summary_object\
            .wikipediaSummaryStarterFunction(username)
        if success == 1:
            badges_object = BadgesModule()
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

            achievements_object = AchievementsModule()
            if achievements_object.\
                    calculate_achievements(wikipedia_summary_object.userAuthorshipMapping):
                achievements_content = achievements_object.achievements
        else:
            message = "CV could not be loaded properly"
    return render(request, 'user_summary/summary.html',
                  {'wikipedia_summary_content': summary_content,
                   'achievements_content': achievements_content,
                   'message': message})
