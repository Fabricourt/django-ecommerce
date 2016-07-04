from django.http import HttpResponse
from .models import Product
from django.shortcuts import render, get_object_or_404


def index(request):
    latest_product_list = Product.objects.order_by('-creation_date')[:5]
    context = {'latest_product_list': latest_product_list}
    return render(request, 'store/index.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/detail.html', {'product': product})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)