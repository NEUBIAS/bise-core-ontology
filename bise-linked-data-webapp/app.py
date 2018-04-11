import csv
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

from string import Template

from rdflib import ConjunctiveGraph

app = Flask(__name__)

# client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)

ns = {"biii": "http://bise-eu.info/core-ontology#",
      "p-plan": "http://purl.org/net/p-plan#",
      "edam": "http://purl.obolibrary.org/obo/edam#"}

client = MongoClient(host=['localhost:27017'])
db = client.tododb
icanDb = client.ican_sandbox

g = ConjunctiveGraph()
g.parse("static/data/neubias-dump-20180129.ttl",
        format="turtle")
g.parse("static/data/EDAM-bioimaging_alpha03.owl")
g.parse("static/data/sample_biii_workflow.ttl",
        format="turtle")

print(str(len(g)) + ' triples in Biii data graph')

# my_template = Template("Hello, ${person_name}, how are you?")
# for name in ['Jane', 'Bob', 'Dan']:
#     print(my_template.substitute(person_name=name))

@app.route('/graphQ4')
def graphQ4():
    tbl = []
    qres = g.query(
        """       
	SELECT ?label (count(distinct ?s1) as ?soft_count) 
	WHERE { 
	    ?s1 a <http://biii.eu/node/software> .
	    ?s1 biii:hasTopic ?edam_class .
	    ?edam_class rdfs:label ?label .
	}
	GROUP BY ?edam_class ?label
 
	ORDER BY DESC(?soft_count)

        """, initNs=ns)

    for row in qres:
        tbl.append({"name": row['label'],"count":row['soft_count']})

    return render_template('testQ4.html', tbl=tbl)



## Demo Workflow 1
@app.route('/sparql')
def sparql():
    return render_template('sparql.html')

## Demo Workflow 1
@app.route('/graph')
def graph():
    # list_of_nodes = [{"label": "node1"},
    #          {"label": "node2"},
    #          {"label": "node3"}]
    # list_of_edges = [{"source": "node1", "target": "node2"},
    #                  {"source": "node1", "target": "node3"}]
    list_of_nodes = []
    list_of_edges = []

    qres = g.query(
        """
        SELECT DISTINCT ?c2 ?f2_label ?c1 ?f1_label WHERE {
            ?c2 p-plan:isPreceededBy ?c1 .

            ?c2 biii:hasImplementation ?s2 .
            ?c2 biii:hasFunction ?f2 .
            ?f2 rdfs:label ?f2_label .

            ?c1 biii:hasImplementation ?s1 .    
            ?c1 biii:hasFunction ?f1 .  
            ?f1 rdfs:label ?f1_label .
        }
        """, initNs=ns)

    with open('static/data/wf.csv', 'w', newline='') as csvfile:
        fieldnames = ['source', 'source_label', 'target', 'target_label', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in qres:
            list_of_nodes.append({"id": row['c1']})
            list_of_nodes.append({"id": row['c2']})
            list_of_edges.append({"source": row['c1'], "target": row['c2'],
                                  "source_label": row['f1_label'], "target_label": row['f2_label']})
            # writer.writerow({'source': row['c1'],
            #                  'source_label': row['f1_label'],
            #                  'target': row['c2'],
            #                  'target_label': row['f2_label'],
            #                  'value': '2'})

    return render_template('test.html', nodes=list_of_nodes, edges=list_of_edges)

@app.route('/')
def welcome():
    qres = g.query(
        """
        SELECT DISTINCT ?c2 ?f2_label ?c1 ?f1_label WHERE {
            ?c2 p-plan:isPreceededBy ?c1 .

            ?c2 biii:hasImplementation ?s2 .
            ?c2 biii:hasFunction ?f2 .
            ?f2 rdfs:label ?f2_label .

            ?c1 biii:hasImplementation ?s1 .    
            ?c1 biii:hasFunction ?f1 .  
            ?f1 rdfs:label ?f1_label .
        }
        """, initNs=ns)

    with open('static/data/wf.csv', 'w', newline='') as csvfile:
        fieldnames = ['source', 'source_label', 'target', 'target_label', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in qres:
            # writer.writerow({'source': row['f1_label'], 'target': row['f2_label'], 'value': '2'})
            # writer.writerow({'source': str(row['f1_label']+"\n"+row['c1']),
            #                  'source_label': row['f1_label'],
            #                  'target': str(row['f1_label']+"\n"+row['c1']),
            #                  'target_label': row['f2_label'],
            #                  'value': '3'})

            writer.writerow({'source': row['c1'],
                             'source_label': row['f1_label'],
                             'target': row['c2'],
                             'target_label': row['f2_label'],
                             'value': '2'})

            # print(row['c2'])
            # print(row['c1'])
            # print("%s %s %s %s" % row)

    return render_template('wf.html')


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
