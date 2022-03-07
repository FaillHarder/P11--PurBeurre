from search.models import Product

from django.http import JsonResponse
from django.shortcuts import redirect, render


def index(request):
    return render(request, "index.html")


def mentions(request):
    return render(request, "mentions.html")


def search_product(request):
    """Get user input to search product in db.
    return a queryset"""
    if request.method == "GET":
        query = request.GET.get("query")
        if query != "":
            products_list = Product().search(query)
            context = {
                "products": products_list
            }
            return render(request, "search_product.html", context)
        else:
            return(redirect("index"))
    else:
        return(redirect("index"))


def ajax_search_product(request):
    """Get user input to search product in db.
    return a queryset"""
    query = request.POST.get("query")
    if query != "":
        print(query)
        ajax_response = []
        products_list = Product().search(query)
        for prod in products_list:
            ajax_response.append({
                "product_name": prod.product_name,
                "bar_code": prod.bar_code,
                "nutriscore": prod.nutriscore,
                "image": prod.image
            })
        return JsonResponse({"result": ajax_response})


def substitute(request):
    """Get product seleted by user,use their barcode for
    search a substitute. Return a queryset"""
    if request.method == "GET":
        bar_code = request.GET.get("query")
        product = Product.objects.get(bar_code=bar_code)
        substitutes = Product().substitute(bar_code)
        context = {
            "product": product,
            "substitutes": substitutes
        }
        return render(request, "substitute.html", context)
