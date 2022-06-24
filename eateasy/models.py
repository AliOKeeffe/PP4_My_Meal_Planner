from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))

DAY_CHOICES = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)

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
    status = models.IntegerField(choices=STATUS, default=0)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)

    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})

class MealPlanItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plan")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="meal_plan_item")
    day = models.CharField(max_length=20, choices=DAY_CHOICES, default='Monday', unique=True)
        
    def __str__(self):
        return self.day

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

