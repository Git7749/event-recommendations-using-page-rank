from flask import Flask, render_template, url_for, request, redirect, json
from SPARQLWrapper import SPARQLWrapper, JSON
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from flask import Flask, render_template, json, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',tasks=[])

@app.route('/users/search', methods=['POST'])
def search():
    search_pattern = request.form['search_term'].strip()
    print(search_pattern)
    sparql = SPARQLWrapper("http://18.222.233.173:3030/recommend/query")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rec: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/untitled-ontology-10#>
        PREFIX user: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/users#>
        SELECT ?s
        WHERE {
            ?u rdf:type rec:user.
            ?u user:has_id ?s.
            ?u rec:has_popularity_score ?score
            FILTER regex(?s,'"""+search_pattern+"""',"i")
        }
        ORDER BY DESC(?score)
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cols = results["head"]["vars"]
    data = results["results"]["bindings"]
    users = []
    for i in range(len(data)):
        users.append({"id": data[i][cols[0]]['value'], "name": data[i][cols[0]]['value']})
    # print(users)
    # users = '[{"id":"1", "name" : "kumar"}, {"id":"2" ,"name" : "divya"},{"id":"3" , "name": "rohit"}]'
    print(users)
    # tasks = json.loads(users)
    return render_template('index.html', tasks=users)

@app.route('/recommend', methods=['GET'])
def recommendations():
    user_id = request.args.get('userid')
    print(user_id)
    print("******************************************************************")
    sparql = SPARQLWrapper("http://18.222.233.173:3030/recommend/query")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rec: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/untitled-ontology-10#>
        PREFIX user: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/users#>
        PREFIX event: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/untitled-ontology-9#>
        PREFIX eve: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/event#>
        PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
        PREFIX re: <http://www.w3.org/2000/10/swap/reason#>
        PREFIX ex: <http://example.org/>
        PREFIX ev: <http://www.w3.org/2001/xml-events/>
        SELECT ?user ?event_id ?friend_id ?score
        WHERE {
          ?user rdf:type rec:user.
          ?user user:has_id '"""+user_id+"""'.
          ?user rec:has_friends ?friend.
          ?friend user:has_id ?friend_id.
          ?friend rec:has_popularity_score ?score.
          ?friend user:interested_in_event ?event_id
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cols = results["head"]["vars"]
    data = results["results"]["bindings"]
    # print(data)
    users = []
    for i in range(len(data)):
        users.append({"event":data[i]['event_id']['value'], "friend":data[i]['friend_id']['value'], "score":data[i]['score']['value']})
    print(users)

    # events = '[{"id":"11", "name" : "sun burn"}, {"id":"12" ,"name" : "kochela"},{"id":"13" , "name": "sreemantam"}]'
    # tasks = json.loads(events)
    return render_template('events.html', tasks=users)

@app.route('/event', methods=['GET'])
def event():
    event_id = request.args.get('id')
    print(event_id)
    # print("******************************************************************")
    sparql = SPARQLWrapper("http://18.216.61.64:3030/event/query")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rec: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/untitled-ontology-10#>
        PREFIX user: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/users#>
        PREFIX event: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/untitled-ontology-9#>
        PREFIX eve: <http://www.semanticweb.org/dpolinen/ontologies/2020/10/event#>
        PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
        PREFIX re: <http://www.w3.org/2000/10/swap/reason#>
        PREFIX ex: <http://example.org/>
        PREFIX ev: <http://www.w3.org/2001/xml-events/>
        SELECT ?event ?event_id ?address ?lat ?lng ?score
        WHERE {
  			?event rdf:type event:Event.
  			?event event:has_event_id '"""+event_id+"""'.
  			?event event:has_event_id ?event_id.
  			?event event:at_location ?location.
            ?event eve:has_score ?score.
  			?location event:has_location_name ?address.
  			?location event:has_latitude ?lat.
  			?location event:has_longitude ?lng.
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cols = results["head"]["vars"]
    data = results["results"]["bindings"]
    event = []
    print(data)
    for i in range(len(data)):
        event.append({"event":data[i]['event_id']['value'],
                        "location":data[i]['address']['value'],
                        "Coordinates":data[i]['lat']['value']+","+data[i]['lng']['value'],
                        "score": data[i]['score']['value']})
    return render_template("hotels.html", tasks = event)

if __name__ == "__main__":
    app.run(debug=True)
