import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from helpup.forms import CustomUserCreationForm, CreateProjectForm
from helpup.models import Project


def home(request):
    return render(request, 'base_template.html', {'user': request.user})

@login_required()
def profile(request):
    projects = Project.objects.filter(student=request.user)
    data = {'projects': projects}
    return render(request, 'profile.html', data)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_exempt
def new_project(request):
    if request.method == "POST":
        # form = CreateProjectForm(request.POST, request.FILES)
        # if form.is_valid():
        #     title = form.cleaned_data['title']
        #     description = form.cleaned_data['description']
        #     location = form.cleaned_data['location']
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        location = data['location']
        lng=data['lng']
        lat=data['lat']
        # picture=data['picture']

        # print picture
        new_project=Project.objects.create(
            title=title,
            date_created=datetime.today(),
            description=description,
            location=location,
            student=request.user,
            lat=lat,
            lng=lng,
        )

        project_info = {
            'title': new_project.title,
            'descriptions': new_project.description,
            'location': new_project.location,
            'lat': lat,
            'lng': lng
        }
        return HttpResponse(json.dumps(project_info), content_type='application/json')








def project_map(request):
    return render(request, 'maps.html')

@csrf_exempt
def get_location(request):
    projects = Project.objects.all()
    project_list=[]
    for project in projects:
        project_info = {
            'title': project.title,
            'description': project.description,
            'lat': project.lat,
            'lng': project.lng
        }
        project_list.append(project_info)
    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_project(request):
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        project_info = {
            'title': project.title,
            'description': project.description,
            'first_name': project.student.first_name,
            'last_name': project.student.last_name,
            'image': str(project.picture),
            'id': project.id

        }
        project_list.append(project_info)

    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')


def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    data={'project': project}
    return render(request, 'view_project.html', data)


@csrf_exempt
def get_user_project(request):
    user=request.user
    projects = Project.objects.filter(student=user)
    project_list=[]
    for project in projects:
        project_info = {
            'title': project.title,
            'id': project.id
        }
        project_list.append(project_info)
    data = {'project_list': project_list}
    return HttpResponse(json.dumps(data), content_type='application/json')

def form(request):
    form = CreateProjectForm()

    data = {'form': form}
    return render(request, 'form.html', data)
