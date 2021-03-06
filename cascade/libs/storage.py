__author__ = 'jbennett'

from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import PipelineMixin

from storages.backends.s3boto import S3BotoStorage

#TODO test removing CachedFilesMixin
class S3PipelineStorage(PipelineMixin, S3BotoStorage):
    pass
