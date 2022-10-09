from django.urls import path

from msg.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

]
