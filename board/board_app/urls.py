from django.urls import path
from .views import PostDetail, PostCreate, PostsList, PostResponse, PostResponses, ResponseDelete, MyPosts, \
   accept_response, PostUpdate, PostDelete


urlpatterns = [
   path('', (PostsList.as_view()), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/response/', PostResponse.as_view(), name='post_response'),
   path('profile/', MyPosts.as_view(), name='my_posts'),
   path('profile/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('profile/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('profile/<int:post_id>', PostResponses.as_view(), name='post_responses'),
   path('<int:pk>/delete', ResponseDelete.as_view(), name='unresponse'),
   path('<int:pk>/accept', accept_response, name='accept'),



]
