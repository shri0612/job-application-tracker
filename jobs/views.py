from django.shortcuts import render, redirect
from .models import Job
from .forms import JobForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.contrib import messages



# Create your views here.


# This view handles the logic for displaying all job entries
@login_required
@never_cache
def job_list(request):
    jobs = Job.objects.filter(user=request.user)  # only show jobs for logged-in user
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
@never_cache
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # link job to logged-in user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
@never_cache
def edit_job(request, id):
    try:
        job = Job.objects.get(id=id, user=request.user)  # ✅ only this user's job
    except Job.DoesNotExist:
        return HttpResponseNotFound("<h2>This job does not exist or you have deleted the job.</h2>")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'job': job})


@login_required
@never_cache
def delete_job(request, id):
    try:
        job = Job.objects.get(id=id, user=request.user)  # ✅ only this user's job
    except Job.DoesNotExist:
        return HttpResponseNotFound("<h2>This job does not exist or you have deleted the job.</h2>")

    if request.method == 'POST':
        job.delete()
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
