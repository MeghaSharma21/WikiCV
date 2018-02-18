from django.conf.urls import url, include
from user_summary import views

urlpatterns = [
    url(r'^profile$', views.profile, name='profile'),
    url(r'^accounts/login$', views.login_oauth, name='login'),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    url(r'^$', views.index),
    # Regex handles the case when username is not present in the username
    url(r'^wiki-cv(?:/(?P<username>\w+))?/$', views.wiki_cv, name='wiki_cv'),
    url(r'^update-cached-data(?:/(?P<username>\w+))?/$',
        views.update_cached_data, name='update_cached_data'),
    url(r'^load-graphs/$', views.load_graphs, name='load_graphs'),
    url(r'^edit-profile(?:/(?P<username>\w+))?/$',
        views.edit_profile, name='edit_profile')
]
