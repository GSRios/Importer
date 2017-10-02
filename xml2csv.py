import xml.etree.ElementTree
import sys
from more_itertools import unique_everseen

def xmlparse(mapname, restrict=False, excludeway=[]):
    e = xml.etree.ElementTree.parse(mapname).getroot()
    node = open(str(sys.argv[1])+'.csv', 'w')
    node.write(("%s,%s,%s") % ("ID:ID","Lat","Long \n"))
    coords = {}
    for coord in e.findall('node'):
        osmid = coord.get("id")
        lat = coord.get("lat")
        lon = coord.get("lon")
        attribs={}
        for obj in coord:
            att = obj.attrib
            if len(att) > 0:
                key = att["k"]
                val = att["v"]
                attribs[key]=val
        coords[osmid] = [(lon, lat), attribs]
        node.write(("%s,%s,%s\n") % (osmid, lat, lon))
    node.close()            
  
    relName = str(sys.argv[2])+'.csv'
    rel = open(relName, 'w')
    rel.write(":START_ID,Weight,:END_ID,:TYPE")
    def getNodes(nodes):
        for i in range(0,len(nodes)-1):
            rel.write (("%s,%s,%s,%s") % (nodes[i],20,nodes[i+1],"LINKED_TO\n"))

    waydict = {}
    for way in e.findall('way'):
        osmid = way.get("id")
        attribs={}
        refs=[]
        for obj in way:
            att = obj.attrib
            if "k" in att:
                key = att["k"]
                val = att["v"]
                attribs[key]=val
            if "ref" in att:
                refs.append(att["ref"])
        if restrict==False:
            waydict[osmid] = attribs, refs			
        elif restrict in attribs and attribs[restrict] not in excludeway:
            waydict[osmid] = [attribs, refs]			

    for i in waydict:			 
		attributes = waydict[i][0]
		getNodes(list(waydict[i][1]))
		if 'oneway' not in attributes and 'highway' in attributes and attributes['highway'] != 'motorway':
			getNodes(list(reversed(waydict[i][1])))
		elif 'oneway' in attributes and attributes['oneway'] != 'yes' and attributes['oneway'] != '-1' and  attributes['highway'] != 'motorway':
			getNodes(list(reversed(listwaydict[i][1])))  
    rel.close()

    with open(relName,'r') as f, open('new_'+relName,'w') as out_file:
        out_file.writelines(unique_everseen(f))
    

result = xmlparse(str(sys.argv[0])'.osm')


