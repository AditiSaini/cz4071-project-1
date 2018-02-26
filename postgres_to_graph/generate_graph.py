# Run: python3 generate_graph <limit: optional>
# Example: python3 generate_graph 5
import psycopg2
import json
import sys

CREDS = "dbname='tpch' user='junxiang' host='localhost'"

# Example Format
# nodes = {
#     region: {
#         1: {node_id: 0, data: { name: 'AFRICA' } }
#     },
#     nation: {
#         1: {node_id: 1, data: { name: 'SINGAPORE' } }
#     }
# }

# edges = [(0, 1), (2, 3)]

## Regenerates the data from the whole dataset
gen_data = """
DROP TABLE data_lineitem;
DROP TABLE data_orders;
DROP TABLE data_customer;
DROP TABLE data_nations;
DROP TABLE data_region;
DROP TABLE data_supplier;
DROP TABLE data_partsupp;
DROP TABLE data_part;

select * into data_lineitem from lineitem limit {} offset {};
select * into data_orders from orders where o_orderkey in (select distinct l_orderkey from data_lineitem);
select * into data_customer from customer where c_custkey in (select distinct o_custkey from data_orders);
select partsupp.* into data_partsupp from partsupp join data_lineitem on l_partkey = ps_partkey and l_suppkey = ps_suppkey WHERE l_orderkey in (select distinct l_orderkey from data_lineitem);
select * into data_part from part where p_partkey in (select distinct ps_partkey from data_partsupp);
select * into data_supplier from supplier where s_suppkey in (select distinct ps_suppkey from data_partsupp);
select * into data_nations from nation where n_nationkey in (select distinct c_nationkey from data_customer union all select distinct s_nationkey from data_supplier);
select * into data_region from region where r_regionkey in (select distinct n_regionkey from data_nations);
"""

nodes = {}
edges = []
node_id = 0


conn = psycopg2.connect(CREDS)
cur = conn.cursor()

if len(sys.argv) == 2:
    cur.execute(gen_data.format(sys.argv[1], 0))

## Dump Region Rows
nodes['region'] = {}
cur.execute("""SELECT * from data_region""")
rows = cur.fetchall()
for row in rows:
    nodes['region'][row[0]] = {'node_id': node_id, 'data': {'name': row[1].strip(), 'table': 'region'}}
    node_id += 1

## Dump Nation Rows
nodes['nation'] = {}
cur.execute("""SELECT * from data_nations""")
rows = cur.fetchall()
for row in rows:
    nodes['nation'][row[0]] = {'node_id': node_id, 'data': { 'name': row[1].strip(), 'table': 'nation' } }
    edges.append((node_id, nodes['region'][row[2]]['node_id']))
    node_id += 1

## Dump Supplier Rows
nodes['supplier'] = {}
cur.execute("""SELECT * from data_supplier""")
rows = cur.fetchall()
for row in rows:
    nodes['supplier'][row[0]] = {'node_id': node_id, 'data': {
        'name': row[1].strip(), 'table': 'supplier'}}
    edges.append((node_id, nodes['nation'][row[3]]['node_id']))
    node_id += 1

## Dump Customer Rows
nodes['customer'] = {}
cur.execute("""SELECT * from data_customer""")
rows = cur.fetchall()
for row in rows:
    nodes['customer'][row[0]] = {'node_id': node_id, 'data': {
        'name': row[1].strip(), 'table': 'customer'}}
    edges.append((node_id, nodes['nation'][row[3]]['node_id']))
    node_id += 1

## Dump Order Rows
nodes['order'] = {}
cur.execute("""SELECT * from data_orders""")
rows = cur.fetchall()
for row in rows:
    nodes['order'][row[0]] = {'node_id': node_id, 'data': {'name': 'O:' + str(row[0]), 'table': 'order'}}
    edges.append((node_id, nodes['customer'][row[1]]['node_id']))
    node_id += 1

## Dump part Rows
nodes['part'] = {}
cur.execute("""SELECT * from data_part""")
rows = cur.fetchall()
for row in rows:
    nodes['part'][row[0]] = {'node_id': node_id, 'data': {'name': 'P:' + str(row[0]), 'table': 'part'}}
    node_id += 1

## Dump partsupp Rows
# Do note that this is just for test. Partsupp should not end up to be a node
nodes['partsupp'] = {}
cur.execute("""SELECT * from data_partsupp""")
rows = cur.fetchall()
for row in rows:
    nodes['partsupp'][(row[0], row[1])] = {'node_id': node_id, 'data': {'name': 'PS:' + str((row[0], row[1])), 'table': 'partsupp'}}
    edges.append((node_id, nodes['part'][row[0]]['node_id']))
    edges.append((node_id, nodes['supplier'][row[1]]['node_id']))
    node_id += 1

## Dump lineitem Rows
lineitemID = 0
nodes['lineitem'] = {}
cur.execute("""SELECT * from data_lineitem""")
rows = cur.fetchall()
for row in rows:
    nodes['lineitem'][lineitemID] = {
        'node_id': node_id, 'data': {'name': 'LI:' + str(lineitemID), 'table': 'lineitem'}}
    edges.append((node_id, nodes['order'][row[0]]['node_id']))
    edges.append((node_id, nodes['partsupp'][(row[1], row[2])]['node_id']))
    node_id += 1
    lineitemID += 1


# print(json.dumps(nodes, indent=2, sort_keys=True))
# print(edges)

import networkx as nx

## Create graph
G = nx.Graph()

## Adding of nodes
for table_key in nodes:
    for prim_key in nodes[table_key]:
        G.add_node(nodes[table_key][prim_key]['node_id'], color='blue', **nodes[table_key][prim_key]['data'])

## Adding of edges
G.add_edges_from(edges)
nx.write_gml(G, 'graph.gml')

raw_file = open('graph.txt', 'w')
for i in G.nodes:
    raw_file.write(' '.join([str(q[1]) for q in G.edges(i)]) + '\n')
raw_file.close()

# # Graph plotting
# import matplotlib.pyplot as plt

# Create color map
color_map = {
    'region': '#e6194b', # red
    'nation': '#3cb44b', # green
    'supplier': '#ffe119', # yellow
    'customer': '#0082c8', # blue
    'order': '#f58231', # orange
    'lineitem': '#911eb4', # purple
    'part': '#46f0f0', # cyan
    'partsupp': '#f032e6', # magenta
    'lineitem': '#fabebe'  # pink
}

# Create labels
labels = {}
for table_key in nodes:
    for prim_key in nodes[table_key]:
        labels[nodes[table_key][prim_key]['node_id']] = nodes[table_key][prim_key]['data']['name']

pos = nx.spring_layout(G, scale=2)
## construct a list of colors then pass to node_color
nx.draw(G, labels=labels, node_color=[color_map[G.node[node]['table']] for node in G])
# nx.draw(G, node_color=[color_map[G.node[node]['table']] for node in G])
plt.show()
