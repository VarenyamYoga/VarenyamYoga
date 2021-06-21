from django.db import models
from django.contrib.auth.models import User
from questions.question_models import Question_DB
from questions.questionpaper_models import Question_Paper

class ClientInfo(models.Model):
    Name = models.CharField(max_length=15, blank=True)
    DOB = models.CharField(max_length=50, blank=True)
    BloodGroup = models.CharField(max_length=50, blank=True)
    Height = models.CharField(max_length=50, blank=True)
    Weight = models.CharField(max_length=50, blank=True)
    waist = models.CharField(max_length=50, blank=True)
    Heap = models.CharField(max_length=50, blank=True)
    Diseases = models.CharField(max_length=50, blank=True)
    Company = models.CharField(max_length=50, blank=True)
    Designation = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to = 'Client_profile_pics', blank=True)
    '''
    def __str__(self):
        return self.user.username   
    '''
    class Meta:
        verbose_name_plural = 'Client Info'

class Client_Question(Question_DB):
    Trainer = None
    Client = models.ForeignKey(User, limit_choices_to={'groups__name': "Client"}, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="E")

    def __str__(self):
        return str(self.Client.username) + " "+ str(self.qno) +"-Client_QuestionDB"


class ClientExam_DB(models.Model):
    Client = models.ForeignKey(User, limit_choices_to={'groups__name': "Client"}, on_delete=models.CASCADE, null=True)
    Assessmentname = models.CharField(max_length=100)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Client_Question)
    score = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Client.username) +" " + str(self.Assessmentname) + " " + str(self.qpaper.qPaperTitle) + "-ClientExam_DB"


class ClientResults_DB(models.Model):
    Client = models.ForeignKey(User, limit_choices_to={'groups__name': "Client"}, on_delete=models.CASCADE, null=True)
    Assessment = models.ManyToManyField(ClientExam_DB)

    def __str__(self):
        return str(self.Client.username) +" -ClientResults_DB"