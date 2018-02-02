#!/usr/bin/python3
from datetime import datetime
import re
import sys
from jira import JIRA

def connect_jira(jira_username,jira_pass,inc_start_date,inc_end_date):
    
    options = {'server': server_add}
    jira = JIRA(options, basic_auth=(jira_username,jira_pass))
    query = 'project = BAT AND "SR Type" in (Event, Incident) AND created >= '+inc_start_date+' AND created <= '+inc_end_date+' AND reporter in (ranjitha.b, paysup, maha.g, r.dhanakkodi, rprabha.rao, amar.c, siva.y, pratiq.kaul, pradeep.c, vinod.kandru, mahesh3.d, ghause.mr, ajit.km, mani.kanta, shub.kumar, r.asmath) ORDER BY environment ASC, key DESC'
    all_issues = jira.search_issues(query)
    regexing(all_issues)


def regexing(all_issues):
    jira_link = server_add + "/browse/"
    listy = [[] for i in range(len(all_issues))]
    regex_time1 = re.compile(r'Duration.*?(\d\d\d\d)-(\d\d)-(\d\d).*(\d\d):(\d\d).*?(\d\d\d\d)-(\d\d)-(\d\d).*?(\d\d):(\d\d).*?Description', re.S)
    regex_time2 = re.compile(r'Duration.*?(\d\d\d\d)-(\d\d)-(\d\d).*?(\d\d):(\d\d).*?(\d\d):(\d\d).*?Description', re.S)
    regex_cr = re.compile(r'Resolution\](.*?)\[Other',re.S)
    for each_issue in list(range(len(all_issues))):
        str_desc = str(all_issues[each_issue].fields.description)
        jira_link_issue = '<a href="' + jira_link+all_issues[each_issue].key+'">'+ all_issues[each_issue].key  + '</a>'
        listy[each_issue].append(jira_link_issue)
        listy[each_issue].append(all_issues[each_issue].fields.summary)
        result1 = regex_time1.search(str_desc)
        result2 = regex_time2.search(str_desc)
        cause_res = regex_cr.search(str_desc)
        if result1:
            flag=True
            st_string = ''.join(result1.group(1,2,3,4,5))
            en_string = ''.join(result1.group(6,7,8,9,10))
            event_time = getdate(st_string, en_string, flag)
            listy[each_issue].append(event_time)
        elif result2:
            flag=False
            st_string = ''.join(result2.group(1,2,3,4,5))
            en_string = ''.join(result2.group(1,2,3,6,7))
            event_time = getdate(st_string, en_string, flag)
            listy[each_issue].append(event_time)
        else:
            listy[each_issue].append("Could not process time")
        if cause_res:
            listy[each_issue].append(str(cause_res.group(1)))
        else:
            listy[each_issue].append("Could not process Cause and Res") 
    
    writetohtml(listy)
    
def getdate(st_string, en_string, flag):
    start_time = datetime.strptime(st_string, "%Y%m%d%H%M")
    end_time = datetime.strptime(en_string, "%Y%m%d%H%M")
    duration = end_time - start_time
    start_time_str = str(start_time)
    end_time_str = str(end_time)
    duration_str= str(duration)
    if flag:
        event_time = "Duration: " + duration_str[:-3] + " [ " + start_time_str[:-3] + " ~ "+ end_time_str[:-3] + " UTC ]"
    else:
        event_time = "Duration: " + duration_str[:-3] + " [ " + start_time_str[:-3] + " ~ "+ end_time_str[11:16] + " UTC ]"
    return event_time


def writetohtml(listy):
    html_st = """ <!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    font-size: 75%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 5px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>

<table>"""
    html_en = """</table>

</body>
</html> """
    
    with open('output.html', 'w') as htmlfile:
        htmlfile.write(html_st)
        for p in range(len(listy)):
            htmlfile.write("<tr>")
            for k in range(4):
              
                htmlfile.write('<th>{0}</th>'.format(listy[p][k]))
            htmlfile.write("</tr>")
        htmlfile.write(html_en)

jira_username = str(sys.argv[1])
jira_pass = str(sys.argv[2])
inc_start_date = str(sys.argv[3])
inc_end_date = str(sys.argv[4])
server_add = str(sys.argv[5])


connect_jira(jira_username,jira_pass,inc_start_date,inc_end_date)



