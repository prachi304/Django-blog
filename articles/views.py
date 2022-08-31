from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import redirect

# Create your views here.
def article_list(request):
    articles = Article.objects.all().order_by('title')
    return render(request,'articles/article_list.html',{'articles':articles})

def article_detail(request,slug):
    articles = Article.objects.get(slug=slug)
    return render(request,'articles/article_detail.html',{'articles':articles})

@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request,'articles/article_create.html',{'form':form})

@login_required(login_url="/accounts/login/")
def article_update(request,slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:list')
        else:
            form = forms.CreateArticle(instance=article)
    return render(request,'articles/article_update.html',{'articles':article,'form':form})


@login_required(login_url="/accounts/login/")
def article_delete(request,slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:list')
    return render(request,'articles/article_delete.html',{'articles':article})
