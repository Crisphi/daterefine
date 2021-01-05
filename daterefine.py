
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:34:11 2020

@author: Cristian Ortega Singer
"""

import csv
import os
from collections import OrderedDict

os.chdir("./ToCheck") #replace with path to directory where the data sets to be processed are stored
path = os.getcwd()
files = []
files = os.listdir(path)
exceptions = {} #dict with all exceptions; can be exported if needed; right now the script doesn't export it
rows = []
newKeyOrder = ['Branch', 'File Name', 'Image ID', 'Artist', 'Surname', 'First Name', 'Epitheton', 'GND-Number', 'Title', 'Iconography', 'Part', 'Earliest Date', 'Latest Date', 'Date', 'Margin Years', 'Genre', 'Material', 'Medium', 'Height of Image Field', 'Width of Image Field', 'Type of Object', 'Height of Object', 'Width of Object', 'Diameter of Object', 'Position of Depiction on Object', 'Current Location', 'Repository Number', 'Original Location', 'Original Place', 'Original Position', 'Context', 'Place of Discovery', 'Place of Manufacture', 'Associated Scenes', 'Object Categories', 'Related Works of Art', 'Type of Similarity', 'Inscription', 'Text Source', 'Bibliography', 'Photo Archive', 'Image Credits', 'Details URL', 'Additional Information']

#helper function for reordering of ordered dict
def reorder_ordereddict(od, new_key_order):
    new_od = OrderedDict([(k, None) for k in new_key_order if k in od])
    new_od.update(od)
    return new_od

for file in files:
    print(file)
    exceptions[file] = []
    with open(file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            nrow = OrderedDict(row.copy())
            if nrow["Earliest Date"]:
                t1 = nrow["Earliest Date"]
                if nrow["Latest Date"]:
                    t2 = nrow["Latest Date"]
                    try:
                        int(t1)
                        int(t2)
                    except:
                        entry = {"file": file, "row": row}
                        exceptions[file].append(entry)
                        nrow["Date"] = "EXCEPTION"
                    else:
                        if int(t1) > int(t2):
                            t1 = nrow["Earliest Date"]
                            t2 = nrow["Latest Date"]
                            entry = {"file": file, "row": row}
                            exceptions[file].append(entry)
                            nrow["Date"] = "EXCEPTION"
                        else:
                            t1 = nrow["Earliest Date"]
                            t2 = nrow["Latest Date"]
                            tjoin = t1 + "/" + t2
                            nrow["Date"] = tjoin
                else:
                    try:
                        int(nrow["Earliest Date"])
                    except:
                        entry = {"file": file, "row": row}
                        exceptions[file].append(entry)
                        nrow["Date"] = "EXCEPTION"
                    else:
                        nrow["Date"] = nrow["Earliest Date"]
            else:
                nrow["Date"] = None

            rows.append(nrow)
    print("Exceptions for: "+ file +"\n-------------------------")
    for x in exceptions[file]:
        print(x["row"]["Earliest Date"], x["row"]["Latest Date"])
    print("-------------------------")

    for od in rows:
        reorder_ordereddict(od, newKeyOrder)

    os.chdir("../dateRefined") #replace with path to directory where refined data sets should be saved
    filename = "dateRefined-" + file
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames= newKeyOrder)

        writer.writeheader()
        for x in rows:
            writer.writerow(x)
    rows = []
    os.chdir("../ToCheck") #replace with path to directory where the data sets to be processed are stored

os.chdir("../dateRefined")
with open("exceptions.txt", "w") as txtfile:
    txtfile.write("\n----------------------------------\nExceptions\n----------------------------------\n\n")
    for x in exceptions.keys():
        num = len(exceptions[x])
        if num > 0:
            txtfile.write(x + ":"+"\n"+ str(num) + "\n----\n")
    txtfile.write("\n----------------------------------\nNo Exceptions found\n----------------------------------\n\n")
    for x in exceptions.keys():
        num = len(exceptions[x])
        if num == 0:
            txtfile.write(x + ":"+"\n"+ str(num) + "\n----\n")
