import datetime
from urllib.request import urlopen

from django.test import LiveServerTestCase, SimpleTestCase, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    """Create a question with a pub_date offset by `days` from now."""
    pub_time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_time)


class QuestionModelTests(TestCase):
    """Lab requirement: 2 tests using django.test.TestCase."""

    def test_was_published_recently_with_future_question(self):
        future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_question = Question(
            pub_date=timezone.now()
            - datetime.timedelta(hours=23, minutes=59, seconds=59)
        )
        self.assertIs(recent_question.was_published_recently(), True)


class PollsSimpleTests(SimpleTestCase):
    """Lab requirement: 1 test using django.test.SimpleTestCase."""

    def test_index_url_resolves(self):
        self.assertEqual(reverse("polls:index"), "/polls/")


class PollsTransactionTests(TransactionTestCase):
    """Lab requirement: 1 test using django.test.TransactionTestCase."""

    def test_can_create_question_in_transaction_test(self):
        question = create_question("Transaction question", days=-1)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get(pk=question.pk).question_text, "Transaction question")


class PollsLiveServerTests(LiveServerTestCase):
    """Lab requirement: 1 test using django.test.LiveServerTestCase."""

    def test_live_server_serves_index_page(self):
        url = f"{self.live_server_url}{reverse('polls:index')}"
        with urlopen(url) as response:
            body = response.read().decode("utf-8")
        self.assertIn("No polls are available.", body)