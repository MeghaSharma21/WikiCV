import json
import dateutil.parser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from user_summary.helper_functions.wiki_cv_helper \
    import wiki_cv_helper_function, \
    impact_graph_helper_function
from user_summary.models import DataCache, UserData, \
    WikipediaGeneralDataCache, PageAttributesTable
from user_summary.modules.graphs_module import GraphsModule
from user_summary.modules.profile_module import ProfileModule
from user_summary.utility import evaluate_time_filters, \
    convert_page_attribute_table_objects_to_lists, check_user_exists
import user_summary.constants as constants
from user_summary.modules.pinned_repository_module \
    import PinnedRepositoryModule


# View that corresponds to the main page of WikiCV
def wiki_cv(request, username):
    message = ''
    data = {}
    error = False
    is_logged_in = False
    # If user is authenticated and wants to see
    # own profile, automatically username will be assigned
    if username is None and request.user.is_authenticated:
        username = request.user
        is_logged_in = True

    if username is not None and check_user_exists(username) is True:
        if DataCache.objects.filter(username=username).count() == 0:
            data = wiki_cv_helper_function(username)
            DataCache.create_object(username, data)
            # If data for user is not already stored, then data for
            # the contributed pages won't also be there
            impact_graph_helper_function(data)
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

        # Fetch data for pinned repositories section
        data['pinned_repositories'] = \
            PinnedRepositoryModule().get_repositories(username)
        data['profile_data'] = ProfileModule().get_profile_data(username)

        # Converting first and last contribution timestamps into datetime
        # objects so that they can be parsed in the template
        data['summary_content']['firstContributionTimestamp'] = \
            dateutil.parser.parse(data['summary_content']
                                  ['firstContributionTimestamp'])
        data['summary_content']['lastContributionTimestamp'] = \
            dateutil.parser.parse(data['summary_content']
                                  ['lastContributionTimestamp'])

    # If user is neither authenticated nor has provided any name in the URL
    else:
        message = "CV could not be loaded properly"
        error = True

    return render(request, 'user_summary/profile.html',
                  {'data': data, 'message': message,
                   'is_logged_in': is_logged_in, 'error': error})


# View that updates the cached data for the user
def update_cached_data(request, username):
    results = {'result': False}
    if username is not None:
        data = wiki_cv_helper_function(username)
        DataCache.update_or_create_object(username, data)
        WikipediaGeneralDataCache\
            .update_or_create_object(data['contribution_distribution'])
        # To store data in PageAttributeTable
        impact_graph_helper_function(data)
        results['result'] = True

    return JsonResponse(results)


# View for loading graphs for the user
def load_graphs(request):
    username = request.GET.get('username')
    time_filter = request.GET.get('filter')
    time_filter_type = request.GET.get('time_filter_type')
    graphs_object = GraphsModule()

    # In case view is called independently, then it
    # needs to evaluate other data as well
    if DataCache.objects.filter(username=username).count() == 0:
        data = wiki_cv_helper_function(username)
        DataCache.create_object(username, data)
        # If data for user is not already stored, then data for
        # the contributed pages won't also be there
        impact_graph_helper_function(data)

    cached_data = DataCache.objects.get(username=username)

    # If only year filter has been clicked
    if time_filter_type == 'year':
        page_attributes_objects = \
            PageAttributesTable.objects\
            .filter(pk__in=cached_data.summary_content['pages_contributed'])
        page_attributes_data = \
            convert_page_attribute_table_objects_to_lists(
                page_attributes_objects)
        impact_graphs_data = graphs_object\
            .make_impact_graph(int(time_filter),
                               cached_data
                               .summary_content['user_contribution'
                                                '_based_on_time'],
                               page_attributes_data['total_contribution'
                                                    '_by_all_in_pages_dict'],
                               page_attributes_data['page_views_dict'],
                               cached_data
                               .summary_content['pages_contributed'])
        return JsonResponse({"impact_graphs_data": impact_graphs_data})

    else:
        filters_time_dict = evaluate_time_filters()
        graphs_object.graphs_starter_function(cached_data
                                              .contribution_content[
                                                  'edits_array'],
                                              cached_data
                                              .contribution_content[
                                                  'articles_created_array'],
                                              cached_data
                                              .page_to_project_mapping,
                                              filters_time_dict[
                                                  time_filter])

        return JsonResponse({'spread_over_projects_data':
                            graphs_object.spread_over_projects_data,
                             'edits_activity_chart_data':
                            graphs_object.edits_activity_chart_data,
                             'created_activity_chart_data':
                            graphs_object.created_activity_chart_data})


# View that corresponds to editing the profile by logged-in user
@login_required()
def edit_profile(request, username):
    if request.is_ajax():
        input_dict = {'full_name': request.POST.get('full_name'),
                      'languages': request.POST.get('languages'),
                      'tools': request.POST.get('tools'),
                      'introduction': request.POST.get('introduction'),
                      'location': request.POST.get('location'),
                      'job_designation': request.POST.get('job_designation'),
                      'website': request.POST.get('website'),
                      'blog': request.POST.get('blog'),
                      'github': request.POST.get('github'),
                      'linkedin': request.POST.get('linkedin'),
                      'facebook': request.POST.get('facebook'),
                      'twitter': request.POST.get('twitter'),
                      'pinned_repositories':
                          json.loads(request.POST
                                     .get('pinned_repositories'))}

        response = PinnedRepositoryModule()\
            .format_input_repositories(username, input_dict)
        if response['error_message'] is not '':
            return JsonResponse({'error': 1,
                                 'error_message': response['error_message']})

        UserData.update_or_create_object(username, input_dict)

    return JsonResponse({'error': 0})
