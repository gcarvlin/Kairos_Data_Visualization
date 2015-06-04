#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"Fetch Dylos averages from KairosDB"

import StringIO, pycurl, json, csv, sys, time
from datetime import datetime

# Initialize variables
#
URL = "https://replicant.deohs.washington.edu/api/v1/datapoints/query"
CACERT = "C:\Users\Admin\Desktop\cacert4.pem"
AUTH = "query:treelimberice7"
DYLOS_UNITS = sys.argv[1].split(",")
BINS = sys.argv[2].split(",")
T_FROM = sys.argv[3]
T_TO = sys.argv[4]
OUT_DIR = "C:\Users\Admin\Desktop"
out_array = [['Timestamp']]
output_dict = {}
num_tags = 0

# Functions
#
def prep_query(u_name):
    "This prepares a data structure to send in JSON format"
    query_data = {"start_absolute": T_FROM, "end_absolute": T_TO, "metrics" : prep_metrics(u_name)}
    #print query_data
    return query_data

def prep_metrics(u_name):
    "Prepare metrics"
    prep_out_array = []
    for i in range(0,len(BINS)):
        prep_out_array.append({"name":u_name, "tags": {"Bin":BINS[i]}})
    return prep_out_array

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
    
    return json.loads(buf.getvalue())
    
def buf_to_dict(buffer,u_name):
    global output_dict
    global out_array
    global num_tags
    
    #get number of tags in out_array
    if (len(out_array)==0):
        num_tags = 0
    else:
        num_tags = len(out_array[0])-1
    #print num_tags
    
    #try to parse the buffer and write it to a file
    #try:
        #if buffer is empty write one line of NAs to file
    if (buffer['queries'][0]['sample_size']==0):
        #sys.stdout.write("Empty")
        placeholder = 1;
    #otherwise parse buffer
    else:
        num_queries = len(buffer['queries'])
        #print num_queries
        current_tags = []
        #loop through all queries (i.e. bin1, bin2, bin3...)
        for q in range(0,num_queries):
            tag_name = buffer['queries'][q]['results'][0]['tags'].values()[0][0].capitalize()
            current_tags.append(tag_name)
            num_values = len(buffer['queries'][q]['results'][0]['values'])
            #loop through all values (i.e. [timestamp, value1],[timestamp, value2]...)
            for v in range(0,num_values):
                key = buffer['queries'][q]['results'][0]['values'][v][0]
                value = buffer['queries'][q]['results'][0]['values'][v][1]
                #if the key does not exist then add a default value of "NA"
                if not (key in output_dict):
                    na_list = []
                    for x in range(0,num_queries+num_tags):
                        na_list.append('null')
                    output_dict[key] = na_list
                elif (q==0): #if key exists and we are on a fresh Dylos append the correct number of NAs
                    for x in range(0,num_queries):
                        output_dict[key].append('null')
                #save value to the correct offset in list; offsets represent the different queries {ts: [bin1_val, bin2_val...]}
                if ((q+num_tags-1)>len(output_dict[key])-1):
                    t_num = q+num_tags
                    print ("Problem at timestamp: %s\nValues in the array for that timestamp are: %s\nLength of array: %s\nLooking for index: %s\n" % (key, output_dict[key], len(output_dict[key]), t_num))
                    print "Pausing operation for 30 seconds for debug.  Press ctrl-C to end."
                    time.sleep(30)
                else:
                    output_dict[key][q+num_tags] = str(value)
        #Add tags from this Dylos to the final output array header
        header1 = []   #,','.join(l_tags),',Flag'  #deprecated
        for i in range(0,len(current_tags)):
            header1.append(str(u_name+" "+current_tags[i]))
            #header1.append('Flag')  #uncomment for flags
        if (len(out_array)==0):
            out_array.append(header1)
        else:
            for i in range(0,len(header1)):
                out_array[0].append(header1[i])

def format_output():
    global output_dict
    sorted_keys = sorted(output_dict)
    for item in sorted_keys:
        item_string = []
        item_string.append(datetime.fromtimestamp(item/1000).strftime("%H:%M %m/%d/%y"))
        for i in range(0,len(output_dict[item])):
            #print output_dict[item][i]
            if (output_dict[item][i]=='null'):
                item_string.append(1.1)
            else:
                item_string.append(round(float(output_dict[item][i])))
        #item_string.append(0)  #uncomment for flags
        out_array.append(item_string)
        #print item_string
    print out_array

# Loop through each Dylos unit
for dylos in DYLOS_UNITS:
    buffer = send_query(prep_query(dylos),dylos)
    buf_to_dict(buffer,dylos)

format_output()


