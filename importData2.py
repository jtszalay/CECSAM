import csv
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
import datetime
from CECSAM.models import *
def import_data():
    with open('/home/ubuntu/asset.csv', 'rb') as csvfile:
        cvr = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = cvr.next()
        for row in cvr:
            a = Asset.objects.get(tag=row[1])
            a.original_location = row[3]
            a.save()
