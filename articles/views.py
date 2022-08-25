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