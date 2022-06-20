from . import views
from django.urls import path

urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('myrecipes/', views.MyRecipes.as_view(), name='my_recipes'),
    path('addrecipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('<slug:slug>/update/', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('<slug:slug>/delete/', views.DeleteRecipe.as_view(), name='delete_recipe'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
]
