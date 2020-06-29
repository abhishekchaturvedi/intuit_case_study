import os, sys
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from userlogin.app import create_celery_app, mail_extension
from userlogin.blueprints.user.models import User

celery = create_celery_app()

activate_account_template = """
Hi %s,

Please use the following url to activate your account.

%s/api/confirm/?token=%s

If you did not register then ignore this email.

Thanks,

"""

@celery.task()
def send_email(user_id, token):
    """
    Send a activation/registration email to a user.

    :param user_id: The user id
    :param token: The activation token
    """
    user = User.query.get(user_id)

    if user is None:
        return

    message = activate_account_template % (user.email, celery.conf['SERVER_NAME'], token)
    logger.debug("Sending email: {0}".format(message))
    mail_extension.send_message(subject='Activate your account :--: ',
                                recipients=[user.email])
    return None
