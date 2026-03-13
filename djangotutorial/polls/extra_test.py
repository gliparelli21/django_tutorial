import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class ExtraTutorialQuestionTests(TestCase):
    """One extra tutorial-style test kept in a separate file."""

    def test_was_published_recently_with_old_question(self):
        old_question = Question(
            pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1)
        )
        self.assertIs(old_question.was_published_recently(), False)
