from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from .models import Choice
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from django.template import loader

# Create your views here.
# def index(request):
#     question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('blog/index.html')
#     context = {
#         'question_list': question_list,
#     }
#     # return HttpResponse(template.render(context,request))
#     return render(request, 'blog/index.html', context)
#
# def detail(request,question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('question does not exist')
#     # return render(request, 'blog/detail.html', {'question': question})
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request, 'blog/detail.html',{'question':question})
#
# def result(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,'blog/results.html', {'question':question})
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'blog/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'blog/results.html'

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'blog/detail.html',{
            'question': question,
            'error_message': 'You didnt select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('blog:results', args=(question_id,)))



