from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    #http://127.0.0.1:8000/
    path('', views.home, name='home'),

    #http://127.0.0.1:8000/sign_in/
    path('sign_in/', views.sign_in, name='sign_in'),

    #http://127.0.0.1:8000/sign_up/
    path('sign_up/', views.sign_up, name='sign_up'),

    #http://127.0.0.1:8000/sign_out/
    path('sign_out/', views.sign_out, name='sign_out'),

    #http://127.0.0.1:8000/exercises/
    path('exercises/', views.exercises, name='exercises'),

    #http://127.0.0.1:8000/exercises/1
    path('exercises/<int:exercise_id>/', views.exercise, name='exercise'),

    #http://127.0.0.1:8000/exams/
    path('exams/', views.exams, name='exams'),

    #http://127.0.0.1:8000/exams/1
    path('exams/<int:exam_id>/', views.exam, name='exam'), 

    #http://127.0.0.1:8000/resources/
    path('resources/', views.resources, name='resources'), 

    #http://127.0.0.1:8000/download/1 #Not for users
    path('download/<int:resource_id>', views.download, name='download'), 

    #http://127.0.0.1:8000/profile/user_1/
    path('profile/<user_username>/', views.profile, name='profile'),

    #http://127.0.0.1:8000/feed/
    path('feed/', views.feed, name='feed'),

    #http://127.0.0.1:8000/feed/post/1/
    path('feed/post/<int:id>/', views.post, name='post'),

    #http://127.0.0.1:8000/delete/1/ #Not for users
    path('delete/<int:post_id>/', views.delete, name='delete'),

    #http://127.0.0.1:8000/like/1 #Not for users
    path('like/<int:post_id>/', views.like, name='like'),

    #http://127.0.0.1:8000/dislike/1 #Not for users
    path('dislike/<int:post_id>/', views.dislike, name='dislike'),

    #http://127.0.0.1:8000/select/1 #Not for users
    path('select/<int:reply_id>/<int:post_id>/', views.select, name='select'),

    #http://127.0.0.1:8000/select_avatar/1/ #Not for users
    path('select_avatar/<int:avatar_order>/', views.selectAvatar, name='select_avatar'),

    #http://127.0.0.1:8000/feed/search/?q=The+rough+serpant
    path('feed/search/', views.search, name='search'),

    #http://127.0.0.1:8000/forgot/
    path('forgot/', views.forgot, name='forgot'),

    #http://127.0.0.1:8000/about/
    path('about/', views.about, name='about'),

    #http://127.0.0.1:8000/contact_us/
    path('contact_us/', views.contact_us, name='contact_us'),

    #http://127.0.0.1:8000/use_conditions/
    path('use_conditions/', views.use_conditions, name='use_conditions'),

    #http://127.0.0.1:8000/report_bug/
    path('report_bug/', views.report_bug, name='report_bug'),

    #http://127.0.0.1:8000/donation/
    path('donation/', views.donation, name='donation'),
    
]