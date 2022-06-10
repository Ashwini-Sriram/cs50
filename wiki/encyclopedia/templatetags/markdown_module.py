#this is how to regiter a filter 
from atexit import register
import markdown2 as md
from django import template
from django.template.defaultfilters import stringfilter

register=template.Library()

@register.filter()
@stringfilter

#filter 
def markdown(value):
    #return md.markdown(value, extensions=['markdown2.extensions.fenced_code'])
    return md.markdown(value)

