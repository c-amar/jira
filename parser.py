#!/usr/bin/python3
from datetime import datetime
import re
import xml.etree.ElementTree as ET
import sys
import csv

html_st = """ <!DOCTYPE html>
<html>
<body>

<table style="width:100%">"""
html_en = """</table>

</body>
</html> """

def regex(Title, Desc, listy):
    i = len(Title)
    reex1 = re.compile(r'Duration.*?(\d\d\d\d)-(\d\d)-(\d\d).*(\d\d):(\d\d).*?(\d\d\d\d)-(\d\d)-(\d\d).*?(\d\d):(\d\d).*?Description', re.S)
    reex2 = re.compile(r'Duration.*?(\d\d\d\d)-(\d\d)-(\d\d).*?(\d\d):(\d\d).*?(\d\d):(\d\d).*?Description', re.S)
    reex_cr = re.compile(r'&#91;Cause &amp; Resolution&#93;(.*?)&#91;Other Info',re.S)
    for each in list(range(i)):
        str_desc = str(Desc[each])
        result1 = reex1.search(str_desc)
        result2 = reex2.search(str_desc)
        obj2 = reex_cr.search(str_desc)
        if result1:
            st_string = ''.join(result1.group(1,2,3,4,5))
            en_string = ''.join(result1.group(6,7,8,9,10))
            setarray(st_string, en_string, listy, Title[each], Desc[each],each,obj2)
            
        elif result2:
            st_string = ''.join(result2.group(1,2,3,4,5))
            en_string = ''.join(result2.group(1,2,3,6,7))
            setarray(st_string, en_string, listy, Title[each], Desc[each],each,obj2)
			
        else:
            listy[each].append(str(Title[each]))
            listy[each].append("Could not process time")
            if obj2:
                listy[each].append(cleanxml(str(obj2.group(1))))
            else:
                listy[each].append("Could not parse Cause and Res")
    return listy


def cleanxml(raw_text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_text)
  return cleantext


def xml_parser(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    Title = []
    Desc = []
    for item in root.findall("./channel/item"):
        for child in item:
            if child.tag == "title":
                Title.append(child.text)
            elif child.tag == "description":
                Desc.append(child.text)
    if len(Title) == len(Desc):
        listy = [[] for i in range(len(Title))]
        regex(Title, Desc, listy)
        writetocsv(listy)
	
def setarray(st_string, en_string, listy, Title_st, Desc_st,each,obj2):
    start_time = datetime.strptime(st_string, "%Y%m%d%H%M")
    end_time = datetime.strptime(en_string, "%Y%m%d%H%M")
    duration = end_time - start_time
    listy[each].append(str(Title_st))
    listy[each].append(str(duration))
    if obj2:
        listy[each].append(cleanxml(str(obj2.group(1))))
    else:
        listy[each].append("Could not parse Cause and Res")
	


def writetohtml(listy):

    with open('output.html', 'w') as htmlfile:
        htmlfile.write(html_st)
        for p in range(len(listy)):
            htmlfile.write("<tr>")
            for k in range(3):
                
                htmlfile.write('<th>{0}</th>'.format(listy[p][k]))
            htmlfile.write("</tr>")
        htmlfile.write(html_en)
	
def writetocsv(listy):
    with open('parsedout.csv', 'w') as f:
        writer = csv.writer(f) 
        writer.writerows(listy)
    writetohtml(listy)	
		
xml_parser(str(sys.argv[1]))



html_st = """ <!DOCTYPE html>
<html>
<body>

<table style="width:100%">"""
html_en = """</table>

</body>
</html> """

