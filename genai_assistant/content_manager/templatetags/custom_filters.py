# content_manager/templatetags/custom_filters.py
import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)
