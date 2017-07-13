from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question(question_text=question_text, pub_date=time)



class QuestionMethodTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_now_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        now_question = Question(pub_date=time)
        self.assertIs(now_question.was_published_recently(), True)


class QuestionViewTest(TestCase):
    def test_index_view_with_no_question(self):
        '''如果问题不存在，给出提示'''
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No blog are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text='Past question', days=-3).save()
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question>'])
    def test_index_view_with_a_future_question(self):
        create_question(question_text='Future question', days=30).save()
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'No blog are available')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_past_future_question(self):
        create_question(question_text='Past question', days=-30).save()
        create_question(question_text='Future question', days=30).save()
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question>'])

    def test_index_view_with_two_past_question(self):
        create_question(question_text='Past question1', days=-30).save()
        create_question(question_text='Past question2', days=-4).save()
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question2>', '<Question: Past question1>'])


# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         future_question = create_question(question_text='Future question', days=30).save()
#         url = reverse('blog:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         past_question = create_question(question_text='Past question', days=-4).save()
#         url = reverse('blog:detail', args=(Question.objects.values('id'),))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
