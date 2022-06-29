from .models import Comment, Recipe, MealPlanItem
from django.shortcuts import get_object_or_404
from django import forms
# from django.forms import inlineformset_factory
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'cook_time',
            'method',
            'ingredients',
            'image',
            'is_vegetarian',
            'is_vegan',
            'status',
        ]
        widgets = {
            'method': SummernoteWidget(),
            'ingredients': SummernoteWidget()
        }

    def clean_title(self):
        return self.cleaned_data['title'].title()

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlanItem
        fields = ('day',)

# class IngredientForm(forms.ModelForm):
#     class Meta:
#         model = Ingredient
#         exclude = ('recipe',)


# IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm)
