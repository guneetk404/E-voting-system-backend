from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from evotingadmin.serializers import UserSerializer, VoteSerializer
from evotingapp.models import Vote, Contest, Contestant, Voter
from evotingapp.serializers import ContestSerializer, VoterSerializer
from django.contrib.auth import authenticate
from django.db.models import Sum
# Create your views here.


class VoterHandle(APIView):
    def post(self, request):
        try:
            print(request.data)
            request.data['password'] = 'Abcd1234@#'
            request.data['email'] = request.data['Email']
            request.data['first_name'] = request.data['Name']
            request.data['last_name'] = request.data['FatherName']
            request.data['password2'] = request.data['password']
            request.data['is_voter'] = True
            user = CustomUserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                user = CustomUser.objects.get(email=request.data['Email'])
                request.data['User'] = user.id
                extradata = VoterSerializer(data=request.data)
                if extradata.is_valid():
                    extradata.save()
                    return Response({'message': 'Voter Created'}, status=200)
                return Response(extradata.errors, status=400)
            return Response(user.errors, status=400)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=400)

# using to search the voter ~~but not suggested you can use new endpoint for this
    def patch(self, request):
        try:
            data = Voter.objects.get(Aadhaar=request.data['Aadhaar'])
            dataserializer = VoterSerializer(data)
            return Response(dataserializer.data, status=200)
        except Exception as e:
            return Response({'error': 'Voter not found'}, status=400)

    def put(self, request):
        try:
            getuser = CustomUser.objects.filter(email=request.data['Email']).first()
            getextradata = Voter.objects.get(User=getuser)
            extradata = VoterSerializer(getextradata,data=request.data,partial=True)
            if extradata.is_valid():
                extradata.save()
                return Response({'message': 'Voter Updated'}, status=200)
            return Response(extradata.errors, status=400)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=400)

class DeleteVoterHandle(APIView):
    def post(self,request):
        try:
            CustomUser.objects.filter(email=request.data['Email'],is_voter=True).delete()
            return Response({'message': 'Voter Deleted'}, status=200)
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=400)