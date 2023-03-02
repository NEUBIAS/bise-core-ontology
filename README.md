# Bise Core Ontology

This repository hosts the core ontology of the BISE BioImaging Search Engine. 
Latest data dump is available from the bio.tools git hub:  https://raw.githubusercontent.com/bio-tools/content/master/datasets/bise-ontology-biii-dump.ttl

## Ontology development process 
1. Web protégé (online web editor) : https://webprotege.stanford.edu/#projects/38b3da5d-b5ce-4d59-972c-23fcb700256a 
2. Export to an OWL file
3. Documentation generation (LODE) : 
  - http://vowl.visualdataweb.org/webvowl-old/webvowl-old.html#iri=https://raw.githubusercontent.com/NeuBIAS/bise-core-ontology/master/owl-ontology/bise-core-ontology-v1.1.owl
  - (broken link) http://www.essepuntato.it/lode/owlapi/https://raw.githubusercontent.com/NeuBIAS/neubias-data-model/master/owl-ontology/bise-core-ontology-v1.1.owl

# Demo queries
[demo-queries.md](demo-queries.md)

# Demo notebooks 
 - Example of advanced ontology-based queries : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NeuBIAS/bise-core-ontology/master?filepath=advanced-queries-demo.ipynb)
 - Quality-oriented queries : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NeuBIAS/bise-core-ontology/master?filepath=quality-curation-queries.ipynb)
 - Authors network visualisation query:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NeuBIAS/bise-core-ontology/master?filepath=network-visualization-queries.ipynb)

### Getting python dependencies
With Conda :
```
conda create --name bise-ld-webapp
source activate bise-ld-webapp
conda install rdflib jupyter -c conda-forge
```
Or with pip :
```
pip install rdflib
pip install jupyter
```
### Launching the notebook
```
jupyter-notebook
```

 
# Demo web app
### Virtual environment setup to get python dependencies
```
conda create --name bise-ld-webapp
source activate bise-ld-webapp
conda install flask rdflib pymongo -c conda-forge
conda install rdflib-jsonld -c bioconda
```
### Launch the web app
```
cd bise-linked-data-webapp
python app.py
```
