from rest_framework.parsers import BaseParser


class CSVFileUploadParser(BaseParser):
    """
    A naive raw file upload parser.
    """
    media_type = '*/*'  # Accept anything

    def parse(self, stream, media_type=None, parser_context=None):
        content = stream.read()
        name = 'example.dat'
        content_type = 'application/octet-stream'
        size = len(content)
        charset = 'utf-8'

        # Write a temporary file based on the request content
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(content)
        uploaded = UploadedFile(temp, name, content_type, size, charset)

        # Return the uploaded file
        data = {}
        files = {name: uploaded}
        return DataAndFiles(data, files)