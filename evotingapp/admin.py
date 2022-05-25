from django.contrib import admin
from evotingapp.models import Vote,Voter,Contest,Contestant

# Register your models here.
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Contest)
admin.site.register(Contestant)
