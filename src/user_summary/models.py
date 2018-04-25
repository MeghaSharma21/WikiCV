from django.db import models
from jsonfield import JSONField
import user_summary.constants as constants


# Model for table that contains the cached data for every user
class DataCache(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    summary_content = JSONField()
    achievements_content = JSONField()
    contribution_content = JSONField()
    page_to_project_mapping = JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    # Method to create a new entry in the table
    @staticmethod
    def create_object(username, data):
        DataCache.objects.create(username=username,
                                 summary_content=data['summary_content'],
                                 achievements_content=data[
                                     'achievements_content'],
                                 contribution_content={
                                     'edits_array': data['edits_array'],
                                     'articles_created_array':
                                         data['articles_created_array']},
                                 page_to_project_mapping=data[
                                     'page_to_project_mapping'])

    # Method to update or create (in case it isn't present earlier)
    # an entry in the table
    @staticmethod
    def update_or_create_object(username, data):
        DataCache.objects.update_or_create(username=username, defaults={
            'summary_content':
                data['summary_content'],
            'achievements_content':
                data['achievements_content'],
            'contribution_content':
                {'edits_array': data['edits_array'],
                 'articles_created_array':
                     data['articles_created_array']},
            'page_to_project_mapping':
                data['page_to_project_mapping']})


# Model for table that contains general cached data of the app
class WikipediaGeneralDataCache(models.Model):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    contribution_distribution = JSONField()

    # Method to create a new entry in the table
    @staticmethod
    def create_object(contribution_distribution):
        WikipediaGeneralDataCache.objects\
            .create(id=constants.GENERAL_DATA_CACHE_DEFAULT_ID,
                    contribution_distribution=contribution_distribution)

    # Method to update or create (in case it isn't present earlier)
    # an entry in the table
    @staticmethod
    def update_or_create_object(contribution_distribution):
        WikipediaGeneralDataCache.objects\
            .update_or_create(id=constants.GENERAL_DATA_CACHE_DEFAULT_ID,
                              defaults={'contribution_distribution':
                                        contribution_distribution})


# Model for table that contains user's data
class UserData(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=100, blank=True)
    introduction = models.TextField(max_length=1000, blank=True)
    pinned_repositories = JSONField(null=True)
    job_designation = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    languages = models.CharField(max_length=100, blank=True)
    tools = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    blog = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to update or create (in case it isn't present earlier)
    # an entry in the table
    @staticmethod
    def update_or_create_object(username, data):
        UserData.objects\
            .update_or_create(
             username=username,
             defaults={'introduction': data['introduction'],
                       'full_name': data['full_name'],
                       'pinned_repositories':
                           data['pinned_repositories'],
                       'job_designation':
                           data['job_designation'],
                       'location': data['location'],
                       'languages': data['languages'],
                       'tools': data['tools'],
                       'website': data['website'],
                       'blog': data['blog'],
                       'github': data['github'],
                       'linkedin': data['linkedin'],
                       'facebook': data['facebook'],
                       'twitter': data['twitter']})


# Model for table that contains data related to Wikipedia pages
class PageAttributesTable(models.Model):
    page_id = models.CharField(max_length=50, primary_key=True)
    page_views = models.FloatField(default=0)
    total_contribution_by_all_users = models.FloatField(default=0)

    # Method to update or create (in case it isn't present earlier)
    # an entry in the table
    @staticmethod
    def update_or_create_object(page_ids, page_views_dict,
                                total_contribution_dict):
        for page_id in page_ids:
            PageAttributesTable.objects\
                .update_or_create(page_id=page_id,
                                  defaults={'page_views':
                                            page_views_dict[str(page_id)],
                                            'total_contribution_by_all_users':
                                                total_contribution_dict[
                                                    page_id]
                                            })
