from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from tasks.models import Task
from .forms import CreateNewTask
from django.utils import timezone
from django.contrib.auth.decorators import login_required #para proteger las urls

# Create your views here.

def home(req):
    return  render(req,'index/index.html')

def singup(req):
    if req.method=='GET':
        return render(req,'singup/singup.html',{
        #'form':UserCreationForm()
        
    })
    else:
        
        if req.POST['password1'] == req.POST['password2']:
            try:
                user=User.objects.create_user(username=req.POST['username'],password=req.POST['password1'])
                login(req,user)
                return redirect('home')
               
                
            
            except:
                return render(req,'singup/singup.html',{
                    'form':UserCreationForm(),
                    'saveuser':'user already exist'
                    
                })
            
        else:
            return render(req,'singup/singup.html',{
                    'form':UserCreationForm(),
                    'saveuser':'password does not match'
                    
                })
            
@login_required
def tasks(req):
    
    tasks=Task.objects.filter(user=req.user, datecompleted__isnull=True)
    return render(req,'tasks.html',{
        'tasks':tasks
    })
@login_required
def listTaskCompleted(req):
    tasks=Task.objects.filter(user=req.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(req,'tasks.html',{
        'tasks':tasks,
    })
@login_required
def taskDetail(req,id):
   
    if req.method=='GET':
        task=get_object_or_404(Task,pk=id, user=req.user)
        form=CreateNewTask(instance=task)
        
        return render(req,'task_detail.html',{
        'task':task,
        'form':form
    })
    else:
        try:
            task=get_object_or_404(Task,pk=id,user=req.user)
            form=CreateNewTask(req.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
              return render(req,'task_detail.html',{
        'form':CreateNewTask,
        'error':'Please provide valida data'
    })
@login_required        
def completedTask(req,id):
    task=get_object_or_404(Task,pk=id, user=req.user)
    if req.method=='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('listTaskCompleted')

@login_required        
def incompletedTask(req,id):
    task=get_object_or_404(Task,pk=id, user=req.user)
    if req.method=='POST':
        task.datecompleted=None
        task.save()
        return redirect('tasks')    
    
@login_required
def singout(req):
    logout(req)
    return redirect('home')

def singin(req):
    if req.method=='GET':
        return render(req,'singin/singin.html',{
        #'form':AuthenticationForm
    })
    else:
        user=authenticate(req,username=req.POST['username'],password=req.POST['password'])
        if user is None:
             return render(req,'singin/singin.html',{
        'form':AuthenticationForm,
        'error': 'user or password is incorrect'
    })
        else:
            login(req,user)
            return redirect('tasks')
@login_required          
def createTask(req):
    if req.method=='GET':
        
        return render(req,'createTasks.html',{
        'form':CreateNewTask
    })
    else:
        try:
            form=CreateNewTask(req.POST)
            new_task=form.save(commit=False)
            new_task.user=req.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
              return render(req,'createTasks.html',{
        'form':CreateNewTask,
        'error':'Please provide valida data'
    })
@login_required      
def deleteTask(req,id):
    task=get_object_or_404(Task,pk=id, user=req.user)
    if req.method=='POST':
        
        task.delete()
        return redirect('tasks')
            
    
   
          
 
        
    