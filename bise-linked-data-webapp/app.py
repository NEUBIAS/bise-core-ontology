import csv
from flask import Flask, redirect, url_for, request, render_template
import random

from rdflib import ConjunctiveGraph

app = Flask(__name__)

ns = {"nb": "http://bise-eu.info/core-ontology#",
      "dc": "http://dcterms/",
      "p-plan": "http://purl.org/net/p-plan#",
      "edam": "http://purl.obolibrary.org/obo/edam#"}

g = ConjunctiveGraph()
#g.parse("bise-linked-data-webapp/static/data/neubias-dump-20180129.ttl", format="turtle")
g.parse("static/data/neubias-latest.ttl", format="turtle")
g.parse("static/data/EDAM-bioimaging_alpha03.owl")
print(str(len(g)) + ' triples in Biii data graph')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curation_needs_demo')
def curation_needs_demo():

    # NO PUBLICATION
    q_no_publication = """
    SELECT (count(?title) as ?nb_soft) WHERE {
        ?s rdf:type <http://biii.eu/node/software> .
        ?s dc:title ?title .
        FILTER NOT EXISTS {?s nb:hasReferencePublication ?publication} .
    }
    """
    q_no_publication_entries = """
    SELECT ?s ?title WHERE {
        ?s rdf:type <http://biii.eu/node/software> .
        ?s dc:title ?title .
        FILTER NOT EXISTS {?s nb:hasReferencePublication ?publication} .
    }
    """
    results = g.query(q_no_publication, initNs=ns)
    count_no_pub = 0
    for r in results:
        print(r)
        count_no_pub = str(r["nb_soft"])

    results = g.query(q_no_publication_entries, initNs=ns)
    no_pub = []
    for r in results:
        no_pub.append({"title": r["title"], "url": r["s"]})
    if len(no_pub) > 5:
        no_pub = random.sample(no_pub, 10)

    # NO EDAM TOPIC OR FUNCTION
    q_no_edam = """
        SELECT (count(?title) as ?nb_soft) WHERE {
            ?s rdf:type <http://biii.eu/node/software> .
            ?s dc:title ?title .
            FILTER NOT EXISTS {?s nb:hasTopic ?topic} .
            FILTER NOT EXISTS {?s nb:hasFunction ?operation} .
        }
        """
    results = g.query(q_no_edam, initNs=ns)
    count_no_edam = 0
    for r in results:
        count_no_edam = str(r["nb_soft"])

    q_no_edam_entries = """
        SELECT ?s ?title WHERE {
            ?s rdf:type <http://biii.eu/node/software> .
            ?s dc:title ?title .
            FILTER NOT EXISTS {?s nb:hasTopic ?topic} .
            FILTER NOT EXISTS {?s nb:hasFunction ?operation} .
        }
        """
    results = g.query(q_no_edam_entries, initNs=ns)
    no_edam = []
    for r in results:
        no_edam.append({"title": r["title"], "url": r["s"]})
    if len(no_edam) > 5:
        no_edam = random.sample(no_edam, 10)

    return render_template('demo_curation_needs.html',
                           count_no_pub=count_no_pub,
                           count_no_edam=count_no_edam,
                           missing_publication = no_pub,
                           missing_edam=no_edam)


@app.route('/comulis_demo')
def comulis_demo():
    q_segmentation = """
    SELECT DISTINCT ?soft ?title 
        (group_concat(?function_label;separator="|") as ?operations)
        (group_concat(?topic_label;separator="|") as ?topics) 
        WHERE { 
        ?soft a <http://biii.eu/node/software> .
        ?soft <http://bise-eu.info/core-ontology#hasFunction> ?edam_function .
        ?edam_function rdfs:subClassOf* <http://edamontology.org/operation_Image_segmentation> . 
        ?edam_function rdfs:label ?function_label .
        ?soft dc:title ?title .
        
        OPTIONAL {
            ?soft <http://bise-eu.info/core-ontology#hasTopic> ?edam_topic .
            ?edam_topic rdfs:label ?topic_label .
        }
    }
    GROUP BY ?soft
    ORDER BY ?title
    """

    q_registration = """
    SELECT DISTINCT ?soft ?title 
        (group_concat(?function_label;separator="|") as ?operations)
        (group_concat(?topic_label;separator="|") as ?topics) 
    WHERE { 
        ?soft a <http://biii.eu/node/software> .
        ?soft <http://bise-eu.info/core-ontology#hasFunction> ?edam_function . 
        ?edam_function rdfs:subClassOf* <http://edamontology.org/operation_Image_registration> . 
        ?edam_function rdfs:label ?function_label . 
        ?soft dc:title ?title .
        
        OPTIONAL {
            ?soft <http://bise-eu.info/core-ontology#hasTopic> ?edam_topic .
            ?edam_topic rdfs:label ?topic_label .
        }
    }
    GROUP BY ?soft
    ORDER BY ?title
    """

    q_visualisation = """
    SELECT DISTINCT ?soft ?title 
        (group_concat(?function_label;separator="|") as ?operations)
        (group_concat(?topic_label;separator="|") as ?topics)
    WHERE { 
        ?soft a <http://biii.eu/node/software> .
        ?soft <http://bise-eu.info/core-ontology#hasFunction> ?edam_function .
        ?edam_function rdfs:subClassOf* <http://edamontology.org/operation_Image_visualisation> . 
        ?edam_function rdfs:label ?function_label .

        ?soft dc:title ?title .
        
        OPTIONAL {
            ?soft <http://bise-eu.info/core-ontology#hasTopic> ?edam_topic .
            ?edam_topic rdfs:label ?topic_label .
        }
    }
    GROUP BY ?soft
    ORDER BY ?title
    """

    seg_entries = []
    results = g.query(q_segmentation, initNs=ns)
    for r in results:
        title = str(r["title"])
        url = str(r["soft"])
        operations = list(set(str(r["operations"]).split("|")))
        operations = filter(None, operations)
        topics = list(set(str(r["topics"]).split("|")))
        topics = filter(None, topics)
        seg_entries.append({"title":title, "url":url, "operations":operations, "topics":topics})

    reg_entries = []
    results = g.query(q_registration, initNs=ns)
    for r in results:
        title = str(r["title"])
        url = str(r["soft"])
        operations = list(set(str(r["operations"]).split("|")))
        operations = filter(None, operations)
        topics = list(set(str(r["topics"]).split("|")))
        topics = filter(None, topics)
        reg_entries.append({"title": title, "url": url, "operations": operations, "topics": topics})

    vis_entries = []
    results = g.query(q_visualisation, initNs=ns)
    for r in results:
        title = str(r["title"])
        url = str(r["soft"])
        operations = list(set(str(r["operations"]).split("|")))
        operations = filter(None, operations)
        topics = list(set(str(r["topics"]).split("|")))
        topics = filter(None, topics)
        vis_entries.append({"title": title, "url": url, "operations": operations, "topics": topics})

    return render_template('demo_comulis.html', seg_entries=seg_entries, reg_entries=reg_entries, vis_entries=vis_entries)

@app.route('/cy')
def cy():
    return render_template('test_cy.html')

@app.route('/topic_map_demo')
def topic_map_demo():
    query = """
        SELECT ?topic_label ?operation_label WHERE {
             ?x a <http://biii.eu/node/software> .
             ?x <http://bise-eu.info/core-ontology#hasTopic> ?edam_topic .
             ?x <http://bise-eu.info/core-ontology#hasFunction> ?edam_operation .
             ?x <http://dcterms/title> ?title .
             
             ?edam_topic rdfs:label ?topic_label .
             ?edam_operation rdfs:label ?operation_label .
        } 
        """

    list_of_nodes = []
    list_of_edges = []
    qres = g.query(query)
    for row in qres:
        #print(row["topic_label"] + " <-> "  + row["operation_label"])
        list_of_nodes.append({"id": row["topic_label"], "type": "topic"})
        list_of_nodes.append({"id": row["operation_label"], "type": "operation"})
        list_of_edges.append({"source": row["topic_label"], "target": row["operation_label"]})

    return render_template('demo_topic_map.html', nodes=list_of_nodes, edges=list_of_edges)

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

@app.route('/demo_query_3')
def demoQ3():
    query = """
    CONSTRUCT {
       ?ti <http://bise-eu.info/core-ontology#hasTopic> ?label 
    } WHERE {
         ?x a <http://biii.eu/node/software> .
         ?x <http://bise-eu.info/core-ontology#hasAuthor> ?a .
         ?x <http://dcterms/title> ?ti .
         ?x <http://bise-eu.info/core-ontology#hasTopic> ?c .
 
         ?c rdfs:subClassOf* ?superClass .
         ?superClass rdfs:label ?label .
 
         FILTER (regex(?label, "microscopy"))
    } 
    """

    qres = g.query(query)

    list_of_nodes = []
    list_of_edges = []
    for row in qres:
        list_of_nodes.append({"id": row[0], "type" :"software"})
        list_of_nodes.append({"id": row[2], "type" : "topic"})
        list_of_edges.append({"source": row[0], "target": row[2], "edge_label": row[1]})

    # print(list_of_nodes)
    # print(list_of_edges)
    return render_template('demo_d3.html', nodes=list_of_nodes, edges=list_of_edges)

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

@app.route('/welcome')
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
