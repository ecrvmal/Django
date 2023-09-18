import logging
from typing import Dict, Union

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    """
    The send_feedback_mail function sends an email to the TechSupport Help team.
        Args:
            message_form (Dict[str, Union[int, str]]): A dictionary containing a user's id and message.

    :param message_form: Dict[str: Specify the type of data that is expected to be passed into the function
    :param Union[int: Specify that the value of user_id can be either an int or a string
    :param str]]: Specify the type of data that is expected to be passed into the function
    :return: None
    :doc-author: Trelent
    """
    logger.info(f"Send message: '{message_form}'")
    model_user = get_user_model()
    user_obj = model_user.objects.get(pk=message_form["user_id"])
    send_mail(
        "TechSupport Help",  # subject (title)
        message_form["message"],  # message
        user_obj.email,  # send from
        ["techsupport@braniac.com"],  # send to
        fail_silently=False,
    )
    return None
