# CZ4071-Assignment

## Deadline

March 13, 2018; 5 PM

# TODO List

1. [x] Import the TPC-H benchmark data into Postgres
2. [x] Convert the tables into a graph
3. Analyze various graph properties
  - [x] Average path length
  - [x] Betweenness centrality
  - [x] Closeness centrality
  - [x] Degree distribution
  - [x] Maximum degree
  - [x] Degree correlation
  - [x] Degree centrality
  - [x] Clustering coefficient - local & average
  - [x] N-th moment
4. [ ] Compare with random network and scale-free networks
5. [ ] Generate UI (Python Tkinter)
  - [x] Betweenness heatmap
  - [x] Closeness heatmap
  - [x] Degree distribution (tgt. w/ N-th moment)
  - [x] Degree correlation
  - [ ] BC v.s. closeness plot
  - [ ] Closeness v.s. degree plot
  - [ ] BC v.s. degree plot
6. [ ] Consider networks from http://snap.stanford.edu/data/index.html (optional)

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
