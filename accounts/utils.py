from accounts.models import OtpModel
from rest_framework_simplejwt.tokens import RefreshToken


class Util:

    @staticmethod
    def generate_password(user):
        import random
        import string
        chars = string.digits
        otp = ''.join(random.choice(chars) for _ in range(6))
        alreadydata = OtpModel.objects.filter(user=user).first()
        if alreadydata:
            alreadydata.otp = otp
            alreadydata.save()
            return otp
        otpdata = OtpModel.objects.create(otp=otp, user=user)
        otpdata.save()
        return otp

    @staticmethod
    def send_otp(request, user):
        # from twilio.rest import Client
        # account_sid = "ACac3b49a332e62ac597316b7735b85a09"
        # auth_token = "da28c7a671b039cfc71f99a58449f5ec"
        # client = Client(account_sid, auth_token)
        otp = Util.generate_password(user)
        # client.messages.create(
        #     to=f"+91{request.data['Mobile']}",
        #     from_="+17692273018",
        #     body=f"Hello your otp is {otp}"
        # )
