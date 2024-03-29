# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='default'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('home/', views.home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('submit/', views.submit_view, name='submit'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

    path('story_submission/', views.story_submission_view, name='story_submission'),
    path('story/<slug:story_name_slug>/',
         views.story_view, name='story'),
    path('comment/<str:story_title>/', views.comment_view, name='comment'),
]

