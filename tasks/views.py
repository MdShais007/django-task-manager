from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from .forms import RegisterForm , LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Task


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
       
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user) #Inbuild django function used to store session 
            return redirect("dashboard")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })
    return render (request, 'login.html')


@login_required(login_url="login")
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
   

    context = {
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "completed": tasks.filter(completed=True).count(),
        "pending": tasks.filter(completed=False).count(),
    }
    print(context)
    return render(request, 'dashboard.html', context=context)


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("dashboard")
    else:
        form = TaskForm()

    return render(request, "add_task.html", {"form": form})



@login_required
def mark_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    task.completed = True
    task.save()

    return redirect("dashboard")


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task)

    return render(request, "edit_task.html", {"form": form})

@login_required
def mark_pending(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    task.completed = False
    task.save()

    return redirect("dashboard")


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    task.delete()

    return redirect("dashboard")


def logout_view(request):
    logout(request)
    return redirect('login')


from .forms import TaskForm

