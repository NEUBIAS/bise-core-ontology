# RDF data dumps generation

## Data transformation process

  1. For each CSV table, write a SPARQL CONSTRUCT query to align column names to RDF predicates.  
  2. Run TARQL to produce one RDF for each CSV table. 
  3. The resulting RDF files can later be deployed onto a SPARQL endpoint. A sample SPARQL endpoint is available here : http://192.54.201.50/sparql
