import os, sys
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from userlogin.app import create_celery_app
from flask import current_app

celery = create_celery_app()

@celery.task(name = 'echo_every_1_min')
def echo_every_1_min():
    current_app.logger.debug('Runnning celery... ')
    logger.debug('Running celery... ')
