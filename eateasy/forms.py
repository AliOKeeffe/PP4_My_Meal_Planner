from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# class AddRecipeForm(forms.ModelForm):
#     class Meta:
#         model = Recipe
#         fields = [
#             'title',
#             'description',
#             'method',
#             'image',
#             'is_vegetarian',
#             'is_vegan'
#         ]