

from django.db.models import Avg
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.utils.http import urlencode
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
    top_story = Story.objects.annotate(avg_rating=Avg('comments__rating')).order_by('-avg_rating').first()
    latest_stories = Story.objects.order_by('-date')[:3]
    genre_list = [genre_name for code, genre_name in GENRES]
    context = {'top_story': top_story,
               'latest_stories': latest_stories,
               'genre_list': genre_list}


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
    if profile.role == 'reader':
        return render(request, 'profileAuthor.html', {'profile': profile})
    else:
        return render(request, 'profileReader.html', {'profile': profile})


@login_required


@login_required
def story_submission_view(request):
    if request.method == 'POST':
        if request.user.profile.role != 'author':
            return JsonResponse({'message': 'The user role is not author'}, status=400)

        title = request.POST.get("title")
        if Story.objects.filter(title=title).exists():
            context = {'error': 'Story title exists. Please change the title.'}
            return render(request, 'storySubmission.html', context)

        genre = request.POST.get("genre")
        if not genre in dict(GENRES).keys():
            context = {'error': 'Invalid genre selected. Please select a valid genre.'}
            return render(request, 'storySubmission.html', context)

        description = request.POST.get("description")
        content = request.POST.get("content")

        Story.objects.create(
            title=title,
            genre=genre,
            description=description,
            content=content,
            author=request.user.profile
        )

        messages.success(request, 'Submit story successfully')
        return redirect('profile')  # Assumes 'profile' is the name of the URL pattern for the profile view
    else:
        return render(request, 'storySubmission.html')


@login_required
def story_view(request):
    title = request.GET.get("title", "")
    context = {}

    story = Story.objects.filter(title=title).first()
    if story:
        comments_objs = story.comments.all()
        comments = [{"body": obj.body, "rating": obj.rating} for obj in comments_objs]

        # 正确地从Story实例获取作者的用户名
        author_username = story.author.user.username  # 这里是正确的路径

        # 使用模型中定义的方法或属性获取平均评分
        rate_avg = story.rating() if hasattr(story, 'rating') and callable(story.rating) else 'No ratings'

        context = {
        "title": story.title,
        "content": story.content,
        "genre": story.genre,
        "description": story.description,
        "date": story.date.strftime('%B %d, %Y'),  # Formatting date
        "author": author_username,
        "author_id": story.author.user.id,
        "comments": comments,
        "rate_avg": rate_avg,
        "author_link": f"/profile/{author_username}/"
        }
    else:
        context = {"error": "The requested story does not exist."}

    return render(request, 'storyPage.html', context)

@login_required
def comment_view(request, story_title):
    if request.method == 'POST':
        # Fetch the story by title
        story = get_object_or_404(Story, title=story_title)

        # Create comment
        comment_body = request.POST.get("comment")
        rating = request.POST.get("rating")

        Comment.objects.create(
            body=comment_body,
            rating=int(rating),
            story=story,
        )

        messages.success(request, 'Your comment was posted successfully.')

        # Encode the title for use in the URL
        title_encoded = urlencode({'title': story_title})

        # Redirect back to the story view
        return redirect(f'/inkfluence/story/?{title_encoded}')
    else:
        messages.error(request, 'There was an error with your comment submission.')
=======
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from . import forms

from .models import *
from django.contrib import messages
from django.utils.http import urlencode
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
            Profile.objects.create(user=user, role=role)
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


@login_required
def story_submission_view(request):
    if request.method == 'POST':
        if request.user.profile.role != 'author':
            return JsonResponse({'message': 'The user role is not author'}, status=400)

        title = request.POST.get("title")
        if Story.objects.filter(title=title).exists():
            context = {'error': 'Story title exists. Please change the title.'}
            return render(request, 'storySubmission.html', context)

        genre = request.POST.get("genre")
        if not genre in dict(GENRES).keys():
            context = {'error': 'Invalid genre selected. Please select a valid genre.'}
            return render(request, 'storySubmission.html', context)

        description = request.POST.get("description")
        content = request.POST.get("content")

        Story.objects.create(
            title=title,
            genre=genre,
            description=description,
            content=content,
            author=request.user.profile
        )

        messages.success(request, 'Submit story successfully')
        return redirect('profile')  # Assumes 'profile' is the name of the URL pattern for the profile view
    else:
        return render(request, 'storySubmission.html')


@login_required
def story_view(request):
    title = request.GET.get("title", "")
    context = {}

    story = Story.objects.filter(title=title).first()
    if story:
        comments_objs = story.comments.all()
        comments = [{"body": obj.body, "rating": obj.rating} for obj in comments_objs]

        # 正确地从Story实例获取作者的用户名
        author_username = story.author.user.username  # 这里是正确的路径

        # 使用模型中定义的方法或属性获取平均评分
        rate_avg = story.rating() if hasattr(story, 'rating') and callable(story.rating) else 'No ratings'

        context = {
        "title": story.title,
        "content": story.content,
        "genre": story.genre,
        "description": story.description,
        "date": story.date.strftime('%B %d, %Y'),  # Formatting date
        "author": author_username,
        "author_id": story.author.user.id,
        "comments": comments,
        "rate_avg": rate_avg,
        "author_link": f"/profile/{author_username}/"
        }
    else:
        context = {"error": "The requested story does not exist."}

    return render(request, 'storyPage.html', context)

@login_required
def comment_view(request, story_title):
    if request.method == 'POST':
        # Fetch the story by title
        story = get_object_or_404(Story, title=story_title)

        # Create comment
        comment_body = request.POST.get("comment")
        rating = request.POST.get("rating")

        Comment.objects.create(
            body=comment_body,
            rating=int(rating),
            story=story,
        )

        messages.success(request, 'Your comment was posted successfully.')

        # Encode the title for use in the URL
        title_encoded = urlencode({'title': story_title})

        # Redirect back to the story view
        return redirect(f'/inkfluence/story/?{title_encoded}')
    else:
        messages.error(request, 'There was an error with your comment submission.')
        return redirect('home')