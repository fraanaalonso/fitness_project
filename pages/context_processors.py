from .models import Page

def getPages(request):
    pages = Page.objects.filter(public=True).order_by("order").values_list('id', 'name', 'slug') #select id name url from pages
    return{
        'pages':pages
    }