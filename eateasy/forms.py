"""Forms for Recipes, Comments and Meal Plans"""

from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Recipe, MealPlanItem


class CommentForm(forms.ModelForm):
    """ Create Comment Form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """Get comment model, choose fields to display"""
        model = Comment
        fields = ('body',)


class RecipeForm(forms.ModelForm):
    """ Create Recipe Form """
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """
        Get recipe model, choose fields to display and add summernote widget
        """
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'cook_time',
            'method',
            'ingredients',
            'image',
            'status',
        ]
        widgets = {
            'method': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
        }

    # def clean_ingredients(self):
    #     """
    #     remove all whitespace and strip tags from ingredients
    #     """
    #     ingredients = self.cleaned_data['ingredients']
    #     ingredients = ingredients.replace('&nbsp;', '').strip()
    #     return strip_tags(ingredients)

    # def clean_method(self):
    #     """
    #     remove all whitespace and strip tags from ›method
    #     """
    #     method = self.cleaned_data['method']
    #     method = method.replace('&nbsp;', '').strip()
    #     return strip_tags(method)


class MealPlanForm(forms.ModelForm):
    """ Create Meal Plan Form """
    class Meta:
        """Get meal plan model, choose fields to display"""
        model = MealPlanItem
        fields = ('day',)
