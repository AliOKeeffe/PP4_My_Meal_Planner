from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browserecipes/', views.RecipeList.as_view(), name='browse_recipes'),
    path('myrecipes/', views.MyRecipes.as_view(), name='my_recipes'),
    path('addrecipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('favourite/<slug:slug>', views.FavouriteRecipe.as_view(), name='favourite_recipe'),
    path('myfavourites/', views.MyFavourites.as_view(), name='my_favourites'),
    path('mymealplan/', views.MealPlan.as_view(), name='my_mealplan'),
    path('recipes/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('recipes/<slug:slug>/update/', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('recipes/<slug:slug>/delete/', views.DeleteRecipe.as_view(), name='delete_recipe'),


]
