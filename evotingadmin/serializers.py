from django.contrib.auth.models import User
from evotingapp.models import Vote
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='Contestant.name')
    class Meta:
        model = Vote
        fields = '__all__'