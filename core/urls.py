from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('movie/<str:pk>/', views.movie, name='movie'),
    path('genre/<str:pk>/', views.genre, name='genre'),
    path('search/', views.search, name='search'),
    path('my-list/', views.my_list, name='my-list'),
    path('my-list-json/', views.my_list_json, name='my-list-json'),
    path('add-to-list/', views.add_to_list, name='add-to-list'),
    path('remove-from-list/', views.remove_from_list, name='remove-from-list'),
    path('custom-lists/', views.custom_lists, name='custom_lists'),
    path('custom-list-json/<int:list_id>/', views.custom_list_json, name='custom_list_json'),
    path('create-custom-list/', views.create_custom_list, name='create_custom_list'),
    path('update-custom-list/<int:list_id>/', views.update_custom_list, name='update_custom_list'),
    path('delete-custom-list/<int:list_id>/', views.delete_custom_list, name='delete_custom_list'),
    path('add-to-custom-list/', views.add_to_custom_list, name='add_to_custom_list'),
    path('remove-from-custom-list/', views.remove_from_custom_list, name='remove_from_custom_list'),
]
