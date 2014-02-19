import csv
from CECSAM.models import *
def import():
	with open('/home/vagrant/app/CECS Asset Info Spring 2014.csv', 'rb') as csvfile:
		cvr = csv.reader(csvfile, delimiter=',', quotechar='"')
		building = (0, "")
		location = (0, "")
		for row in cvr:
			if location[1] == row[2].split("_")[1]:
					a = Asset(tag = str(row[0]), description = str(row[1]), location=location[0], serialId = str(row[3]), model=str(row[4]), found=False)
					a.save()
			else:
				if row[2].split("_")[0] == building[1]:
					l = Location(building=building[0], room=str(row[2].split("_")[1]))
					l.save()
					location = (l, row[2].split("_")[1])
                                        a = Asset(tag = str(row[0]), description = str(row[1]), location=location[0], serialId = str(row[3]), model=str(row[4]), found=False)
					a.save()
				else:
					b = Building(name=str(row[2].split("_")[0]))
					b.save()
					building = (b, row[2].split("_")[0])
					l = Location(building=building[0], room=str(row[2].split("_")[1]))
					l.save()
					location = (l, row[2].split("_")[1])
                                        a = Asset(tag = str(row[0]), description = str(row[1]), location=location[0], serialId = str(row[3]), model=str(row[4]), found=False)
					a.save()
