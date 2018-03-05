# CZ4071-Assignment

## Deadline
March 13, 2018; 5 PM

# TODO List
1) From TPC -> Write import statement into Postgres
2) Using Postgres data, generate Nodes and Edges
  - Using Python to convert
3) Analyze graph properties
  - [x] Average path length
  - [x] Betweenness centrality
  - [x] Closeness centrality
  - [ ] Degree distribution
  - [ ] Maximum degree
  - [ ] Degree correlation
  - [ ] Degree centrality
  - [ ] Clustering coefficient
  - [ ] N-th moment
4) Compare with random network and scale free networks
  - Random Network [Jia Jun] 
  - Scale Free Networks 
4) Generate UI (Python Tkinter)
5) (Optional) Consider networks from http://snap.stanford.edu/data/index.html

## TPC-H Steps
- Program uploaded as tpc-h-tool.zip
- Unzip the package. You will find a folder “dbgen” in it.
- Open up tpch.vcproj using visual studio software.
- Build the tpch project. When the build is successful, a command prompt will appear with “TPC-H Population Generator <Version 2.17.3>” and several *.tbl files will be generated. You should expect the following .tbl files: customer.tbl, lineitem.tbl, nation.tbl, orders.tbl, part.tbl, partsupp.tbl, region.tbl, supplier.tbl
- Save these .tbl files as .csv files
- These .csv files contain an extra “|” character at the end of each line. These “|” characters are incompatible with the format that PostgreSQL is expecting. Write a small piece of code to remove the last “|” character in each line. Now you are ready to load the .csv files into PostgreSQL
- Open up PostgreSQL. Add a new database “TPC-H”.
- Create new tables for “customer”, “lineitem”, “nation”, “orders”, “part”, “partsupp”, “region” and “supplier”
- Import the relevant .csv into each table. Note that pgAdmin4 for PostgreSQL (windows version) allows you to perform import easily. You can select to view the first 100 rows to check if the import has been done correctly.

## Deliverables
- Hard copy of the program.
- Hardcopy of analysis and insights that characterize the various properties of the generated network w.r.t random and scale-free networks you have studied in the course.
- Hard copy of screenshots of the GUI and its various features. Discussion on challenges you have faced in visualizing the chosen network and how you have addressed them.
- Softcopy of the program.
- More details related to softcopy submission will be provided closer to the date.

## Reference
- https://github.com/edwin-candinegara/CZ4071-network-science
