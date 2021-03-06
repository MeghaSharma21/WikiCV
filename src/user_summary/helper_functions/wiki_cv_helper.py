import json
from user_summary.helper_functions.calculate_page_assessments \
    import calculate_page_to_project_mapping
from user_summary.helper_functions.calculate_views_for_pages \
    import calculate_page_to_views_mapping
from user_summary.models import PageAttributesTable
from user_summary.modules.achievements_module import AchievementsModule
from user_summary.modules.badges_module import BadgesModule
from user_summary.modules.graphs_module import GraphsModule
from user_summary.modules.wikipedia_summary_module \
    import WikipediaSummaryModule


# Helper function for the wiki_cv function
def wiki_cv_helper_function(username):
    achievements_content = []
    total_contribution_by_all_in_pages = {}
    contribution_distribution = {}
    wikipedia_summary_object = WikipediaSummaryModule()
    achievements_object = AchievementsModule()
    success = wikipedia_summary_object\
        .wikipediaSummaryStarterFunction(username)
    if success == 1:
        badges_object = BadgesModule()
        # Populate badges for the user
        badges_object.badgesStarterFunction(wikipedia_summary_object
                                            .editSummary,
                                            wikipedia_summary_object.userInfo)
        total_contribution_by_all_in_pages = \
            wikipedia_summary_object.userAuthorshipMapping[
                'total_contribution']
        summary_content = {'username': username,
                           'firstContributionTimestamp':
                               wikipedia_summary_object
                           .editSummary['firstContributionTimestamp'],
                           'lastContributionTimestamp':
                               wikipedia_summary_object.editSummary[
                                   'lastContributionTimestamp'],
                           'pages_contributed':
                               wikipedia_summary_object
                           .editSummary['pagesContributed'],
                           'bytesAdded': wikipedia_summary_object
                               .editSummary['bytesAdded'],
                           'editCount': wikipedia_summary_object
                               .editSummary['editCount'],
                           'pagesAboveContributionThreshold':
                               wikipedia_summary_object
                           .pagesAboveContributionThreshold,
                           'numberOfArticlesCreated': wikipedia_summary_object
                               .articlesCreatedSummary[
                                'numberOfArticlesCreated'],
                           'name': wikipedia_summary_object.userInfo['name'],
                           'specialGroups': wikipedia_summary_object
                               .userInfo['specialGroups'],
                           'userLanguages': wikipedia_summary_object
                               .userLanguages,
                           'badges': json.dumps(badges_object.badges),
                           'percentageContributionInArticles':
                               wikipedia_summary_object
                               .userAuthorshipMapping[
                                   'percentageContribution'],
                           'contribution_threshold':
                               wikipedia_summary_object.contribution_threshold,
                           'user_contribution_based_on_time':
                               wikipedia_summary_object
                               .userAuthorshipMapping[
                                   'user_contribution_based_on_time']}

        # Populate achievements for the user
        edits_assessment = achievements_object. \
            calculate_achievements(username, wikipedia_summary_object
                                   .userAuthorshipMapping)
        if edits_assessment:
            achievements_content = achievements_object.achievements

        # Fetch data for user ranking graph
        user_ranking_graph_data = \
            GraphsModule.make_user_ranking_graph(username)
        if user_ranking_graph_data['success']:
            summary_content.update({'user_rank':
                                    user_ranking_graph_data['user_rank'],
                                   'user_group':
                                    user_ranking_graph_data['user_group'],
                                    'user_complete_edit_count':
                                        user_ranking_graph_data[
                                            'user_complete_edit_count'],
                                    'user_percentile':
                                        user_ranking_graph_data[
                                            'user_percentile']})

            contribution_distribution = {'total_no_of_users':
                                         user_ranking_graph_data[
                                             'total_no_of_users'],
                                         'percentage_of_users_in_group':
                                         user_ranking_graph_data[
                                             'percentage_of_users_in_group']}
        return {'summary_content': summary_content,
                'achievements_content': achievements_content,
                'edits_array': wikipedia_summary_object
                .editSummary['editsArray'],
                'articles_created_array': wikipedia_summary_object
                .articlesCreatedSummary['articlesCreatedArray'],
                'page_to_project_mapping':
                    calculate_page_to_project_mapping(edits_assessment),
                'contribution_distribution': contribution_distribution,
                'total_contribution_by_all_in_pages':
                    total_contribution_by_all_in_pages}


# Helper function for storing data for Impact graph
def impact_graph_helper_function(wiki_data):
    page_views_dict = \
        calculate_page_to_views_mapping(wiki_data['summary_content'][
                                            'pages_contributed'])
    PageAttributesTable \
        .update_or_create_object(wiki_data['summary_content'][
                                         'pages_contributed'],
                                 page_views_dict,
                                 wiki_data[
                                         'total_contribution_by_all_in_pages'])
