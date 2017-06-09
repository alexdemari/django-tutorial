import datetime

import pytest
from django.urls.base import reverse
from django.utils import timezone

from mysite.polls.models import Question


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


@pytest.mark.django_db
def test_index_view_with_no_questions(client):
    """
    If no questions exist, an appropriate message should be displayed.
    """
    response = client.get(reverse('polls:index'))
    assert response.status_code == 200
    assert "No polls are available." in response.content.decode()
    assert not response.context['latest_question_list']


@pytest.mark.django_db
def test_index_view_with_a_past_question(client):
    """
    Questions with a pub_date in the past should be displayed on the
    index page.
    """
    create_question(question_text="Past question.", days=-30)
    response = client.get(reverse('polls:index'))
    assert 'Past question.' in response.content.decode()


@pytest.mark.django_db
def test_index_view_with_a_future_question(client):
    """
    Questions with a pub_date in the future should not be displayed on
    the index page.
    """
    create_question(question_text="Future question.", days=30)
    response = client.get(reverse('polls:index'))
    assert "No polls are available." in response.content.decode()
    assert not response.context['latest_question_list']


@pytest.mark.django_db
def test_index_view_with_future_question_and_past_question(client):
    """
    Even if both past and future questions exist, only past questions
    should be displayed.
    """
    create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    response = client.get(reverse('polls:index'))
    assert 'Past question.' in response.content.decode()


@pytest.mark.django_db
def test_index_view_with_two_past_questions(client):
    """
    The questions index page may display multiple questions.
    """
    create_question(question_text="Past question 1.", days=-30)
    create_question(question_text="Past question 2.", days=-5)
    response = client.get(reverse('polls:index'))
    assert 'Past question 1.' in response.content.decode()
    assert 'Past question 2.' in response.content.decode()


@pytest.mark.django_db
def test_detail_view_with_a_future_question(client):
    """
    The detail view of a question with a pub_date in the future should
    return a 404 not found.
    """
    future_question = create_question(question_text='Future question.', days=5)
    url = reverse('polls:detail', args=(future_question.id,))
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_detail_view_with_a_past_question(client):
    """
    The detail view of a question with a pub_date in the past should
    display the question's text.
    """
    past_question = create_question(question_text='Past Question.', days=-5)
    url = reverse('polls:detail', args=(past_question.id,))
    response = client.get(url)
    assert past_question.question_text in response.content.decode()
