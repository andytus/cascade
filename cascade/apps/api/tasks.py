from __future__ import absolute_import

from celery import shared_task
from cascade.libs.uploads import process_upload_records

@shared_task
def task_upload_records(model_type, upload_file_id):
    process_upload_records(model_type, upload_file_id)


