from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Recipe, MealPlanItem
from .forms import CommentForm, RecipeForm, MealPlanForm


class Home(View):
    def get(self, request):
        return render(request, 'index.html')



class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'browse_recipes.html'
    paginate_by = 6



    # def get(self, request):
    #     mealplan = MealPlanItem.objects.filter(user=request.user.id)
    #     return render(
    #         request, 'my_mealplan.html', {'mealplan': mealplan})


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

            if mealplan_item:
                # check if user wants to over write existing meal plan item
                mealplan_item.recipe = recipe
            else:
                mealplan_item = mealplan_form.save(commit=False)
                mealplan_item.user = request.user
                mealplan_item.recipe = recipe

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


class AddRecipe(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    # formset = IngredientFormSet()
    template_name = 'add_recipe.html'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class AddMealPlanItem(LoginRequiredMixin, generic.CreateView):
#     form_class = MealPlanForm
#     template_name = 'add_mealplan_item.html'
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         # recipe = get_object_or_404(Recipe, slug=slug)
#         form.instance.user = self.request.user

#         return super().form_valid(form)

# def add_recipe(request):
#     if request.method == "GET":
#         form = RecipeForm()
#         formset = IngredientFormSet()
#         return render(request, 'add_recipe.html', {"form": form, "formset": formset})

#     elif request.method == 'POST':
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             form.instance.author = request.user
#             recipe = form.save()
#             formset = IngredientFormSet(request.POST, instance=recipe)
#             if formset.is_valid():
#                 formset.save()
#             return redirect('/')
#         else:
#             return render(request, 'add_recipe.html', {"form": form})

class MyRecipes(LoginRequiredMixin, generic.ListView):
    model = Recipe
    queryset = Recipe.objects.all()
    template_name = 'my_recipes.html'
    paginate_by = 6


class UpdateRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   
    def test_func(self):
        """
        Prevent another user from deleting recipes
        """

        recipe = self.get_object()
        return recipe.author == self.request.user



class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        """
        Prevent another user from deleting recipes
        """
        recipe = self.get_object()
        return recipe.author == self.request.user

class FavouriteRecipe(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=slug)
        if recipe.favourites.filter(id=request.user.id).exists():
            recipe.favourites.remove(request.user)
        else:
            recipe.favourites.add(request.user)
        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))


class MyFavourites(LoginRequiredMixin, generic.ListView):
    def get(self, request):
        fav_recipes = Recipe.objects.filter(favourites=request.user.id)
        return render(
            request, 'my_favourites.html', {'fav_recipes': fav_recipes})


class MealPlan(LoginRequiredMixin, generic.ListView):
    def get(self, request):
        mpi = MealPlanItem.objects.filter(user=request.user)
        days = [0, 1, 2, 3, 4, 5, 6]
        mpi_response = {}
        for cal_day in days:
            mpi_response[cal_day] = mpi.filter(day=cal_day) or 'nil'

        return render(
            request, 'my_mealplan.html', {'mpi': mpi_response, 'days': [0, 1, 2, 3, 4, 5, 6]})
