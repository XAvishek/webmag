from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, RedirectView, CreateView, DeleteView, UpdateView

from news.models import News, Comment
from accounts.forms import EmailSignupForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.text import slugify

from news.forms import NewsCreateForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
class NewsTemplateView(TemplateView):
    template_name='index.html'
    form = EmailSignupForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        context["latest_news"] = news.order_by("-created_at")

        context["webdesign_news"] = news.filter(
            category="1").order_by("-created_at")[:4]
        context["javascript_news"] = news.filter(
            category="2").order_by("-created_at")[:4]
        context["css_news"] = news.filter(
            category="3").order_by("-created_at")[:4]
        context["jquery_news"] = news.filter(
            category="4").order_by("-created_at")[:4]
        context["popular_news"] = news.order_by("-count")[:4]
        context["featured_news"] = news.order_by("count")[:3]
        context["form"] = self.form
        return context


class CreateNewsView(LoginRequiredMixin,CreateView):
    model = News
    login_url='/accounts/login'
    form_class=NewsCreateForm
    
    template_name='news/create_news.html'
    success_url=reverse_lazy('home')
    

    def form_valid(self,form):
        
        news = form.save(commit=False)
        title= form.cleaned_data['title']
        
        # news_tag=form.cleaned_data['news_tag']
        news.author = self.request.user
        news.slug = slugify(title)
        news.save()
        return super(CreateNewsView,self).form_valid(form)


    def form_invalid(self,form):
        print (form.errors)
        return super(CreateNewsView,self).form_invalid(form)      


class NewsCategoryView(ListView):
    model = News
    ordering = ['-created_at']
    context_object_name = 'category_list'
    template_name = "news/category_news.html"
    paginate_by = 2
    form = EmailSignupForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get('category')
        return context

    def get_queryset(self):
        category = self.kwargs.get("category")
        category_key = [item[0] for item in News.CATEGORY if item[1] == category][0]

        return News.objects.filter(category=category_key)


class NewsDetailView(DetailView):
    model = News
    form = EmailSignupForm()
    template_name = 'news/detail_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        news = News.objects.all()

        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object)
        #context['my_likes'] = Like.objects.filter(news=self.object)
        context['popular_news'] = news.order_by("-count")[:4]
        context["featured_news"] = news.order_by("count")[:2]
        # context["tags"] = TaggableManager().bulk_related_objects(self.object)
        self.object.count = self.object.count + 1
        self.object.save()
        return context


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = "news/update_news.html"
    fields = ("title", "story")
    success_url = reverse_lazy("home")


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("home")


@login_required
def create_comment(request, **kwargs):
    data = request.POST
    news = get_object_or_404(News, pk=kwargs.get('pk'))
    feedback = data.get('feedback')
    comment_by = request.user
    payload = {"news": news, "comment_by": comment_by, "feedback": feedback}
    comment = Comment(**payload)
    comment.save()
    return render(request, "news/comment.html", {"comment": comment})



class SearchResultsView(ListView):
    model = News
    template_name = 'search_results.html'    

    def get_context_data(self, **kwargs):
        news = News.objects.all()
        context = super().get_context_data(**kwargs)
        context['popular_news'] = news.order_by("-count")[:4]
        context["featured_news"] = news.order_by("count")[:2]
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = News.objects.filter(Q(title__icontains=query) |
        Q(story__icontains=query)
        ) 
        return object_list
