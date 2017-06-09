import datetime

from django.utils import timezone

from mysite.polls.models import Question


def test_was_published_recently_with_future_question():
    """
    was_published_recently() should return False for questions whose
    pub_date is in the future.
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    assert not future_question.was_published_recently()


def test_was_published_recently_with_old_question():
    """
    was_published_recently() should return False for questions whose
    pub_date is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(pub_date=time)
    assert not old_question.was_published_recently()


def test_was_published_recently_with_recent_question():
    """
    was_published_recently() should return True for questions whose
    pub_date is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Question(pub_date=time)
    assert recent_question.was_published_recently()
