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
            'is_vegetarian',
            'is_vegan',
            'status',
        ]
        widgets = {
            'method': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
        }

    # def clean_title(self):
    #     return self.cleaned_data['title'].title()


class MealPlanForm(forms.ModelForm):
    """ Create Meal Plan Form """
    class Meta:
        """Get meal plan model, choose fields to display"""
        model = MealPlanItem
        fields = ('day',)
