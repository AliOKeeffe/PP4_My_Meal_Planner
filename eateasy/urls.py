"""URL Patterns"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse_recipes'),
    path('myrecipes/', views.MyRecipes.as_view(), name='my_recipes'),
    path('addrecipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('mymealplan/', views.MealPlan.as_view(), name='my_mealplan'),
    path(
        'bookmark/<slug:slug>',
        views.BookmarkRecipe.as_view(), name='bookmark_recipe'
        ),
    path('mybookmarks/', views.MyBookmarks.as_view(), name='my_bookmarks'),
    path(
        'recipes/<slug:slug>/',
        views.RecipeDetail.as_view(), name='recipe_detail'
        ),
    path(
        'recipes/<slug:slug>/update/',
        views.UpdateRecipe.as_view(), name='update_recipe'
        ),
    path(
        'recipes/<slug:slug>/delete/',
        views.DeleteRecipe.as_view(), name='delete_recipe'
        ),
    path(
        'comments/<int:pk>/update/',
        views.UpdateComment.as_view(), name='update_comment'
        ),
    path(
        'comments/<int:pk>/delete/',
        views.DeleteComment.as_view(), name='delete_comment'
        ),
]
