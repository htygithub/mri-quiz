from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from quiz.views import QuizView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mriquiz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', QuizView.as_view(), name='quiz_view')
)
