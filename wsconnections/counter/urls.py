from django.urls import path
from counter.views import CountersWrapperView, CountView

urlpatterns = [
    path('count/', CountersWrapperView.as_view()),
    path('count/<slug:room_name>/', CountView.as_view()),
]