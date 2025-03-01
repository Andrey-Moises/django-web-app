from .models                    import Article
from django.db                  import models
from django.urls                import reverse_lazy
# from django.shortcuts           import render, redirect
from django.utils.formats       import date_format
from django.views.generic       import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation   import ngettext, gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# region Function Based Views

# def home(request):

#     articles = Article.objects.all()                                # Query the database for all articles
#     return render(request, "app/home.html", {"articles": articles}) # Render the home.html template with the articles context

# def create_article(request):
#     if request.method == "POST":
#         form = CreateArticleForm(request.POST)
#         if form.is_valid():                     # Check if the form is valid
#             form_data = form.cleaned_data        # Get the form data
#             new_article = Article(
#                 title        = form_data["title"],
#                 status       = form_data["status"],
#                 content      = form_data["content"],
#                 word_count   = form_data["word_count"],
#                 twitter_post = form_data["twitter_post"]
#             )
#             new_article.save()                   # Save the new article to the database
#             return redirect("home")              # Redirect the user to the home page
#     else:
#         form = CreateArticleForm()             # Create an empty form instance
#     return render(request, "app/create_article.html", {"form": form}) # Render the create_article.html template with the form context

# endregion

class ArticleListView(LoginRequiredMixin, ListView):
    
    template_name       = "app/home.html"
    model               = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.get_queryset()
        
        article_count = articles.count()
        written_words = articles.aggregate(total_words=models.Sum('word_count'))['total_words'] or 0

        articles_part = ngettext(
            "You have created %(article_count)s article",
            "You have created %(article_count)s articles",
            article_count
        ) % {'article_count': article_count}

        words_part = ngettext(
            "and written %(written_words)s word",
            "and written %(written_words)s words",
            written_words
        ) % {'written_words': written_words}


        context['user_stats_message'] = f"{articles_part} {words_part}"
        
        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):

    template_name = "app/create_article.html"
    model         = Article
    fields        = ["title", "content", "twitter_post", "status"]
    success_url   = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    template_name       = "app/update_article.html"
    model               = Article
    fields              = ["title", "content", "twitter_post", "status"]
    success_url         = reverse_lazy("home")
    context_object_name = "articles"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date"] = date_format(self.get_object().created_at, format='DATETIME_FORMAT', use_l10n=True)
        return context

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    template_name       = "app/delete_article.html"
    model               = Article
    success_url         = reverse_lazy("home")
    context_object_name = "articles"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator