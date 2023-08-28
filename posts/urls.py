from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path('', views.index, name='index' ),
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>', views.PostDetails, name='postdetails'),
    path('tag/<slug:tag_slug>', views.Tags, name='tags'),
    path('<uuid:post_id>/like>', views.like, name='postlike'),
    path('<uuid:post_id>/favorite', views.favorite, name='postfavorite'),
]

