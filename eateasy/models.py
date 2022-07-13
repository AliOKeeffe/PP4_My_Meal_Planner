from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from cloudinary.models import CloudinaryField

STATUS = ((0, "Save for later"), (1, "Publish Now"))



# class Ingredient(models.Model):
#     name = models.CharField(max_length=100)
#     # quantity = models.FloatField()
#     # recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")

#     def __str__(self):
#         return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    updated_on = models.DateTimeField(auto_now=True)
    preparation_time = models.CharField(max_length=10, default=0)
    cook_time = models.CharField(max_length=10, default=0)
    description = models.TextField()
    ingredients = models.TextField()
    method = models.TextField()
    image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)

    class Meta:
        ordering = ['-created_on']


    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class MealPlanItem(models.Model):

    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plan")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="meal_plan_item")
    day = models.IntegerField(choices=DAY_CHOICES, default='0')
    
    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"Meal Plan for {self.day} by {self.user}"

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

