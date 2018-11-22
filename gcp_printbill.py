##
## reads a billingfile download in CSV from GCP and adds up the cost per project 
## output is ; delimited shoudl be importable in Excel/Sheets
## arguments: filename mincost project
##   mincost: minimal cost to print, say 100 that way small costs are not listed in output
##            or 1000000 that way none are listed
##   project: pattern for a project, matches a substring, can be useful if a naming convention is followed
##
import sys
import csv
import re

# if there is an argument use as file name - 2nd arg is a minimum price to print - 3 to focus on a project
filename = "gcpbill.csv"
minprice = 0.0
focusproject = ""
if (len(sys.argv)>1):
  filename = sys.argv[1]
if (len(sys.argv)>2):
  minprice = float(sys.argv[2])
if (len(sys.argv)>3):
  focusproject = sys.argv[3]

projectsum = {} 
projectdetail = {} 
sourcepattern = re.compile("\[(.*)\]")

with open(filename, "rb") as infile:
  line = infile.readline()
  if ("Description" in line):
    format = 1 
  else:
    format = 2 
infile.close()

# process each line as a scv, sum up by project, keep each line per project for reporting
with open(filename, "rb") as billcsvfile:
  line = csv.reader(billcsvfile) 
  for lineelements in line:
    print lineelements
    # find the project name
    try:
      if (sourcepattern.search(lineelements[format])):
        project = sourcepattern.search(lineelements[format]).group(1)
      else:
        project = lineelements[format]
      print project
      if project not in projectsum:
        projectsum[project] = 0.0
        projectdetail[project] = {} 
      # remove commas in price string
      try:
        price = lineelements[len(lineelements)-1].replace(",","")
        try:
          if (float(price)>0):
    	    projectsum[project] = projectsum[project] + float(price)
            details = projectdetail[project]
            if (format == 2):
	      details[lineelements[3]+"-"+lineelements[4]] = float(price)
            else:
	      details[lineelements[1]] = float(price)
        except ValueError:
          # there are weird negative number included inteh file not with a real - but some UTF-8 thing, i
          # they dont convert but since we do not need them... 
          pass
      except IndexError:
        pass
    except IndexError:
      pass

  # print highest last
  total = 0
  for project, sum in sorted(projectsum.iteritems(), key=lambda (k,v): (v,k)):
    if ((len(focusproject) == 0) or (focusproject in project)):
      total = total + sum
      print "== %s; %s" % (project, sum)
      # extract the projects details to a new list to be able to sort it
      sortdetail = projectdetail[project] 
      for detail, price in sorted(sortdetail.iteritems(), key=lambda (k,v): (v,k)):
        if (price > minprice):
          print "  %s; %s" % (detail, price)
  print "=== total %s; %s" % (filename, total)
