import logging
from user_summary.utility import fetch_data_from_mediawiki_api


# Contains data and functions related to the achievements section of WikiCV
class AchievementsModule:

    logger = logging.getLogger('django')
    achievements = []
    contribution_threshold = 15

    # Starter function for calculating achievements
    def calculate_achievements(self, username, user_authorship_mapping):
        page_ids = []
        message = 'Achievements calculated successfully for user:' \
                  + username + '. Achievements are:'
        for key, value in \
                user_authorship_mapping['percentageContribution'].items():
            if value >= self.contribution_threshold:
                page_ids.append(key)
        pageids_list = ' | '.join(str(page) for page in page_ids)

        parameters = {'action': 'query',
                      'format': 'json',
                      'prop': 'pageassessments',
                      'palimit': '1',
                      'pageids': pageids_list,
                      'formatversion': 2}
        while True:
            results = fetch_data_from_mediawiki_api(parameters)
            if not results['result']:
                message = ''
                break

            json_data = results['json_data']
            pages_assessment_results = json_data['query']['pages']
            self.achievements = self.achievements + self.parse_assessment_data(
                pages_assessment_results, user_authorship_mapping)

            if 'continue' in json_data:
                parameters['pacontinue'] = \
                    json_data['continue']['pacontinue']
                parameters['continue'] = \
                    json_data['continue']['continue']
            else:
                break

        # sorting achievements by percentage contribution in respective pages
        self.achievements = sorted(self.achievements,
                                   key=lambda k: k['percentage_contribution'],
                                   reverse=True)
        self.logger.info(message + str(self.achievements))
        if not results['result']:
            return -1
        else:
            return 1

    # Retrieves the relevant data obtained from the API call
    def parse_assessment_data(self, pages_assessment_results,
                              user_authorship_mapping):
        achievements = []
        for assessment_result in pages_assessment_results:
            data = {'page_id': assessment_result.get('pageid'),
                    'title': assessment_result.get('title'),
                    'achievement_description':
                        'User has contributed to the following projects: ',
                    'percentage_contribution':
                        user_authorship_mapping['percentageContribution']
                        [str(assessment_result.get('pageid'))]}
            FA_count = 0
            A_count = 0
            GA_count = 0
            if assessment_result.get('pageassessments'):
                for key, value in assessment_result.get('pageassessments') \
                        .items():
                    data['achievement_description'] = \
                        data['achievement_description'] + str(key)
                    if value.get('class'):
                        data['achievement_description'] = \
                            data['achievement_description'] + \
                            ' (' + value.get('class') + '), '
                    if value['class'] == 'FA':
                        FA_count = FA_count + 1
                    else:
                        if value['class'] == 'A':
                            A_count = A_count + 1
                        else:
                            if value['class'] == 'GA':
                                GA_count = GA_count + 1

                if FA_count > 0:
                    data['type'] = 'FA'
                else:
                    if A_count > 0:
                        data['type'] = 'A'
                    else:
                        if GA_count > 0:
                            data['type'] = 'GA'
                        else:
                            continue
                if data['achievement_description'].endswith(', '):
                    data['achievement_description'] = \
                        data['achievement_description'][:-2]
                achievements.append(data)
        return achievements
