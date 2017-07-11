from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    author = models.ForeignKey(Author)
    main_text = models.TextField('正文')
    published_time = models.DateField('出版时间', auto_now_add=timezone.now())
    modified_time = models.DateField('修改时间', auto_now=timezone.now())
    def __str__(self):
        return self.title


