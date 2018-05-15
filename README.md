# Bise Core Ontology

This repository hosts the core ontology of the BISE BioImaging Search Engine. 

## Ontology development process 
1. Web protégé (online web editor) : https://webprotege.stanford.edu/#projects/38b3da5d-b5ce-4d59-972c-23fcb700256a 
2. Export to an OWL file
3. Documentation generation (LODE) : 
  - http://visualdataweb.de/webvowl/#iri=https://raw.githubusercontent.com/NeuBIAS/bise-core-ontology/master/owl-ontology/bise-core-ontology-v1.1.owl
  - http://www.essepuntato.it/lode/owlapi/https://raw.githubusercontent.com/NeuBIAS/neubias-data-model/master/owl-ontology/bise-core-ontology-v1.1.owl

# Demo queries
[demo-queries.md](demo-queries.md)
 
# Demo web app
### Virtual environment setup to get python dependencies
```
conda create --name bise-ld-webapp
source activate bise-ld-webapp
conda install flask rdflib rdflib-jsonld pymongo -c conda-forge
```
### Launch the web app
```
cd bise-linked-data-webapp
python app.py
```
