from django.urls import path
from counter.views import CountView

urlpatterns = [
    path('count/<slug:room_name>/', CountView.as_view()),
]