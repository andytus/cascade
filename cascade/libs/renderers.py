from rest_framework import renderers
import csv
from StringIO import StringIO


class CSVRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    def render(self, data, accepted_media_type=None, renderer_context=None):
       return data

class PDFRenderer(renderers.BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
