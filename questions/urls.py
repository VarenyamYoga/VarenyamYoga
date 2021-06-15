from django.urls import path
from . import views
urlpatterns = [
    path('Trainer/viewAssessment/',views.view_Assessment_Trainer,name="view_Assessment"),
    path('Trainer/viewpreviousexams/',views.view_previousAssessment_Trainer,name="Corporate-previous"),
    path('Trainer/viewresults/',views.view_results_Trainer,name="Corporate-result"),
    path('Trainer/addquestions/',views.add_questions,name="Corporate-addquestions"),
    path('Trainer/addnewquestionpaper/',views.add_question_paper,name="Corporate-add_question_paper"),
    path('Trainer/viewClient/',views.view_Client_Trainer,name="faculty-Client"),
    path('Client/viewexams/',views.view_Assessment_Client,name="view_Assessment_Client"),
    path('Client/previous/',views.Client_view_previous,name="Client-previous"),
    path('Client/appear/<int:id>',views.appear_Assessment,name = "appear-Assessment"),
    path('Client/result/<int:id>',views.result,name = "result"),
    path('Client/attendance/',views.view_Client_attendance,name="view_Client_attendance")
]