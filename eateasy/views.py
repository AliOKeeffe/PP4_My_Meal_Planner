"""Views"""

from django.shortcuts import render, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Recipe, MealPlanItem, Comment
from .forms import CommentForm, RecipeForm, MealPlanForm


class Home(generic.TemplateView):
    """This view is used to display the home page"""
    template_name = "index.html"


class RecipeList(generic.ListView):
    """
    This view is used to display all recipes in the browse recipes page
    """
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'browse_recipes.html'
    paginate_by = 8


class RecipeDetail(View):
    """
    This view is used to display the full recipe details including comments.
    It also includes the comment form and add to meal plan form
    """
    def get(self, request, slug):
        """
        Retrives the recipe and related comments from the database
        """
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')
        favourited = False
        if recipe.favourites.filter(id=self.request.user.id).exists():
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

    def post(self, request, slug):
        """
        This method is called when a POST request is made to the view
        via the comment form or the meal plan form.
        """
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')
        favourited = False
        if recipe.favourites.filter(id=self.request.user.id).exists():
            favourited = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            messages.success(self.request, 'Comment successfully added')
        else:
            comment_form = CommentForm()

        mealplan_form = MealPlanForm(data=request.POST)

        if mealplan_form.is_valid():
            # get existing mpi record for user / day
            queryset = MealPlanItem.objects.filter(
                user=request.user, day=request.POST['day'])
            mealplan_item = queryset.first()

            # if a mealplan item already exists for that day
            if mealplan_item:
                # over write existing meal plan item
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
    """This view is used to allow logged in users to create a recipe"""
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    success_message = "%(calculated_field)s was created successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the recipe.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        This function overrides the get_success_message() method to add
        the recipe title into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class MyRecipes(LoginRequiredMixin, generic.ListView):
    """
    This view is used to display a list of recipes created by the logged in
    user.
    """
    model = Recipe
    template_name = 'my_recipes.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return Recipe.objects.filter(author=self.request.user)


class UpdateRecipe(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView
        ):

    """
    This view is used to allow logged in users to edit their own recipes
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'
    success_message = "%(calculated_field)s was edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the recipe.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from updating other's recipes
        """
        recipe = self.get_object()
        return recipe.author == self.request.user

    def get_success_message(self, cleaned_data):
        """
        Override the get_success_message() method to add the recipe title
        into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class DeleteRecipe(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    This view is used to allow logged in users to delete their own recipes
    """
    model = Recipe
    template_name = 'delete_recipe.html'
    success_message = "Recipe deleted successfully"
    success_url = reverse_lazy('my_recipes')

    def test_func(self):
        """
        Prevent another user from deleting other's recipes
        """
        recipe = self.get_object()
        return recipe.author == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display sucess message given
        SucessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteRecipe, self).delete(request, *args, **kwargs)


class FavouriteRecipe(LoginRequiredMixin, View):
    """
    This view allows a logged in user to bookmark recipes.
    """
    def post(self, request, slug):
        """
        Checks if user id already exists in the favourites
        field in the Recipe database.
        If they exist then remove them from the database.
        If they don't exist then add them to the database.
        """
        recipe = get_object_or_404(Recipe, slug=slug)
        if recipe.favourites.filter(id=request.user.id).exists():
            recipe.favourites.remove(request.user)
            messages.success(self.request, 'Recipe removed from bookmarks')
        else:
            recipe.favourites.add(request.user)
            messages.success(self.request, 'Recipe added to bookmarks')

        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class MyFavourites(LoginRequiredMixin, generic.ListView):
    """
    This view allows a logged in user to view their bookmarked recipes.
    """
    model = Recipe
    template_name = 'my_favourites.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user favourites"""
        return Recipe.objects.filter(favourites=self.request.user.id)


class MealPlan(LoginRequiredMixin, View):
    """This view renders the logged in user's Meal Plan"""

    def get(self, request):
        """
        Filters the MealPlanItems table by user and creates a dictionary with
        day and meal plan item as a key, value pair.
        """
        user_meal_plan_items = MealPlanItem.objects.filter(user=request.user)

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
            # Retrive meal plan item based on day
            day_meal_plan_item = user_meal_plan_items.filter(day=ind).first()
            # Add to meal plan if it exists
            mealplan[day] = day_meal_plan_item or None

        return render(
            request, 'my_mealplan.html', {'mealplan': mealplan})


class UpdateComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):

    """
    This view is used to allow logged in users to edit their own comments
    """
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    success_message = "Comment edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the comment.
        """
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


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):

    """
    This view is used to allow logged in users to delete their own comments
    """
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"

    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display success message given
        SuccessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to recipe detail view when comment deleted sucessfully"""
        recipe = self.object.recipe
        return reverse_lazy('recipe_detail', kwargs={'slug': recipe.slug})
