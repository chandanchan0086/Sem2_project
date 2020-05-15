import sqlite3
import googlemaps
import webbrowser 
from datetime import datetime
dbfile=r"/home/sahana/Desktop/chandu_sem2/database_f.db"
conn=None
conn=sqlite3.connect(dbfile)
cur=conn.cursor()
gmaps = googlemaps.Client(key='AIzaSyAWiHE0okg-Uro_IxRTgGAvpnP1BYe1uJA')
final_node=[]
def distance(lat1, lat2, lon1, lon2):
	lat1_s=str(lat1)
	lat2_s=str(lat2)
	lon1_s=str(lon1)
	lon2_s=str(lon2)
	origin=(lat1_s+","+lon1_s)
	destination=(lat2_s+","+lon2_s)
	dist = gmaps.distance_matrix(origin,destination, mode="driving", language=None, avoid=None, units=None, departure_time=None, arrival_time=None, transit_mode=None, transit_routing_preference=None, traffic_model=None, region=None)
	dist=((dist["rows"][0]["elements"][0]["distance"]["value"])/1000)
	return(dist) 

def min_distance(bl,tl):
	dis=[]
	for i in tl:
		dis.append([i[0],round(distance(bl[1],i[1],bl[2],i[2]),1)])
	return min_id(dis)
def min_id(dis):
	temp=[]
	for i in dis:
		temp.append(i[1])
	minimum=min(temp)
	identity=dis[temp.index(minimum)][0]
	return [minimum,identity]

def delete(identity,temp_rows):
	#global temp_rows
	for i in temp_rows:
		if i[0]==identity:
			temp_rows.remove(i)
			return i

def shortest_path(table_name):
	laat=13.4230
	loon=77.1481
	qur="select *from "+table_name+";"
	cur.execute(qur)
	rows=cur.fetchall()
	temp_rows=rows.copy()

	spl=(0,laat,loon)
	d_spl=[]
	final_dist=[]
	#final_node=[]
	bl=spl
	tl=rows
	
	for i in range(len(rows)):
		value=min_distance(bl,tl)
		final_dist.append(value[0])
		final_node.append(value[1])
		bl=delete(value[1],temp_rows)
		tl=temp_rows
	final_node.insert(0,0)
	final_node.append(0)
	last2=final_node[-2]
	for ele in rows:
		if(ele[0]==last2):
			final_dist.append(round(distance(spl[1],ele[1],spl[2],ele[2]),1))
	print(final_dist,final_node)
	total_dist=sum(final_dist)
	print(total_dist," Kms")
	maps("dup")
	return

def maps(table_name):
	
	qur="select ID,LATITUDE,LONGITUDE from "+table_name+";"
	cur.execute(qur)
	rows=cur.fetchall()
	node_m=final_node
	node_m.pop(0)
	node_m.pop(-1)
	length=len(node_m)
	#print(node_m)
	map_node=[]
	#print(len(rows))
	for i in node_m:
		for j in range(0,length):
			if(i == rows[j][0] ):
				map_node.append(rows[j])
	#URL format
	#https://www.google.com/maps/dir/?api=1&origin=&destination=&travelmode=driving&waypoints=%7C%7C%7C'
	
	base="https://www.google.com/maps/dir/?api=1&origin=13.4230,77.1481&destination=13.4230,77.1481&travelmode=driving&waypoints="
	count=1;
	for i in map_node:
		lat=str(i[1])
		lon=str(i[2])
		base=base+lat+","+lon
		if(count==length):
			break;
		base=base+"%7C"
		count=count+1
		
	#print(base)
	webbrowser.open(base)
	return
def drop(table_name):
	qur="DROP TABLE "+table_name +";"
	try:
		cur.execute(qur)
	except:
		print("\nno such table")
	return
def create(table_name):
	qur="CREATE TABLE "+table_name+"(ID INTEGER PRIMARY KEY AUTOINCREMENT,LATITUDE FLOAT,LONGITUDE FLOAT,ADDRESS TEXT,GARBAGE_LEVEL FLOAT);"
	cur.execute(qur)
	return

def insert(num_data,table_name):
	for i in range(num_data):
		qur="insert into "+table_name+"(LATITUDE,LONGITUDE,ADDRESS) values({},{},{})"
		lat=float(input("Enter LATITUDE of a location= "))
		lng=float(input("Enter LONGITUDE of a location= "))
		print('\n###__NOTE:- Enter Address with in the "your address"__###')
		addr=input("Enter ADDRESS of the location= ")
		qur=qur.format(lat,lng,addr)
		cur.execute(qur)
	conn.commit()
def update(table_name):
	qur="select *from "+table_name+";"
	cur.execute(qur)
	count=len(cur.fetchall())
	for lim in range(1,count+1):
		print("\nEnter the Gargage Level of:-\nBin-",lim)
		garbage=input("--->")
		lim=str(lim)
		qur="UPDATE "+table_name+" SET GARBAGE_LEVEL = "+garbage+"  WHERE ID ="+lim+";"
		qur=str(qur)
		cur.execute(qur)
		lim=int(lim)
	conn.commit()
	return
def disp(table_name):
	qur="select *from "+table_name+";"
	cur.execute(qur)
	rows=cur.fetchall()
	for row in rows:
		print(row[:])
def dele(table_name,threshold):
	threshold=str(threshold)
	qur="DELETE FROM dup;"
	cur.execute(qur)
	qur="INSERT INTO dup SELECT * FROM "+table_name+";"
	cur.execute(qur)
	qur="DELETE FROM dup WHERE GARBAGE_LEVEL < "+threshold+";"
	cur.execute(qur)
	conn.commit()
	return

print("_____________________________________________________________________")
print("\n          Manipal Academy of Higher Education")
print("          MANIPAL SCHOOL OF INFORMATION SCIENCE")
print("PROJECT TITTLE ::\n\t\tSMART WASTE MANAGEMENT SYSTEM WITH ROUTE OPTIMIZATION\n")
while(1):
	print("PRESS\n\t0->DROP\n\t1->CREATE\n\t2->INSERT\n\t3->UPDATE\n\t4->DISPLAY\n\t5->DELETE(GARBAGE_LEVEL < threshold)\n\t6->SHORTEST_PATH\n\t7->EXIT\n\n")
	key=int(input("ENTER THE OPERATION: "))
	if key == 0:
		table_name=input("Enter table name to DROP: ")
		drop(table_name)
	elif key == 1:
		table_name=input("\nEnter table name to CREATE: ")
		create(table_name)
	elif key == 2:
		num_data=int(input("\nEnter Num of data to INSERT: "))
		table_name=input("\nEnter table name to INSERT: ")
		insert(num_data,table_name)
	elif key == 3:
		table_name=input("\nEnter table name to UPDATE: ")
		update(table_name)
	elif key == 4:
		table_name=input("\nEnter table name to DISPLAY: ")
		disp(table_name)
	elif key == 5:
		threshold=int(input("\nEnter the THRESHOLD level of GARBAGE = "))
		table_name=input("\nEnter table name to DELETE(GARBAGE_LEVEL < threshold): ")
		dele(table_name,threshold)
	elif key == 6:
		final_node=[]
		table_name=input("\nEnter table name to find SHORTEST_PATH: ")
		shortest_path(table_name)
	elif key == 7:
		print("\nOperation completed")
		print("\nThank you\n")
		break
	print("\nOperation completed")

conn.close()

