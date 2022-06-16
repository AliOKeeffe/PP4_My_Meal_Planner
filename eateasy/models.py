from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    title = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True,)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    method = models.TextField()
    image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return self.title

class Comment(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    # approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


# class Favourites(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
#     favourites = models.ManyToManyField(Recipe, related_name="favourites", blank=True)


# class MealPlan(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plan")

# class MealPlanItem(models.Model):
#     meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="meal_plan_item")
#     recipe = models.ManyToManyField(Recipe, related_name="meal_plan_item")
#     # day = models.IntegerChoices()