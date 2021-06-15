from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group
from Client.models import *
from django.utils import timezone
from Client.models import ClientExam_DB,ClientResults_DB
from questions.questionpaper_models import QPForm
from questions.question_models import QForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@login_required(login_url='Corporate-login')
def view_Assessment_Trainer(request):
    Trainer = request.user
    Trainer_user = User.objects.get(username=Trainer)
    permissions = False
    if Trainer:
        permissions = has_group(Trainer,"Trainer")
    if permissions:
        new_Form = AssessmentForm(Trainer_user)
        if request.method == 'POST' and permissions:
            form = AssessmentForm(Trainer_user,request.POST)
            if form.is_valid():
                Assessment = form.save(commit=False)
                Assessment.Trainer = Trainer
                Assessment.save()
                form.save_m2m()
                return redirect('view_Assessment')

        Assessment = Assessment_Model.objects.filter(Trainer=Trainer)
        return render(request, 'Assessment/mainexam.html', {
            'Assessment': Assessment, 'Assessmentform': new_Form, 'Trainer': Trainer,
        })
    else:
        return redirect('view_Assessment_Client')

@login_required(login_url='Corporate-login')
def add_question_paper(request):
    Trainer = request.user
    Trainer_user = User.objects.get(username=Trainer)
    permissions = False
    if Trainer:
        permissions = has_group(Trainer,"Trainer")
    if permissions:
        new_Form = QPForm(Trainer_user)
        if request.method == 'POST' and permissions:
            form = QPForm(Trainer_user,request.POST)
            if form.is_valid():
                Assessment = form.save(commit=False)
                Assessment.Trainer = Trainer_user
                Assessment.save()
                form.save_m2m()
                return redirect('Corporate-add_question_paper')

        Assessment = Assessment_Model.objects.filter(Trainer=Trainer)
        return render(request, 'Assessment/addquestionpaper.html', {
            'Assessment': Assessment, 'Assessmentform': new_Form, 'Trainer': Trainer,
        })
    else:
        return redirect('view_Assessment_Client')

@login_required(login_url='Corporate-login')
def add_questions(request):
    Trainer = request.user
    Trainer_user = User.objects.get(username=Trainer)
    permissions = False
    if Trainer:
        permissions = has_group(Trainer,"Trainer")
    if permissions:
        new_Form = QForm()
        if request.method == 'POST' and permissions:
            form = QForm(request.POST)
            if form.is_valid():
                Assessment = form.save(commit=False)
                Assessment.Trainer = Trainer_user
                Assessment.save()
                form.save_m2m()
                return redirect('Corpoarte-addquestions')

        Assessment = Assessment_Model.objects.filter(Trainer=Trainer)
        return render(request, 'Assessment/addquestions.html', {
            'Assessment': Assessment, 'Assessmentform': new_Form, 'Trainer': Trainer,
        })
    else:
        return redirect('view_Assessment_Client')

@login_required(login_url='Corporate-login')
def view_previousAssessment_Trainer(request):
    Trainer = request.user
    Client = 0
    Assessment = Assessment_Model.objects.filter(Trainer=Trainer)
    return render(request, 'Assessment/previousexam.html', {
        'Assessment': Assessment,'Trainer': Trainer
    })

@login_required(login_url='login')
def Client_view_previous(request):
    Assessment = Assessment_Model.objects.all()
    list_of_completed = []
    list_un = []
    for Assessment in Assessment:
        if ClientExam_DB.objects.filter(Assessmentname=Assessment.name ,lient=request.user).exists():
            if ClientExam_DB.objects.get(Assessmentname=Assessment.name,Client=request.user).completed == 1:
                list_of_completed.append(Assessment)
        else:
            list_un.append(Assessment)

    return render(request,'Assessment/previousClient.html',{
        'Assessment':list_un,
        'completed':list_of_completed
    })

@login_required(login_url='Corporate-login')
def view_Client_Trainer(request):
    Client = User.objects.filter(groups__name = "Client")
    Client_name = []
    Client_completed = []
    count = 0
    dicts = {}
    Assessmentn = Assessment_Model.objects.filter(Trainer=request.user)
    for Client in Client:
        Client_name.append(Client.username)
        count = 0
        for Assessment in Assessmentn:
            if ClientExam_DB.objects.filter(Client=Client,Assessmentname=Assessment.name,completed=1).exists():
                count += 1
            else:
                count += 0
        Client_completed.append(count)
    i = 0
    for x in Client_name:
        dicts[x] = Client_completed[i]
        i+=1
    return render(request, 'Assessment/viewClient.html', {
        'Client':dicts
    })

@login_required(login_url='Corporate-login')
def view_results_Trainer(request):
    Client = User.objects.filter(groups__name = "Client")
    dicts = {}
    Trainer = request.user
    Trainer = User.objects.get(username=Trainer.username)
    Assessmentn = Assessment_Model.objects.filter(Trainer=Trainer)
    for Assessment in Assessmentn:
        if ClientExam_DB.objects.filter(Assessmentname=Assessment.name,completed=1).exists():
            Client_filter = ClientExam_DB.objects.filter(Assessmentname=Assessment.name,completed=1)
            for Client in Client_filter:
                key = str(Client.Client) + " " + str(Client.Assessmentname) + " " + str(Client.qpaper.qPaperTitle)
                dicts[key] = Client.score
    return render(request, 'Assessment/resultsClient.html', {
        'Client':dicts
    })

@login_required(login_url='login')
def view_Assessment_Client(request):
    Assessment = Assessment_Model.objects.all()
    list_of_completed = []
    list_un = []
    for Assessment in Assessment:
        if ClientExam_DB.objects.filter(Assessmentname=Assessment.name ,Client=request.user).exists():
            if ClientExam_DB.objects.get(Assessmentname=Assessment.name,Client=request.user).completed == 1:
                list_of_completed.append(Assessment)
        else:
            list_un.append(Assessment)

    return render(request,'Assessment/mainexamClient.html',{
        'Assessment':list_un,
        'completed':list_of_completed
    })

@login_required(login_url='login')
def view_Client_attendance(request):
    Assessment = Assessment_Model.objects.all()
    list_of_completed = []
    list_un = []
    for Assessment in Assessment:
        if ClientExam_DB.objects.filter(Assessmentname=Assessment.name ,Client=request.user).exists():
            if ClientExam_DB.objects.get(Assessmentname=Assessment.name,Client=request.user).completed == 1:
                list_of_completed.append(Assessment)
        else:
            list_un.append(Assessment)

    return render(request,'Assessment/attendance.html',{
        'Assessment':list_un,
        'completed':list_of_completed
    })

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    min += hour*60
    return "%02d:%02d" % (min, sec) 

@login_required(login_url='login')
def appear_Assessment(request,id):
    Client = request.user
    if request.method == 'GET':
        Assessment = Assessment_Model.objects.get(pk=id)
        time_delta = Assessment.end_time - Assessment.start_time
        time = convert(time_delta.seconds)
        time = time.split(":")
        mins = time[0]
        secs = time[1]
        context = {
            "Assessment":Assessment,
            "question_list":Assessment.question_paper.questions.all(),
            "secs":secs,
            "mins":mins
        }
        return render(request,'Assessment/giveExam.html',context)
    if request.method == 'POST' :
        Client = User.objects.get(username=request.user.username)
        paper = request.POST['paper']
        AssessmentMain = Assessment_Model.objects.get(name = paper)
        ClientAssessment = ClientExam_DB.objects.get_or_create(Assessmentname=paper, Client=Client,qpaper = AssessmentMain.question_paper)[0]
        
        qPaper = AssessmentMain.question_paper
        ClientAssessment.qpaper = qPaper
         
        qPaperQuestionsList = AssessmentMain.question_paper.questions.all()
        for ques in qPaperQuestionsList:
            Client_question = Client_question(Client=Client,question=ques.question, optionA=ques.optionA, optionB=ques.optionB,optionC=ques.optionC, optionD=ques.optionD,
            answer=ques.answer)
            Client_question.save()
            ClientAssessment.questions.add(Client_question)
            ClientAssessment.save()

        ClientAssessment.completed = 1
        ClientAssessment.save()
        AssessmentQuestionsList = ClientExam_DB.objects.filter(Client=request.user,Assessmentname=paper,qpaper=AssessmentMain.question_paper,questions__Client = request.user)[0]
        #examQuestionsList = ClientAssessment.questions.all()
        AssessmentScore = 0
        list_i = AssessmentMain.question_paper.questions.all()
        queslist = AssessmentQuestionsList.questions.all()
        i = 0
        for j in range(list_i.count()):
            ques = queslist[j]
            max_m = list_i[i].max_marks
            ans = request.POST.get(ques.question, False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            if ans.lower() == ques.answer.lower() or ans == ques.answer:
                AssessmentScore = AssessmentScore + max_m
            i+=1

        ClientAssessment.score = AssessmentScore
        ClientAssessment.save()
        Client = ClientExam_DB.objects.filter(Client=request.user,Assessmentname=AssessmentMain.name)  
        results = ClientResults_DB.objects.get_or_create(Client=request.user)[0]
        results.Assessment.add(Client[0])
        results.save()
        return redirect('view_Assessment_Client')

@login_required(login_url='login')
def result(request,id):
    Client = request.user
    Assessment = Assessment_Model.objects.get(pk=id)
    score = ClientExam_DB.objects.get(Client=Client,Assessmentname=Assessment.name,qpaper=Assessment.question_paper).score
    return render(request,'Assessment/result.html',{'Assessment':Assessment,"score":score})
