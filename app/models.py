import re
from django.db                   import models
from django.conf                 import settings
from django.utils.translation    import gettext_lazy as _
from django.contrib.auth.models  import AbstractUser

from .managers import CustomUserManager

ARTICLE_STATUS = [("draft", _("draft")), # (value in database, display)
                  ("inprogress", _("in progress")),
                  ("published", _("published"))]

# Create your models here.

class UserProfile(AbstractUser):
    
    email           = models.EmailField(_("email address"), unique=True, max_length=255)
    objects         = CustomUserManager()
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = []

    @property
    def article_count(self):
        return self.articles.count()
    
    @property
    def written_words(self):
        return self.articles.aggregate(models.Sum("word_count"))["word_count__sum"] or 0

class Article(models.Model):

    class Meta:
        verbose_name        = _("article")
        verbose_name_plural = _("articles")

    title        = models.CharField(_("title"), max_length=100)
    content      = models.TextField(_("content"), blank=True, default="")
    word_count   = models.IntegerField(_("word count"), blank=True, default="")
    twitter_post = models.TextField(_("twitter post"), blank=True, default="")
    status       = models.CharField(_("status"), 
                                    max_length=20, 
                                    choices=ARTICLE_STATUS,
                                    default="draft")
    created_at   = models.DateTimeField(_("created at"), auto_now_add=True) # auto_now_add=True means that the field is automatically set to now when the object is first created.
    updated_at   = models.DateTimeField(_("updated at"), auto_now=True) # auto_now=True means that the field is automatically set to now every time the object is saved.
    #creator      = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    creator      = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("creator"), on_delete=models.CASCADE, related_name="articles")

    def __str__(self):
        return self.title
    
    def _words_count(self, text):
        return len(re.findall(r"\b\w+\b", re.sub(r"<[^>]*>", "", text).replace("&nbsp;", " ")))
    
    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*>", "", self.content).replace("&nbsp;", " ")
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)