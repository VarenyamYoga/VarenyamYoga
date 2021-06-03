from django.contrib import admin
from .models import Assessment_Model
from .question_models import Question_DB
from .questionpaper_models import Question_Paper
admin.site.register(Question_DB)
admin.site.register(Question_Paper)
#admin.site.register(Special_Students)
admin.site.register(Assessment_Model)