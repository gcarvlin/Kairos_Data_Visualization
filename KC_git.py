#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"Fetch Dylos averages from KairosDB"

import StringIO, pycurl, json, csv, sys
from datetime import datetime

# Initialize variables
#
URL = "URL"
CACERT = "PATH"
AUTH = "USER:PASS"
DYLOS_UNITS = sys.argv[1].split(",")
BINS = sys.argv[2].split(",")
T_FROM = sys.argv[3]
T_TO = sys.argv[4]
OUT_DIR = "OUT"

with open("C:\log.txt", "w") as f:
    f.write("Dylos units: %s\nBins: %s\nFrom: %s\nTo: %s" % (DYLOS_UNITS, BINS,T_FROM,T_TO));

# Functions
#
def prep_query(u_name):
    "This prepares a data structure to send in JSON format"
    query_data = {"start_absolute": T_FROM, "end_absolute": T_TO, "metrics" : prep_metrics(u_name)}
    #print query_data
    return query_data

def prep_metrics(u_name):
    "Prepare metrics"
    out_array = []
    for i in range(0,len(BINS)):
        out_array.append({"name":u_name, "tags": {"Bin":BINS[i]}})
    return out_array

def send_query(db_query, u_name):
    "This sends out individual queries using pycurl which calls libcurl"
    buf = StringIO.StringIO()
    req = pycurl.Curl()
    req.setopt(req.URL, URL)
    req.setopt(req.CAINFO, CACERT)
    req.setopt(req.USERPWD, AUTH)
    req.setopt(req.POSTFIELDS, json.dumps(db_query))
    req.setopt(req.WRITEDATA, buf)
    req.setopt(req.POST, 1L)
    req.perform()
    req.close()
    
    
    #try to parse the buffer and write it to a file
    #try:
        #if buffer is empty write one line of NAs to file
    if (json.loads(buf.getvalue())['queries'][0]['sample_size']==0):
        #sys.stdout.write("Empty")
        placeholder = 1;
    #otherwise parse buffer
    else:
        num_queries = len(json.loads(buf.getvalue())['queries'])
        l_tags = []
        output_dict = {}
        #loop through all queries (i.e. bin1, bin2, bin3...)
        for q in range(0,num_queries):
            tag_name = json.loads(buf.getvalue())['queries'][q]['results'][0]['tags'].values()[0][0].capitalize()
            l_tags.append(tag_name)
            num_values = len(json.loads(buf.getvalue())['queries'][q]['results'][0]['values'])
            #loop through all values (i.e. [timestamp, value1],[timestamp, value2]...)
            for v in range(0,num_values):
                key = json.loads(buf.getvalue())['queries'][q]['results'][0]['values'][v][0]
                value = json.loads(buf.getvalue())['queries'][q]['results'][0]['values'][v][1]
                #if the key does not exist then add a default value of "NA"
                if not (key in output_dict):
                    na_list = []
                    for x in range(0,num_queries):
                        na_list.append('NA')
                    output_dict[key] = na_list
                #save value to the correct offset in list; offsets represent the different queries {ts: [bin1_val, bin2_val...]}
                output_dict[key][q] = str(value)
        sorted_keys = sorted(output_dict)
        #return as an array (stdout??)
        out_array = []
        header1 = ['Timestamp']   #,','.join(l_tags),',Flag'
        for i in range(0,len(l_tags)):
            header1.append(str(u_name+" "+l_tags[i]))
        #header1.append('Flag')  #uncomment for flags
        out_array.append(header1)
        #print header1
        for item in sorted_keys:
            item_string = []
            item_string.append(datetime.fromtimestamp(item/1000).strftime("%H:%M %m/%d/%y"))
            for i in range(0,len(output_dict[item])):
                item_string.append(round(float(output_dict[item][i])))
            #item_string.append(0)  #uncomment for flags
            out_array.append(item_string)
            #print item_string
        print out_array
    #if we cannot parse the values write Err1 to the file
    #except:
        #print "Exception Error"

# Loop through each Dylos unit
for dylos in DYLOS_UNITS:
    send_query(prep_query(dylos),dylos)