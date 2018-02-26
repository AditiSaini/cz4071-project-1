# Generating Graph

1. Make sure to have Postgres Setup and check credentials in `generate_graph.py`
2. Run `pip3 install -r requirements.txt`
3. Run `python3 generate_graph.py <nodes for lineitem: optional> <plot with matplotlib:optional>`
4. Two files will be generated `graph.gml` for graphing tools and `graph.txt` in the format we discussed 

# Results
1. Use `wc -l graph.txt` to count the number of nodes
2. `python3 generate_graph.py 80000` generates 273,687 nodes

# TODO
- Currently, LineItem and PartSupp are set as nodes. They shouldn't be. 