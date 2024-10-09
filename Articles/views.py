from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Articles
from taggit.models import Tag
from Product.models import Product
from authentication.views import menu_list
# Create your views here.

def all_articles(request):
    articles_list = Articles.objects.all()[::-1]

    if request.GET.get('tag'):
        articles_list = Articles.objects.filter(tags__name=request.GET.get('tag'))[::-1]

    if request.GET.get('search'):
        query = request.GET.get('search')
        articles_list = Articles.objects.filter(
            Q(name__icontains=query) |
            Q(content__icontains=query)
        )[::-1]

    tags = Tag.objects.all()[::-1]

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(articles_list, 12)  # Show 10 articles per page
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'All-Articles.html', {
        'result_list': menu_list(),
        'title': 'Articles',
        'tags': tags,
        'articles': articles,
    })
    
def article_main(request, name):
    current_article = get_object_or_404(Articles, name=name)
    all_articles = Articles.objects.all()
    current_index = list(all_articles).index(current_article)
    next_article = None
    if current_index > 0:
        next_article = all_articles[current_index - 1]

    # Get the next article
    previous_article = None
    if current_index < len(all_articles) - 1:
        previous_article = all_articles[current_index + 1]
    
    articles = Articles.objects.all()
    tags = Tag.objects.all()
    top_selling_products = Product.objects.all()[::4]
    

    
    return render(request, 'Article-singal.html', {
        'result_list':menu_list(),'title':current_article.name,
        'article': current_article,
        'previous_article': previous_article,
        'next_article': next_article,
        'articles': articles,
        'tags': tags,
        'top_selling_products': top_selling_products,
    })
