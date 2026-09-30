from .models import Category

def menu_links(request):
    linki = Category.objects.all()
    return dict(links=linki)