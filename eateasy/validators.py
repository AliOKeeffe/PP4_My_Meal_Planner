"""Validators"""

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def textfield_not_empty(textfield):
    """
    Strip white space from textfield and raise validation error
    if field is left empty
    Credit: Ian Meigh_5P for his help with this validator on the code
    Institute's slack channel:
    https://code-institute-room.slack.com/archives/CGWQJQKC5/p1659026298076079?thread_ts=1659005118.161939&cid=CGWQJQKC5.
    """
    cleaned_data = strip_tags(textfield).replace("&nbsp;", "").strip()
    if cleaned_data == "":
        raise ValidationError("Please fill in this field")
