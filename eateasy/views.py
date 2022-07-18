from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Recipe, MealPlanItem, Comment
from .forms import CommentForm, RecipeForm, MealPlanForm


class Home(View):
    def get(self, request):
        return render(request, 'index.html')



class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'browse_recipes.html'
    paginate_by = 8

class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')
        favourited = False
        if recipe.favourites.filter(id = self.request.user.id).exists():
            favourited = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "comment_form": CommentForm(),
                "mealplan_form": MealPlanForm(),
                "favourited": favourited
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')
        favourited = False
        if recipe.favourites.filter(id = self.request.user.id).exists():
            favourited = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        mealplan_form = MealPlanForm(data=request.POST)


        if mealplan_form.is_valid():
            # ----
            # get exsiting mpi record for user / day
            queryset = MealPlanItem.objects.filter(user=request.user, day=request.POST['day'])
            mealplan_item = queryset.first()

            # if a mealplan item already exists for that day
            if mealplan_item:
                # check if user wants to over write existing meal plan item
                mealplan_item.recipe = recipe
                messages.success(self.request, 'Mealplan successfully updated')
            else:
                mealplan_item = mealplan_form.save(commit=False)
                mealplan_item.user = request.user
                mealplan_item.recipe = recipe
                messages.success(self.request, 'Recipe added to mealplan')

            mealplan_item.save()
            

        else:
            mealplan_form = MealPlanForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "comment_form": CommentForm(),
                "mealplan_form": MealPlanForm(),
                "favourited": favourited
            },
        )


class AddRecipe(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    success_message = "%(calculated_field)s was created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
    )


class MyRecipes(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'my_recipes.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return Recipe.objects.filter(author=self.request.user)

class UpdateRecipe(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'
    success_message = "%(calculated_field)s was edited successfully"


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   
    def test_func(self):
        """
        Prevent another user from deleting recipes
        """

        recipe = self.get_object()
        return recipe.author == self.request.user

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
    )


class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    success_message = "Recipe deleted successfully"
    success_url = reverse_lazy('my_recipes')


    def test_func(self):
        """
        Prevent another user from deleting recipes
        """
        recipe = self.get_object()
        return recipe.author == self.request.user
    
    # cannot use SucessMessageMixin on delete view. Found this alternative method on stack
    # over flow: https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteRecipe, self).delete(request, *args, **kwargs)


class FavouriteRecipe(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        if recipe.favourites.filter(id=request.user.id).exists():
            recipe.favourites.remove(request.user)
            messages.success(self.request, 'Recipe removed from bookmarks')
        else:
            recipe.favourites.add(request.user)
            messages.success(self.request, 'Recipe added to bookmarks')

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))



class MyFavourites(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'my_favourites.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user favourites"""
        return Recipe.objects.filter(favourites=self.request.user.id)

    # def get(self, request):
    #     fav_recipes = Recipe.objects.filter(favourites=request.user.id)
    #     return render(
    #         request, 'my_favourites.html', {'fav_recipes': fav_recipes})


class MealPlan(LoginRequiredMixin, generic.ListView):
    def get(self, request):
        user_meal_plan_items = MealPlanItem.objects.filter(user=request.user)
        # days = [0, 1, 2, 3, 4, 5, 6]
        days = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        mealplan = {}

        for ind, day in days.items():
            day_meal_plan_item = user_meal_plan_items.filter(day=ind).first()
            mealplan[day] = day_meal_plan_item or None

        return render(
            request, 'my_mealplan.html', {'mealplan': mealplan})


class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    success_message = "Comment edited successfully"


    def form_valid(self, form):
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from editing user's comments
        """

        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """ Return to recipe detail view when comment updated sucessfully"""
        recipe = self.object.recipe
        return reverse_lazy('recipe_detail', kwargs={'slug': recipe.slug})


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"


    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username
    
    # cannot use SucessMessageMixin on delete view. Found this alternative method on stack
    # over flow: https://stackoverflow.com/questions/24822509/success-message-in-deleteview-not-shown
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to recipe detail view when comment deleted sucessfully"""
        recipe = self.object.recipe
        return reverse_lazy('recipe_detail', kwargs={'slug': recipe.slug})