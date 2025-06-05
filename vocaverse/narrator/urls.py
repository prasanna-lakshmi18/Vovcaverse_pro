from django.urls import path
from .views import index, narrate_story

urlpatterns = [
    path('', index, name='index'),
    path('narrate/', narrate_story, name='narrate_story'),
]