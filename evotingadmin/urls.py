from django.urls import path
from evotingadmin import views

urlpatterns = [
    path('createvoter/',views.VoterHandle.as_view(),name='VoterHandle'),
    path('deletevoter/',views.DeleteVoterHandle.as_view(),name='VoterHandle'),
]
