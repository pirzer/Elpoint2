from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('user_posts/', views.UserPosts.as_view(), name='user_posts'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    # path('update/<slug:slug>', views.UpdatePost.as_view(), name='update'),
    # path('delete/<slug:slug>', views.DeletePost.as_view(), name='delete'),
    path('tag_list/<tag>/', views.TagList.as_view(), name="tag_list"),
]