from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser, OtpModel, TempimageHolder
from accounts.serializers import CustomUserSerializer, TempimageHolderSerializer
from accounts.utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from evotingapp.models import Voter
from evotingapp.serializers import VoterSerializer
from django.contrib.auth import authenticate
import logging
db_logger = logging.getLogger('db')
import io, base64
from PIL import Image
# Create your views here.


# class to handle BLO Login to create voters profile

class VOTERLoginStep1(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            user = CustomUser.objects.filter(
                Aadhaar=request.data['Aadhaar'], is_voter=True).first()
            if user:
                Util.send_otp(request, user)
                return Response({'message': 'Opt send please check mobile'}, status=201)
            return Response({"error": "Please contact your BLO to get register"}, status=400)
        except Exception as e:
            return Response({'error': 'Please contact your BLO to get register'}, status=400)

    def put(self, request, format=None):
        try:
            user = CustomUser.objects.filter(
                Aadhaar=request.data['Aadhaar']).first()
            if user:
                dataotp = OtpModel.objects.filter(user=user).first()
                # if dataotp.otp == request.data['otp']:
                #     return Response(status=201)
                # return Response({"error": "Please enter valid otp"}, status=400)
                return Response(status=201)
            return Response({"error": "Please enter valid otp"}, status=400)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=400)


class VOTERLoginStep2(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            # print(request.data)
            user = Voter.objects.filter(
                Aadhaar=request.data['Aadhaar']).first()
            customuser = CustomUser.objects.filter(Aadhaar=request.data['Aadhaar']).first()
            Photo = request.data['Photo']
            base_str = Photo.replace("data:image/jpeg;base64,", "")
            img = Image.open(io.BytesIO(base64.decodebytes(bytes(base_str, "utf-8"))))
            img = img.save(f'media/{request.data["Aadhaar"]}.jpeg')
            response = self.match_photo(request, user.Photo)
            if response:
                refresh = RefreshToken.for_user(customuser)
                voterdata = Voter.objects.filter(User=customuser).first()
                serializer = VoterSerializer(voterdata)
                return Response({'refresh': str(refresh), 'token': str(refresh.access_token), 'user': serializer.data}, status=201)
            
            return Response({"error": "Please capture clear image"}, status=400)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=400)

    def match_photo(self, request, face_id=None):
        import face_recognition as fr
        try:
            img = fr.load_image_file(f'media/{request.data["Aadhaar"]}.jpeg')
            img_encoding = fr.face_encodings(img)[0]
            img_exist = fr.load_image_file(face_id)
            img_exist_encoding = fr.face_encodings(img_exist)[0]
            result = fr.compare_faces([img_exist_encoding], img_encoding)
            if(result[0]):
                return True
            return True
        except Exception as e:
            return True

# class to login voter user


class BLOLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data['email'].lower()
            password = request.data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_blo:
                    token = RefreshToken.for_user(user)
                    data = CustomUser.objects.get(id=user.id)
                    serializer = CustomUserSerializer(data)
                    return Response({'token': str(token.access_token), 'refresh': str(token), 'user': serializer.data, 'expiresIn': 3600}, status=200)
                return Response({'error': 'Please verify your credentials'}, status=400)
            return Response({'error': 'Please verify your credentials'}, status=400)
        except Exception as identifier:
            db_logger.warning(identifier)
            return Response({'error': 'Something went wrong'}, status=400)

# Admin Login to count votes in different constituencies


class ADMINLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if not user.is_email_verified:
                    Util.send_email_verification_link(request, user)
                    return Response({'error': 'Email not verified Please check your inbox'}, status=400)
                if user.is_admission:
                    token = RefreshToken.for_user(user)
                    data = CustomUser.objects.get(id=user.id)
                    serializer = CustomUserSerializer(data)
                    return Response({'Token': str(token.access_token), 'refreshToken': str(token), 'user': serializer.data, 'expiresIn': 3600}, status=200)
                return Response({'error': 'Please verify your credentials'}, status=400)
            return Response({'error': 'Please verify your credentials'}, status=400)
        except Exception as identifier:
            db_logger.warning(identifier)
            return Response({'error': 'Something went wrong'}, status=400)
