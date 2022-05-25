from rest_framework import serializers
from evotingapp.models import Vote,Voter,Contest,Contestant

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = '__all__'