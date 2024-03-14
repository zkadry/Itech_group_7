from django.test import TestCase

# Create your tests here.
# Inside tests.py or within the tests module, e.g., tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Story, Comment


class ViewTestCase(TestCase):
#Test scenarios for sign-up, log-in, log-out, and home views.
    def setUp(self):
        # Create a user and profile
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, role='reader')

        # Log the user in
        self.client.login(username='testuser', password='12345')

    def test_signup_view_post_existing_user(self):
        response = self.client.post(reverse('signup_view'),
                                    {'username': 'testuser', 'password': '12345', 'is_author': 'on'})
        self.assertContains(response, 'Username already exists. Choose another one.', status_code=200)

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login_view'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        response = self.client.get(reverse('logout_view'))
        self.assertRedirects(response, reverse('login'))

    def test_home_view(self):
        response = self.client.get(reverse('home_view'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_get(self):
        response = self.client.get(reverse('search_view'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 200)


    def test_story_submission_view_not_author(self):
        # Assuming the profile role is not 'author' by default
        response = self.client.post(reverse('story_submission_view'),
                                    {'title': 'Test Story', 'genre': 'fiction', 'description': 'A test story',
                                     'content': 'Story content'})
        self.assertContains(response, 'the user role is not author', status_code=400)


#Unit test based on models .py

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.create(user=user, role='author', bio='Test bio')

    def test_profile_creation(self):
        profile = Profile.objects.get(id=1)
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.role, 'author')
        self.assertEqual(profile.bio, 'Test bio')

    def test_author_rating(self):
        # This test might need adjustment based on how author_rating is implemented.
        user = User.objects.get(id=1)
        profile = Profile.objects.get(user=user)
        self.assertIsNone(profile.author_rating)  # Adjust this based on your logic

class StoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='storyuser', password='12345')
        profile = Profile.objects.create(user=user, role='author', bio='Story author bio')
        Story.objects.create(title='Test Story', genre='FAN', description='A test story description', content='Story content here', author=profile)

    def test_story_creation(self):
        story = Story.objects.get(id=1)
        self.assertTrue(isinstance(story, Story))
        self.assertEqual(story.title, 'Test Story')
        self.assertEqual(story.genre, 'FAN')
        self.assertEqual(story.description, 'A test story description')
        self.assertEqual(story.content, 'Story content here')
        self.assertEqual(story.author.user.username, 'storyuser')


def test_story_rating(self):
    # Retrieve the story created in setUpTestData
    story = Story.objects.get(id=1)

    # Create several comments with different ratings to test the average calculation
    Comment.objects.create(body='Comment 1', story=story, rating=5)
    Comment.objects.create(body='Comment 2', story=story, rating=3)
    Comment.objects.create(body='Comment 3', story=story, rating=4)

    # Calculate the expected average rating
    expected_average_rating = (5 + 3 + 4) / 3.0

    # Retrieve the story again to ensure it's updated
    story = Story.objects.get(id=1)

    # Test if the story's rating property returns the expected average
    self.assertAlmostEqual(story.rating, expected_average_rating, places=2)

    class CommentModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            user = User.objects.create_user(username='commentuser', password='12345')
            profile = Profile.objects.create(user=user, role='author', bio='Comment author bio')
            story = Story.objects.create(title='Comment Story', genre='FAN', description='A comment story description',
                                         content='Story content for comments', author=profile)
            Comment.objects.create(body='A test comment', story=story, rating=5)

        def test_comment_creation(self):
            comment = Comment.objects.get(id=1)
            self.assertTrue(isinstance(comment, Comment))
            self.assertEqual(comment.body, 'A test comment')
            self.assertEqual(comment.rating, 5)
            self.assertEqual(comment.story.title, 'Comment Story')