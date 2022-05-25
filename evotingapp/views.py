from unittest import result
from rest_framework.views import APIView
from rest_framework.response import Response
from evotingapp.models import Contest, Contestant, Vote, Voter
from evotingapp.serializers import ContestSerializer, ContestantSerializer, VoterSerializer
from django.db.models import Sum


class getVoting(APIView):

    def post(self, request, format=None):
        try:
            contestid = request.data['contestid']
            contest = Contest.objects.filter(id=contestid,status=True).first()
            if not contest:
                return Response({'error': "Voting over"}, status=401)
            voter = Voter.objects.get(User=request.user)
            contestents = Contestant.objects.filter(contestno=contestid, city=voter.City, status=True)
            voted = Vote.objects.filter(Voter=voter, Contest=contestid).first()
            if voted:
                return Response({'error': "You have already voted"}, status=400)
            if contestents:
                serializer = ContestantSerializer(contestents, many=True)
                return Response(serializer.data, status=200)
            return Response({'error': "No Candidate to vote"}, status=400)
        except Exception as e:
            return Response({'error': "Contest Not found"}, status=400)


class castVote(APIView):
    def post(self, request, format=None):
        try:
            contestid = request.data['contestno']
            voter = Voter.objects.filter(User=request.user).first()
            contest = Contest.objects.filter(id=contestid,status=True).first()
            if not contest:
                return Response({'error': "Voting over"}, status=401)
            vote_check = Vote.objects.filter(Voter=voter, Contest=contestid).first()
            if vote_check:
                return Response({'error': "You have already voted"}, status=400)
            points = 1
            contestid = Contest.objects.filter(
                id=request.data['contestno']).first()
            contestant = Contestant.objects.filter(
                id=request.data['id']).first()
            savevote = Vote(Voter=voter, Contestant=contestant,
                            Contest=contestid, Points=points)
            savevote.save()
            return Response({'success': "Vote Casted"}, status=200)
        except Exception as e:
            return Response({'error': "Something went wrong please try again"}, status=400)


class getElections(APIView):
    def post(self, request, format=None):
        try:
            contest = Contest.objects.filter(status=True)
            serializer = ContestSerializer(contest, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': "No Elections Live"}, status=400)

class getElectionResultlist(APIView):
    def get(self,request,format=None):
        try:
            contest = Contest.objects.filter(result=True)
            serializer = ContestSerializer(contest, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': "No Elections Live"}, status=400)
     
    def post(self, request, format=None):
        try:
            print(request.data)
            contestant = Contestant.objects.filter(contestno=request.data['id'])
            data = Vote.objects.filter(Contestant__in=contestant).values('Contestant__name').annotate(total=Sum('Points'))
            return Response(data, status=200)
        except Exception as identifier:
            return Response({'error': 'Something went wrong'}, status=400)

            