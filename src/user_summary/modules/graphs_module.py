import logging
from collections import defaultdict
from user_summary.helper_functions.calculate_users_contribution_distribution \
    import calculate_users_contribution_distribution
from user_summary.helper_functions.user_information \
    import calculateUserContributionRank
import user_summary.constants as constants
from user_summary.utility import convert_string_to_datetime


# Module corresponding to Graphs section in the tool
class GraphsModule:
    logger = logging.getLogger('django')
    spread_over_projects_data = []
    edits_activity_chart_data = defaultdict(int)
    created_activity_chart_data = defaultdict(int)

    # Starter function for Graphs Module
    def graphs_starter_function(self, edits_array, articles_created_array,
                                page_to_project_mapping,
                                time_filter):
        if page_to_project_mapping != -1:
            self.make_spread_over_projects_graph(edits_array,
                                                 page_to_project_mapping,
                                                 time_filter)
        self.make_activity_graph(edits_array, articles_created_array,
                                 time_filter)

    # Function contains the code for 'spread over projects' graph
    def make_spread_over_projects_graph(self, edits_array,
                                        page_to_project_mapping,
                                        time_filter):
        data = defaultdict(int)
        for edit in edits_array:
            timestamp = convert_string_to_datetime(str(edit['timestamp']))
            if timestamp >= time_filter:
                if str(edit['pageid']) in page_to_project_mapping:
                    for project in page_to_project_mapping[str(edit
                                                               ['pageid'])]:
                        data[str(project)] = data[str(project)] +\
                                             abs(edit['sizediff'])
                else:
                    data['Not assigned'] = data['Not assigned'] +\
                                           abs(edit['sizediff'])
        self.spread_over_projects_data = \
            [['Project', 'Percentage of Bytes Added']]
        for key, value in data.items():
            self.spread_over_projects_data.append([key, data[key]])

    # Function contains the code for 'activity chart'
    def make_activity_graph(self, edits_array, articles_created_array,
                            time_filter):

        self.edits_activity_chart_data = \
            self.__activity_graph_helper(edits_array, time_filter)
        self.logger.info("Data for articles edited activity chart:" +
                         str(self.edits_activity_chart_data))

        self.created_activity_chart_data = \
            self.__activity_graph_helper(articles_created_array, time_filter)
        self.logger.info("Data for articles created activity chart:" +
                         str(self.created_activity_chart_data))

    # This private helper function prepares a timestamp to
    # contribution mapping for the user
    def __activity_graph_helper(self, contribution_array, time_filter):
        data = defaultdict(int)
        for contribution in contribution_array:
            timestamp = \
                convert_string_to_datetime(str(contribution['timestamp']))
            if timestamp >= time_filter:
                data[str(timestamp.date())] = \
                    data[str(timestamp.date())] + 1
        return data

    # Function corresponds to User Ranking graph
    @staticmethod
    def make_user_ranking_graph(username):
        success = True
        message = 'Data for user ranking graph ' \
                  'fetched successfully.'
        groups = constants.CONTRIBUTION_BUCKETS
        user_contribution_info = calculateUserContributionRank(username)
        data = calculate_users_contribution_distribution()
        user_group = -1
        user_percentile = -1
        if user_contribution_info['user_rank'] == -1 or \
                data['success'] is False:
            success = False
            message = 'Error occurred while fetching data for ' \
                      'user ranking graph.'
        else:
            # checking which group user with given username belongs to
            user_group = 1
            for i in range(len(groups)):
                if groups[i][0] <= \
                        user_contribution_info['complete_edit_count'] <= \
                        groups[i][1]:
                    user_group = i + 1
                    break

            # calculating percentile of the user
            user_percentile = 100 - 100 * round(
                user_contribution_info['user_rank'] /
                data['total_no_of_users'], 4)
        GraphsModule.logger.info(message)
        return {'success': success,
                'percentage_of_users_in_group': data[
                    'percentage_of_users_in_group'],
                'total_no_of_users': data['total_no_of_users'],
                'user_rank': user_contribution_info['user_rank'],
                'user_group': user_group,
                'user_complete_edit_count':
                    user_contribution_info['complete_edit_count'],
                'user_percentile': user_percentile}

    # Function corresponds to Impact graph
    @staticmethod
    def make_impact_graph(year_filter, user_contribution_based_on_time,
                          total_contribution_by_all_users,
                          page_views_dict, pages_list):
        impact = {}
        for month in range(0, 12):
            impact[month] = {}
            for page in pages_list:
                if str(page) in \
                        user_contribution_based_on_time[
                            str(year_filter)][str(month)]\
                        and total_contribution_by_all_users[str(page)] != 0:
                    # Multiplication by 100 as the values otherwise
                    # were very small
                    page_impact = 100 * \
                                  (page_views_dict[str(page)] /
                                   total_contribution_by_all_users[
                                       str(page)]) * \
                                  user_contribution_based_on_time[
                                      str(year_filter)][str(month)][str(page)]
                    # To avoid unnecessary transfer of data which
                    # equates to zero
                    if page_impact != 0:
                        impact[month][page] = round(page_impact, 4)
        GraphsModule.logger.info("Data for impact graph for user is:{0}"
                                 .format(str(impact)))
        return impact
