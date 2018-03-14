from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.add_book),
    url(r'^books/add/save$', views.save_book),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^books/(?P<id>\d+)/add_review$', views.add_review),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    url(r'^books/(?P<book_id>\d+)/delete/(?P<review_id>\d+)$', views.delete_review)
]
