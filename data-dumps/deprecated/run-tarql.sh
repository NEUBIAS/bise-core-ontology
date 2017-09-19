tarql -v -d ";" biii-csv2rdf-entity.sparql entity.csv > rdf/entries.ttl
tarql -v -d ";" biii-csv2rdf-software.sparql softwareartifact.csv > rdf/softwares.ttl
tarql -v -d ";" biii-csv2rdf-paper.sparql academicpaper.csv > rdf/papers.ttl
