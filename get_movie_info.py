import requests
import json

filename = raw_input("Filename: ")
tit_count = 0

nl_io = open(filename, 'r')
for line in nl_io:
    tit_count+=1
nl_io.close()

fio = open(filename, 'r')
json_file = open("json_movies.txt", 'a+')

s_count = 0
p_count = 0

for line in fio:
    p_count += 1
    url_req = "http://www.omdbapi.com/?t="+line+"&y=&plot=short&r=json&tomatoes=True"
    response = requests.get(url_req)
    try:
        parsed_resp = response.json()
        if parsed_resp['Response'] == 'True':
            s_count+=1
            d = {
                'title':parsed_resp['Title'],
                'year':parsed_resp['Year'],
                'rt_rat':parsed_resp['tomatoMeter'],
                'runtime':parsed_resp['Runtime'],
                'plot':parsed_resp['Plot'],
                'poster_url':parsed_resp['Poster']
            }
            json_file.write(json.dumps(d)+'\n')
            print "%d: Success" % p_count
        else:
            print "%d: Failure" % p_count
    except ValueError:
        print "ValueError in JSON processing. Title Skipped."

print "Success rate: %d" % s_count
fio.close()

json_file.close()
