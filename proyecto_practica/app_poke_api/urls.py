from django.urls import path
from . import views
from .views import ApiView

urlpatterns =[
    path('api/v1/players/',ApiView.as_view(),name='players_list'),
    path('api/v1/players/<int:id>',ApiView.as_view(),name='players_id'),
    path('',views.index,name='index'),
    path('pokemon/',views.pokemon,name='pokemon'),
]