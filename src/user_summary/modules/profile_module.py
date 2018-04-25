import logging
from collections import defaultdict
from user_summary.models import UserData


class ProfileModule:
    logger = logging.getLogger('django')
    profile_data = defaultdict(int)

    # Function to fetch stored pinned repositories of the user
    def get_profile_data(self, username):
        message = 'Profile data successfully ' \
                  'fetched for user ' + str(username)
        data = defaultdict(int)
        if UserData.objects.filter(username=username).count() == 0:
            message = 'Data for user ' + str(username) + \
                      ' does not exist'
        else:
            data = UserData.objects.get(username=username)
            self.profile_data = {'introduction': data.introduction,
                                 'full_name': data.full_name,
                                 'job_designation': data.job_designation,
                                 'location': data.location,
                                 'languages': data.languages,
                                 'tools': data.tools,
                                 'website': data.website,
                                 'blog': data.blog,
                                 'github': data.github,
                                 'linkedin': data.linkedin,
                                 'facebook': data.facebook,
                                 'twitter': data.twitter
                                 }

        self.logger.info(message)
        return self.profile_data
