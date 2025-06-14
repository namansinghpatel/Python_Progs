import csv

#declare rows
rows = [["foo", "bar", "spam"],
       ["oof", "rab", "maps"],
       ["writerow", "isn't", "writerows"]]

filename = "university_records.csv"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)