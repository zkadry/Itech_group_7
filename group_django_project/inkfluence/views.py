from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm

from .models import *


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
            return redirect('home')
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
    title = 'And So It Begins...'
    author = 'Jane Doe'
    summary_text = 'Lorem ipsum dolor sit amet consectetur. Arcu donec in facilisis pulvinar elit vitae. In justo vitae vitae\
              in massa lorem orci pellentesque. Suspendisse amet donec vel est porttitor purus. Tincidunt praesent risus\
              a feugiat facilisi. Senectus nulla penatibus arcu rhoncus viverra id eleifend sapien etiam. Ac quis\
              lacinia lacus quam.'
    genre = 'Fantasy'

    context = {'title': title,
               'summary_text': summary_text,
               'author': author,
               'genre': genre}
    return render(request, 'homePage.html', context)


@login_required
def search_view(request):
    return render(request, 'searchPage.html')


@login_required
def submit_view(request):
    return render(request, 'storySubmission.html')


@login_required
def profile_view(request):
    profile = request.user.profile
    if profile.role == 'reader':
        return render(request, 'profileAuthor.html', {'profile': profile})
    else:
        return render(request, 'profileReader.html', {'profile': profile})


@login_required
def story_submission_view(request):
    if request.method == 'POST':
        print(request.user.profile.role)
        # verify the role is author
        if request.user.profile.role != 'author':
            return JsonResponse({'message': 'the user role is not author'}, status=400)
        # create story object
        title = request.POST.get("title")
        if Story.objects.filter(title=title).exists():
            context = {'error': '\t\tStory title exists. Please change the title.'}
            return render(request, 'storySubmission.html', context)
        genre = request.POST.get("genre")
        description = request.POST.get("description")
        content = request.POST.get("content")
        # create Story object
        Story.objects.create(
            title=title,
            genre=genre,
            description=description,
            content=content,
            author=request.user.profile
        )
        # return JsonResponse({'message': 'submit story successfully'}, status=201)
        return render(request, 'profileAuthor.html')
    else:
        return render(request, 'storySubmission.html')


@login_required
def story_view(request):
    # find the story by title
    title = request.GET.get("title", "")
    author = request.GET.get("author", "")
    title_story = Story.objects.filter(title=title).first()
    author_story = Story.objects.filter(author__user__username=author).first()
    if title_story:
        story_dict = title_story.__dict__
        comments_objs = title_story.comments.all()
        comments = [obj.__dict__ for obj in comments_objs]
        story_dict.update({"comments": comments})
        story_dict.update({"rate_avg": int(sum([c["rating"] for c in comments]) / len(comments))})
        story_dict.pop('_state', None)
        # author info
        profile = Profile.objects.filter(id=story_dict["author_id"]).first()
        story_dict.update({"profile": profile})
        return render(request, 'storyPage.html', story_dict)
    elif author_story:
        story_dict = author_story.__dict__
        comments_objs = author_story.comments.all()
        comments = [obj.__dict__ for obj in comments_objs]
        story_dict.update({"comments": comments})
        story_dict.update({"rate_avg": int(sum([c["rating"] for c in comments]) / len(comments))})
        story_dict.pop('_state', None)
        # author info
        profile = Profile.objects.filter(id=story_dict["author_id"]).first()
        story_dict.update({"profile": profile})
        return render(request, 'storyPage.html', story_dict)
    else:
        return render(request, 'storyPage.html')


@login_required
def comment_view(request, story_id):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")
        Comment.objects.create(body=comment, story_id=story_id, rating=rating)
    #
    author_story = Story.objects.filter(author=request.user.profile).first()
    if author_story:
        story_dict = author_story.__dict__
        #
        comments_objs = author_story.comments.all()
        comments = [obj.__dict__ for obj in comments_objs]
        story_dict.update({"comments": comments})
        story_dict.update({"rate_avg": int(sum([c["rating"] for c in comments]) / len(comments))})
        story_dict.pop('_state', None)
        # author info
        profile = Profile.objects.filter(id=story_dict["author_id"]).first()
        story_dict.update({"profile": profile})
        return render(request, 'storyPage.html', story_dict)
    else:
        return render(request, 'storyPage.html')
    # return JsonResponse({'message': 'comment story successfully'}, status=201)
