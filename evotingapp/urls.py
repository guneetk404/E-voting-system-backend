from django.urls import path
from evotingapp import views

urlpatterns = [
    path('getcontestant/',views.getVoting.as_view(),name='getVoting'),
    path('castvote/',views.castVote.as_view(),name='castvote'),
    path('getelections/',views.getElections.as_view(),name='getElections'),
    path('getelectionresultlist/',views.getElectionResultlist.as_view(),name='getElections'),
]
