from .models import*
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import*
from django import template

# Create your views here.
def homefn(request):
    return render(request, 'home.html')

def mainfn(request):
    # Fetch projects (if needed)
    projects = Project.objects.all()
    
    # Fetch tasks assigned to the current user
    tasks = Task.objects.filter(assigned_to=request.user)
    
    # Pass the data to the template
    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'main.html', context)


def loginfn(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            if user.is_superuser:  # Check if the user is an admin
                return redirect('/adminpanel')  # Redirect to Django admin panel
            else:
                return redirect('/main')  # Redirect to main.html for regular users
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logoutfn(request):
    logout(request)
    return redirect('/login')

def regfn(request):
    if request.method == 'POST':
        a = request.POST['user']
        b = request.POST['fname']
        c = request.POST['lname']
        d = request.POST['mail']
        e = request.POST['pass']
        f = request.POST['cpass']
        
        if e == f:
            if User.objects.filter(username=a).exists():
                messages.error(request, 'username already exist')
                return render(request, 'register.html')
            elif User.objects.filter(email=d).exists():
                messages.error(request, 'email already exists')
                return render(request, 'register.html')
            else:
                # Here, you need to create the user and return a response
                User.objects.create_user(username=a, first_name=b, last_name=c, email=d, password=e)
                return redirect('/login')  # Redirect to home or another page after successful registration
        else:
            messages.error(request, 'incorrect pass')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')
    

@login_required
def adminpanel(request):
    # Redirect non-admin users
    if not request.user.is_superuser:
        return redirect('/main')

    # Fetch user-related data (excluding superusers)
    total_users = User.objects.filter(is_superuser=False).count()
    active_users = User.objects.filter(is_active=True, is_superuser=False).count()

    # Fetch task-related data
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Completed').count()

    # Calculate user progress (excluding superusers)
    user_progress = []
    users = User.objects.filter(is_superuser=False)  # Exclude superusers
    for user in users:
        total_user_tasks = Task.objects.filter(assigned_to=user).count()
        completed_user_tasks = Task.objects.filter(assigned_to=user, status='Completed').count()
        progress = (completed_user_tasks / total_user_tasks * 100) if total_user_tasks > 0 else 0
        user_progress.append({
            'user': user,
            'total_tasks': total_user_tasks,
            'completed_tasks': completed_user_tasks,
            'progress': round(progress, 2),
        })
       
    # Fetch projects and tasks
    projects = Project.objects.all()
    tasks = Task.objects.all()
    comment = Comment.objects.all()

    # Pass data to the template
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'user_progress': user_progress,
        'projects': projects,
        'tasks': tasks,
        'comments': comment,
    }

    return render(request, 'adminpanel.html', context)

@login_required(login_url='/login')   
def addfn(request):
    if request .method=='POST':
        f=Projectform(request.POST,request.FILES)
        if f.is_valid():
            x= f.save(commit=False)
            x.us=request.user
            x.save()
            return redirect('/adminpanel')
        else:
            return render(request,'add.html',{'form':f})
    else:
        return render(request,'add.html',{'form':Projectform()})

@login_required(login_url='/login')   
def addfn1(request):
    if request .method=='POST':
        f=Taskform(request.POST,request.FILES)
        if f.is_valid():
            x= f.save(commit=False)
            x.us=request.user
            x.save()
            return redirect('/adminpanel')
        else:
            return render(request,'add.html',{'form':f})
    else:
        return render(request,'add.html',{'form':Taskform()})
    

@login_required(login_url='/')   
def profilefn(request):
    if request .method=='POST':
        f=Profileform(request.POST,request.FILES)
        if f.is_valid():
            x= f.save(commit=False)
            x.us=request.user
            x.save()
            return redirect('/main')
        else:
            return render(request,'profile.html',{'form':f})
    else:
        return render(request,'profile.html',{'form':Profileform()})
    




def viewfn(request, sid):
    # Fetch the task and its comments
    task = get_object_or_404(Task, id=sid)
    comments = Comment.objects.filter(task=task)

    # Handle comment submission
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        task_id = request.POST.get('sid')
        user = request.user

        if comment_text and task_id:
            task = Task.objects.get(id=task_id)
            Comment.objects.create(task=task, user=user, comment=comment_text)
            return redirect('viewfn', sid=task_id)  # Redirect to the same page

    # Render the task detail page
    return render(request, 'viewpage.html', {'s': task, 'com': comments})


def deleteproject(request, p_id):
    if request.method == 'POST':
        p = Project.objects.get(id=p_id)
        p.delete()
        return redirect('/adminpanel') 
    else:
        p = Project.objects.get(id=p_id)
        return render(request,'delete.html',{'pro':p})
    
def editproject(request,s_id):
    p = Project.objects.get(id=s_id)
    if request.method == 'POST':
        f = Projectform(request.POST, request.FILES, instance=p)
        if f.is_valid():
            f.save()
            return redirect('/adminpanel') 
        else:
            x=Project.objects.all()
            return render(request, 'add.html', {'form': f, 'post': x})
    else:
        f = Projectform(instance=p)
        x=Project.objects.all()
        return render(request, 'add.html', {'form': f, 'post': x})

def deletetask(request, p_id):
    if request.method == 'POST':
        p = Task.objects.get(id=p_id)
        p.delete()
        return redirect('/adminpanel') 
    else:
        p = Task.objects.get(id=p_id)
        return render(request,'delete.html',{'pro':p})
    
def edittask(request,s_id):
    p = Task.objects.get(id=s_id)
    if request.method == 'POST':
        f = Taskform(request.POST, request.FILES, instance=p)
        if f.is_valid():
            f.save()
            return redirect('/adminpanel') 
        else:
            x=Task.objects.all()
            return render(request, 'add.html', {'form': f, 'post': x})
    else:
        f = Taskform(instance=p)
        x=Task.objects.all()
        return render(request, 'add.html', {'form': f, 'post': x})
    
def statusupdate(request,s_id):
    p = Task.objects.get(id=s_id)
    if request.method == 'POST':
        f = Statusform(request.POST, request.FILES, instance=p)
        if f.is_valid():
            f.save()
            return redirect('/main') 
        else:
            x=Task.objects.all()
            return render(request, 'add.html', {'form': f, 'post': x})
    else:
        f = Statusform(instance=p)
        x=Task.objects.all()
        return render(request, 'add.html', {'form': f, 'post': x})
    
