from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^process/$', views.user_process, name="process"),
    url(r'^registered/$', views.registered, name="registered"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^add_item/$', views.add_item, name="add_item"),
    url(r'^adding/$', views.adding, name="adding"),
    url(r'^remove/(?P<id>\w+)$', views.remove, name="remove"),
    url(r'^delete/(?P<id>\w+)$', views.destroy, name="delete"),
    url(r'^show/(?P<item_id>\d+)$', views.wish_items, name="wishitem"),
    url(r'^wish/(?P<item_id>\d+)$', views.wish, name="wish"),
    url(r'^logout$', views.logout)
]
# (?P<user_id>\w+)