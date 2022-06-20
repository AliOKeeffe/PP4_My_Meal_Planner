from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Recipe
from .forms import CommentForm, RecipeForm

class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

class RecipeDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')
        # favourite = False
        # if recipe.favourites.filter

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.order_by('created_on')

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "comment_form": CommentForm()
            },
        )


class AddRecipe(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = 'add_recipe.html'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
    def favourite_list(request):
        favourites = Recipe.objects.filter(favourites=request.user)
        return render(request, 'my_favourites.html', {'favourites': favourites})