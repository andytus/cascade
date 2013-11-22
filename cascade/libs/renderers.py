from rest_framework import renderers
import csv
import cStringIO as StringIO

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


class KMLRenderer(renderers.BaseRenderer):
    media_type = 'application/vnd.google-earth.kml+xml'
    format = 'kml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def csv_out(row, index, header):
    csvfile = StringIO.StringIO()
    csv_writer = csv.writer(csvfile)
    if index == 1:
        #here split the header and take the first name if there is only one, else take the second
        #csv_writer.writerow([col.split(".")[0] if len(col.split(".")) == 1 else col.split(".")[1] for col in header])
        csv_writer.writerow([header[col] for col in header.keys()])

    data = []
    for col in header:
        #split the header for call object attributes
        objs = col.split(".")
        if len(objs) == 1:
            #just add the value from the header name
            data.append(str(getattr(row, objs[0])))
        else:
        #Todo depreciate
        #elif len(objs) == 2:
            #get the base object
            base = getattr(row, objs[0])
            if base:
                # if we have a base object then the attribute from the second element of the header
                data.append(str(getattr(base, objs[1])))
            else:
                #if no base object provide and empty string
                data.append("")

    csv_writer.writerow(data)
    #Todo depreciate:
    #csv_writer.writerow([row.id, row.location.street_name, row.location.house_number, row.location.unit,
    #                     row.service_type.code, str(getattr(row.expected_cart, 'rfid', '')),
    #                     row.cart_type.size, row.cart_type])
    return csvfile.getvalue()


def stream_response_generator(data, header):
    index = 0
    for row in data:
        index += 1
        yield csv_out(row, index, header)