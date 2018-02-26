# TODO: Converting to Nodes & Edges

```
-- Drop any existing database
DROP TABLE data_nodes;
DROP TABLE data_edges;

-- Tables to store the nodes and edegs
CREATE TABLE data_nodes (
  id SERIAL primary key,
  table_id INT NOT NULL,
  table_name CHAR(50)
);

CREATE TABLE data_edges (
  id SERIAL primary key,
  from_node INT NOT NULL,
  to_node INT NOT NULL,
  relationship CHAR(50)
);

-- Insert the data from the dumped database
insert into data_nodes (table_id, table_name) select l_orderkey, 'data_lineitem' as table_name from data_lineitem;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_orders' as table_name from data_orders;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_customer' as table_name from data_customer;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_nations' as table_name from data_nations;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_region' as table_name from data_region;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_supplier' as table_name from data_supplier;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_partsupp' as table_name from data_partsupp;
insert into data_nodes (table_id, table_name) select c_custkey, 'data_part' as table_name from data_part;
```

Nodes
- Order
- Part
- Supplier
- Customer
- Nation
- Region

Edges
- Part_Supplier
- Line_Item







edges table
from_node   to_node   relationship
