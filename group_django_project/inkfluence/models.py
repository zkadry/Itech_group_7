from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Defines the list of possible genres as tuples. The right-hand options will be what appears in a drop-down
# menu, and the left-hand options are shorthand strings which will be stored in the database.
GENRES = (('FAN', 'Fantasy'),
          ('SCF', 'Sci-Fi'),
          ('ACT', 'Action & Adventure'),
          ('MYS', 'Mystery'),
          ('HOR', 'Horror'),
          ('THR', 'Thriller & Crime'),
          ('HIS', 'Historical Fiction'),
          ('ROM', 'Romance'),
          ('COM', 'Comedy'),
          ('YA', 'Young Adult'),
          ('CHI', 'Children')
          )

# Defines the list of possible ratings as tuples (Can change to 1-10 or whatever if we prefer).
RATINGS = ((0, 0),
           (1, 1),
           (2, 2),
           (3, 3),
           (4, 4),
           (5, 5)
           )

ROLE_CHOICES = (
    ('author', 'Author'),
    ('reader', 'Reader'),
)

class Profile(models.Model):
    # Associates a single profile with a single user.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')
    # Holds a profile pic image and stores it in the project folder under files/profile_pics.
    # We will need to add more backend logic to allow users to upload their own photos.
    profile_pic = models.ImageField(upload_to='group_django_project/files/profile_pics')
    # Short text bio for an author.
    bio = models.TextField(max_length=300)
    # Allows authors to select multiple genres they like - will be stored in the database
    # as a single string separated by commas e.g. ('FAN, SCF, ACT') etc.
    genre_likes = MultiSelectField(choices=GENRES, max_choices=11, max_length=200)
    # Calculates the author rating as an average of their story ratings. This will not appear
    # as a normal entry in the database but can be called as a normal field property
    # (e.g. Profile.author_rating) when we need to use it, and will be calculated when called,
    # ensuring the info is up-to-date.
    @property
    def author_rating(self):
        return self.stories.aggregate(author_rating=models.Avg('rating'))['author_rating']

class Story (models.Model):
    # Stories can currently only have one genre from the list above.
    # Can change to multi-select if we prefer.
    genre = models.CharField(choices=GENRES, max_length=200)
    # Short text description of the Story.
    description = models.TextField(max_length=300)
    # Similar to author-rating above, this calculates the rating of the story as an average of
    # all ratings left on the story via comments, and can be called like a standard field property (Story.rating).
    # This will mean the info is up to date when the property is called (e.g. when the user loads the website).
    @property
    def rating(self):
        return self.comments.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
    # The content of the story. We can set character limit if we want to but have left it open so far.
    content = models.TextField()
    # Story title, max 200 characters.
    title = models.CharField(max_length=200)
    # This will hold the URL slug which users can use to access the story on the site. We can either let the author
    # choose the slug or perform Slugify logic to automatically create a slug based on the story title.
    slug = models.SlugField()
    # This holds the date the story was created and will auto-fill the date the story was created.
    date = models.DateField(auto_now=True)
    # Holds the story author as a foreign key, allowing a many to one relationship (one author can write many stories).
    # On the Profile side, these are called 'stories' (the related_name variable), so calling Profile.stories will
    # return a list of all stories created by that profile.
    author = models.ForeignKey(Profile, related_name= 'stories' ,on_delete=models.CASCADE)

class Comment(models.Model):
    # Stores the data and time of a comment, and will autofill the date/time the comment was made.
    date_time = models.DateTimeField(auto_now=True)
    # Main content of the comment - I set character limit to 500 for now but can change if we prefer.
    body = models.CharField(max_length=500)
    # When leaving a comment, commenters will be presented with a drop down menu to select a rating
    # from 0-5. Can update to 0-10 or 1-10 or whatever we prefer.
    rating = models.PositiveSmallIntegerField(choices=RATINGS)
    # Holds the story as a foreign key, allowing a many to one relationship (one Story can have many comments).
    # On the Story side, these are called 'comments' (the related_name variable), so calling Story.comments will
    # return a list of all comments on that story.
    story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)


# Create your models here.
