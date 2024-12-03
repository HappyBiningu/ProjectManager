from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UseCase
from .forms import UseCaseForm

@login_required
def usecase_list(request):
    use_cases = UseCase.objects.all()
    return render(request, 'usecases/usecase_list.html', {'use_cases': use_cases})

@login_required
def usecase_create(request):
    if request.method == 'POST':
        form = UseCaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usecase_list')
    else:
        form = UseCaseForm()
    return render(request, 'usecases/usecase_form.html', {'form': form})

@login_required
def usecase_update(request, pk):
    use_case = get_object_or_404(UseCase, pk=pk)
    if request.method == 'POST':
        form = UseCaseForm(request.POST, instance=use_case)
        if form.is_valid():
            form.save()
            return redirect('usecase_list')
    else:
        form = UseCaseForm(instance=use_case)
    return render(request, 'usecases/usecase_form.html', {'form': form})

@login_required
def usecase_delete(request, pk):
    use_case = get_object_or_404(UseCase, pk=pk)
    if request.method == 'POST':
        use_case.delete()
        return redirect('usecase_list')
    return render(request, 'usecases/usecase_confirm_delete.html', {'use_case': use_case})
