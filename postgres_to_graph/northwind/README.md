Guide used https://neo4j.com/developer/guide-importing-data-and-etl/#_developing_a_graph_model
Download from for the dataset used https://code.google.com/archive/p/northwindextended/downloads

## Note: if psql not found
```
export PATH=/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH
```

# Postgres Interactive
```
create database northwind
\c northwind
\i /Users/junxiang/Downloads/northwind.postgre.sql

cp *.csv ~/Library/Application\ Support/Neo4j\ Desktop/Application/neo4jDatabases/database-dc2ffeb4-8a7d-40b4-93d0-42af24b61b40/installation-3.3.3/import/
```

# Neo4J
- Install the client `brew install cleishm/neo4j/neo4j-client`
- Connect and run the following three files`neo4j-client -u neo4j -p root -o result.out -i 3.relationships.cypher localhost 7687`
  - 1.import_csv.cypher (Needs to run the commands each in Neo4J Browser. Issue of it throwing segfault)
  - 2.constraints.cypher
  - 3.relationships.cypher

neo4j-client -u neo4j -p root -o result.out -i 1.import_csv.cypher localhost 7687
