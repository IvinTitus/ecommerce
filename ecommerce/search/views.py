from django.db.models import Q
from django.shortcuts import render
from shop.models import Product


# Create your views here.

def search(request):
    query = ""
    b = None
    if request.method == "POST":
        query = request.POST.get('q', '')
        if query:
            b = Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
    return render(request, "search.html", {'query': query, 'b': b})