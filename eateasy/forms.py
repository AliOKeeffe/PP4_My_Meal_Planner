from .models import Comment, Recipe, Ingredient
from django import forms
from django.forms import inlineformset_factory
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
            'method',
            'image',
            'is_vegetarian',
            'is_vegan',
            'status',
        ]
        widgets = {
            'description': SummernoteWidget(),
            'method': SummernoteWidget()
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm)
