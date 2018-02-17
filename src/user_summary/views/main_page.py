from django.http import JsonResponse
from django.shortcuts import render
from user_summary.helper_functions.wiki_cv_helper \
    import wiki_cv_helper_function
from user_summary.models import DataCache, WikipediaGeneralDataCache
from user_summary.modules.graphs_module import GraphsModule
from user_summary.utility import evaluate_time_filters
import user_summary.constants as constants


# View that corresponds to the main page of WikiCV
def wiki_cv(request, username):
    message = ''
    data = {}
    if username is not None:
        if DataCache.objects.filter(username=username).count() == 0:
            data = wiki_cv_helper_function(username)
            DataCache.create_object(username, data)
        else:
            cached_data = DataCache.objects.get(username=username)
            data = {'summary_content': cached_data.summary_content,
                    'achievements_content': cached_data.achievements_content,
                    'edits_array':
                        cached_data.contribution_content['edits_array'],
                    'articles_created_array': cached_data
                    .contribution_content['articles_created_array'],
                    'page_to_project_mapping':
                        cached_data.page_to_project_mapping,
                    }

        if WikipediaGeneralDataCache.objects.filter(id=1).count() == 0:
            WikipediaGeneralDataCache \
                .update_or_create_object(data['contribution_distribution'])
        else:
            wikipedia_general_cached_data = WikipediaGeneralDataCache.objects\
                .get(id=constants.GENERAL_DATA_CACHE_DEFAULT_ID)
            data['contribution_distribution'] = \
                wikipedia_general_cached_data.contribution_distribution

    else:
        message = "CV could not be loaded properly"

    return render(request, 'user_summary/summary.html',
                  {'data': data, 'message': message})


# View that updates the cached data for the user
def update_cached_data(request, username):
    results = {'result': False}
    if username is not None:
        data = wiki_cv_helper_function(username)
        DataCache.update_or_create_object(username, data)
        WikipediaGeneralDataCache\
            .update_or_create_object(data['contribution_distribution'])

        results['result'] = True

    return JsonResponse(results)


# View for loading graphs for the user
def load_graphs(request):
    username = request.GET.get('username')
    time_filter = request.GET.get('filter')
    filters_time_dict = evaluate_time_filters()
    graphs_object = GraphsModule()

    # In case view is called independently, then it
    # needs to evaluate other data as well
    if DataCache.objects.filter(username=username).count() == 0:
        data = wiki_cv_helper_function(username)
        DataCache.create_object(username, data)

    cached_data = DataCache.objects.get(username=username)
    graphs_object.graphs_starter_function(cached_data
                                          .contribution_content['edits_array'],
                                          cached_data
                                          .contribution_content[
                                              'articles_created_array'],
                                          cached_data.page_to_project_mapping,
                                          filters_time_dict[time_filter])

    return JsonResponse({'spread_over_projects_data':
                        graphs_object.spread_over_projects_data,
                         'edits_activity_chart_data':
                        graphs_object.edits_activity_chart_data,
                         'created_activity_chart_data':
                        graphs_object.created_activity_chart_data})
