from flask import Flask
import base64
import sqlite3
import socket
import requests

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getTravelTime(latLong1, latLong2):
	waypoint ="geo!" + latLong1
	waypoint2 ="geo!" + latLong2
	print waypoint + ", " + waypoint2
	payload = {'app_id': 'devportal-demo-20180625', 'app_code': '9v2BkviRwi9Ot26kp2IysQ', 'waypoint0': waypoint, 'waypoint1': waypoint2, 'mode': "fastest;truck;traffic:disabled", 'limitedWeight': 30.5, 'height': 4.25, 'shippedHazardousGoods': "harmfulToWater"}
	r = requests.post('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload)
	out = r.text
	i = out.find("summary")
	out = out[i:]
	i = out.find("travelTime") + 12
	j = out.find(",\"_type")
	out = out[i:j]
	return out


port = 5000
app = Flask(__name__, static_url_path='')
@app.route('/')
def hello_world():
        conn = sqlite3.connect('/home/pi/flask/cargo.db')
	c = conn.cursor()
	conn.text_factory = str
	ip = get_ip() + ":" + str(port)
	urls = "<h2>Active Cargo:</h2><h4>Click any link to check status!</h4><br />"
	for x in range(4):
		c.execute("SELECT name FROM val WHERE id = %d"%x)
        	name = c.fetchone()
		name = str(name[0])
		path = base64.b64encode(name.encode())
		urls = urls + "Shipment ID: " + str(x) + " - Shipment Alias: " + name + ":    " + "<a href=\"http://" + ip + "/status/" + path + "\">Link</a>" + "<br />"
	conn.commit()
	conn.close()
	return urls

@app.route('/arrival/<name>') #MD5 hash of the Margaritaville
def cargoCheckIn(name):
	conn = sqlite3.connect('/home/pi/flask/cargo.db')
	c = conn.cursor()
	name = str(base64.b64decode(name))
	c.execute("SELECT id FROM val WHERE name =%s"%("\"" + name + "\""))
	id = c.fetchone()
	id = int(id[0])
	c.execute("UPDATE val SET status = 'arrived' WHERE id = %d"%id)
	conn.commit()
	conn.close()
	return 'Cargo status for ' + name + ' updated to \"Arrived\"!'

@app.route('/status/<name>') #B64 of name
def cargoCheck(name):
        conn = sqlite3.connect('/home/pi/flask/cargo.db')
        c = conn.cursor()
        name = str(base64.b64decode(name))
        c.execute("SELECT id FROM val WHERE name =%s"%("\"" + name + "\""))
        id = c.fetchone()
        id = int(id[0])
	c.execute("SELECT cargo FROM val WHERE id = %d"%id)
        cargo = c.fetchone()
        cargo = str(cargo[0])
	c.execute("SELECT startPlace FROM val WHERE id = %d"%id)
        start = c.fetchone()
        start = str(start[0])
	c.execute("SELECT endPlace FROM val WHERE id = %d"%id)
        end = c.fetchone()
        end = str(end[0])
	c.execute("SELECT status FROM val WHERE id = %d"%id)
        statusS = c.fetchone()
        statusS = str(statusS[0])
	c.execute("SELECT startCoord FROM val WHERE id = %d"%id)
        startcor = c.fetchone()
        startcor = str(startcor[0])
	print startcor
	c.execute("SELECT endCoord FROM val WHERE id = %d"%id)
        endcor = c.fetchone()
        endcor = str(endcor[0])
	print endcor
	tT = str(getTravelTime(startcor, endcor))

	status = '''<table><thead><tr>
            <th colspan="2">Shipment Status</th>
        </tr></thead><tbody>'''
        status = status + "<tr><th>Cargo ID:</th>" + "<td>" + str(id)  + "</td>"
	status = status + "<tr><th>Cargo Name:</th>" + "<td>" + name  + "</td>"
	status = status + "<tr><th>Cargo Contents:</th>" + "<td>" + cargo  + "</td>"
	status = status + "<tr><th>Cargo Will Arrive at:</th>" + "<td>" + start  + "</td>"
	status = status + "<tr><th>Cargo Will be Shipped to:</th>" + "<td>" + end  + "</td>"
	status = status + "<tr><th>Cargo Travel Time(Min):</th>" + "<td>" + tT  + "</td>"
	status = status + "<tr><th>Cargo Status:</th>" + "<td>" + statusS  + "</td>"
	status = status + "</tbody></table>"
	conn.commit()
        conn.close()
        return status



if __name__ == '__main__':
    app.run(host='0.0.0.0')
