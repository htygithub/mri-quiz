from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from quiz.views import QuizView, MRIQuizView, RestartView, IndexView

urlpatterns = []

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        })
    )

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'mriquiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^restart/', RestartView.as_view(), name="restart"),
    url(r'^quiz/(?P<quiz>[-\w]+)/?$', QuizView.as_view(), name='quiz_view'),
    url(r'^mri-quiz/?$', MRIQuizView.as_view(), name="mri_quiz_view"),
    url(r'^$', IndexView.as_view(), name="home")
)
