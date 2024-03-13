from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms

from .models import *
from inkfluence.bing_search import run_query


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_author = request.POST.get('is_author')

        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists. Choose another one.'}
            return render(request, 'signup.html', context)
        else:
            user = User.objects.create_user(username=username, password=password)
            role = 'author' if is_author else 'reader'
            profile = Profile.objects.create(user=user, role=role)
            profile.save()
            login(request, user)
            return redirect('edit_profile')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'username={username}    password={password}')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'error': 'Invalid username or password.'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page

@login_required
def home_view(request):
    top_story = Story.objects.annotate(avg_rating=Avg('comments__rating')).order_by('-avg_rating').first()
    latest_stories = Story.objects.order_by('-date')[:3]
    genre_list = [genre_name for code, genre_name in GENRES]
    context = {'top_story': top_story,
               'latest_stories': latest_stories,
               'genre_list': genre_list}
    return render(request, 'homePage.html', context)

@login_required
def search_view(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'searchPage.html', {'result_list': result_list})

@login_required
def submit_view(request):
    return render(request, 'storySubmission.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    profile_pic = request.user.profile.profile_pic
    stories = request.user.profile.stories.all()[:4]
    name = request.user.username
    bio = request.user.profile.bio
    genres = request.user.profile.genre_likes

    if profile.role == 'reader':
        return render(request, 'profileReader.html', {'profile': profile, 'profile_pic': profile_pic, 'stories': stories, 'name': name, 'bio': bio, 'genres': genres})
    else:
        return render(request, 'profileAuthor.html', {'profile': profile, 'profile_pic': profile_pic, 'stories': stories, 'name': name, 'bio': bio, 'genres': genres})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = forms.ProfileForm()
    return render(request, 'editProfile.html', {'form': form})

@login_required
def story_submission_view(request):
    print(request.user.profile.role)
    # verify the role is author
    if request.user.profile.role != 'author':
        return JsonResponse({'message': 'the user role is not author'}, status=400)
    # create story object
    return JsonResponse({'message': 'submit story successfully'}, status=201)

@login_required
def story_view(request):
    # find the story
    return render(request, 'storyPage.html')

@login_required
def comment_view(request):
    # find the story
    return JsonResponse({'message': 'comment story successfully'}, status=201)