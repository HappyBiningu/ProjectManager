from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workflow
from .forms import WorkflowForm

@login_required
def workflow_list(request):
    workflows = Workflow.objects.all()
    return render(request, 'workflows/workflow_list.html', {'workflows': workflows})

@login_required
def workflow_create(request):
    if request.method == 'POST':
        form = WorkflowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workflow_list')
    else:
        form = WorkflowForm()
    return render(request, 'workflows/workflow_form.html', {'form': form})

@login_required
def workflow_update(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk)
    if request.method == 'POST':
        form = WorkflowForm(request.POST, instance=workflow)
        if form.is_valid():
            form.save()
            return redirect('workflow_list')
    else:
        form = WorkflowForm(instance=workflow)
    return render(request, 'workflows/workflow_form.html', {'form': form, 'workflow': workflow})

@login_required
def workflow_delete(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk)
    if request.method == 'POST':
        workflow.delete()
        return redirect('workflow_list')
    return render(request, 'workflows/workflow_confirm_delete.html', {'workflow': workflow})
