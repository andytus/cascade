__author__ = 'jbennett'
#This will be used to pull data form AMCS collection history
#reader = csv.reader(open("/home/jbennett/python_projects/cascade/cascade/apps/collection_manager/fixtures/sample_amcs.txt"), delimiter=' ')

class Parser:

    def __init__(self, file_path):

        self.file = open("/home/jbennett/python_projects/cascade/cascade/apps/collection_manager/fixtures/sample_amcs.txt") #open(file_path)

    def parse(self):
        while 1:
            lines = self.file.readlines(100000)
            if not lines:
                break
            for line in lines:
                print line     # TODO parse file: R 2108 120510123020009610070094 03/03/2014 15:12:24 000000 000000 000000 L N 0 00 0281   39.086793  -84.573372


