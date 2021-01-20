
"""
<!-- 

Author: Francisco López Alonso
Creation date: 24/09/2020 11:43
Last Update -

-->

"""

from django.shortcuts import render
from .models import Page


def page(request, slug):

    page = Page.objects.get(slug=slug)
    return render(request, 'page.html',{
        'page': page
    })



