from django.contrib import admin
from .models import *

admin.site.register(ClientInfo)
admin.site.register(Client_Question)
admin.site.register(ClientExam_DB)
admin.site.register(ClientResults_DB)