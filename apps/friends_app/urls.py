from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index, name="landing"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^friends$', views.dashboard, name="dashboard"),
    url(r'^users/(?P<id>\d+)$', views.show, name="show_user"),
    url(r'^add_favorite/(?P<id>\d+)$', views.favorite, name="favorite"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name="remove"),
]
