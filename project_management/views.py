from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_management/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    return render(request, 'project_management/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_management/project_form.html', {'form': form})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = TaskForm()
    return render(request, 'project_management/task_form.html', {'form': form})




from django.http import JsonResponse

@login_required
def kanban_board(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    return render(request, 'project_management/kanban_board.html', {'project': project, 'tasks': tasks})

@login_required
def update_task_column(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        column = request.POST.get('column')
        if column in dict(Task.COLUMN_CHOICES):
            task.column = column
            task.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})



from django.shortcuts import render
from .models import Project

@login_required
def gantt_chart(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()

    # Prepare the data in a format that frappe-gantt understands
    gantt_data = [
        {
            'id': task.id,
            'name': task.title,
            'start': task.start_date.strftime('%Y-%m-%d'),
            'end': task.end_date.strftime('%Y-%m-%d'),
            'progress': 0 if task.status != 'done' else 100,
            'dependencies': '',
        }
        for task in tasks
        if task.start_date and task.end_date
    ]

    return render(request, 'project_management/gantt_chart.html', {
        'project': project,
        'gantt_data': gantt_data
    })





# project_management/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Requirement, UseCase
from .forms import CommentForm

@login_required
def add_comment(request, model_name, object_id):
    if model_name == 'project':
        model = Project
    elif model_name == 'requirement':
        model = Requirement
    elif model_name == 'usecase':
        model = UseCase
    else:
        return redirect('home')

    obj = get_object_or_404(model, id=object_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, content_type=model, object_id=obj.id)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the page
    else:
        form = CommentForm(content_type=model, object_id=obj.id)

    return render(request, 'project_management/add_comment.html', {'form': form, 'object': obj})




from django.shortcuts import render, redirect
from .forms import FileForm

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the file to the database
            return redirect('success')  # Redirect to a success page (you need to create this)
    else:
        form = FileForm()
    
    return render(request, 'upload_file.html', {'form': form})