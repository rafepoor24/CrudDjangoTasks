from django.urls import path
from tasks import views

urlpatterns = [
    path('',views.home,name='home'),
    path('singup/',views.singup,name='singup'),
    path('tasks/',views.tasks,name='tasks'),
    path('tasks/listTaskCompleted',views.listTaskCompleted,name='listTaskCompleted'),
    path('logout/',views.singout,name='logout'),
    path('singin/',views.singin,name='singin'),
    path('tasks/createTask/',views.createTask,name='createTask'),
    path('tasks/<int:id>',views.taskDetail,name='taskDetail'),
    path('tasks/taskDetail/<int:id>/complete',views.completedTask,name='completedTask'),
    path('tasks/taskDetail/<int:id>/incompleted',views.incompletedTask,name='incompletedTask'),
    path('tasks/taskDetail/<int:id>/delete',views.deleteTask,name='delete'),

] 
