from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Requirement
from .forms import RequirementForm

@login_required
def requirement_list(request):
    requirements = Requirement.objects.filter(created_by=request.user)
    return render(request, 'requirements/requirement_list.html', {'requirements': requirements})



# Create a new requirement and associate it with the logged-in user
@login_required
def requirement_create(request):
    if request.method == 'POST':
        form = RequirementForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit it yet
            requirement = form.save(commit=False)
            requirement.created_by = request.user  # Associate the logged-in user
            requirement.save()  # Now save the requirement to the database
            return redirect('requirement_list')  # Redirect to the list view
    else:
        form = RequirementForm()
    return render(request, 'requirements/requirement_form.html', {'form': form})

# Update an existing requirement that belongs to the logged-in user
@login_required
def requirement_update(request, pk):
    requirement = get_object_or_404(Requirement, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = RequirementForm(request.POST, request.FILES, instance=requirement)
        if form.is_valid():
            form.save()  # Save the updated requirement
            return redirect('requirement_list')  # Redirect to the list view
    else:
        form = RequirementForm(instance=requirement)
    return render(request, 'requirements/requirement_form.html', {'form': form})

# Delete a requirement that belongs to the logged-in user
@login_required
def requirement_delete(request, pk):
    requirement = get_object_or_404(Requirement, pk=pk, created_by=request.user)
    if request.method == 'POST':
        requirement.delete()  # Delete the requirement
        return redirect('requirement_list')  # Redirect to the list view
    return render(request, 'requirements/requirement_confirm_delete.html', {'requirement': requirement})






from .models import SuccessCriteria
from .forms import SuccessCriteriaForm

@login_required
def success_criteria_list(request):
    requirement_id = request.GET.get('requirement', None)
    if requirement_id:
        criteria = SuccessCriteria.objects.filter(requirement_id=requirement_id)
    else:
        criteria = SuccessCriteria.objects.select_related('requirement').all()
    return render(request, 'requirements/success_criteria_list.html', {'criteria': criteria})


@login_required
def success_criteria_create(request):
    if request.method == 'POST':
        form = SuccessCriteriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_criteria_list')
    else:
        form = SuccessCriteriaForm()
    return render(request, 'requirements/success_criteria_form.html', {'form': form})

@login_required
def success_criteria_update(request, pk):
    criteria = get_object_or_404(SuccessCriteria, pk=pk)
    if request.method == 'POST':
        form = SuccessCriteriaForm(request.POST, request.FILES, instance=criteria)
        if form.is_valid():
            form.save()
            return redirect('success_criteria_list')
    else:
        form = SuccessCriteriaForm(instance=criteria)
    return render(request, 'requirements/success_criteria_form.html', {'form': form, 'criteria': criteria})
