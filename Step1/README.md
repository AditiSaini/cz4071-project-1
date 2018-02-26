# Step 1 - Injecting the data into Postgres
http://myfpgablog.blogspot.sg/2016/08/tpc-h-queries-on-postgresql.html

Conversion for *.tbl to *.csv
```
for i in `ls *.tbl`; do sed 's/.\{2\}$//' $i > ${i/tbl/csv}; echo $i; done;
```

Download [tpch.sql](https://drive.google.com/file/d/0Bx98V884cOiAMVlwb29qalRvYjA/view)
Change `/opt/db/ws/tpch/sql/` to the directory of all data files

In Postgres Terminal
```
create database tpch;
\c tpch;
\i <dir>/tpch.sql
```

How data is processed
```
lineitem 
  -> orders
    -> customer
      -> nation
        -> region
        -> supplier
  -> partsupp
    -> part
```

```
-- This values fetch around ~335,000 records
\set item_offset 0
\set items 100000

-- Destroy the previous tables
DROP TABLE data_lineitem;
DROP TABLE data_orders;
DROP TABLE data_customer;
DROP TABLE data_nations;
DROP TABLE data_region;
DROP TABLE data_supplier;
DROP TABLE data_partsupp;
DROP TABLE data_part;

-- Dump data into the tables
select * into data_lineitem from lineitem limit :items offset :item_offset;
select * into data_orders from orders where o_orderkey in (select distinct l_orderkey from data_lineitem);
select * into data_customer from customer where c_custkey in (select distinct o_custkey from data_orders);
select partsupp.* into data_partsupp from partsupp join data_lineitem on l_partkey = ps_partkey and l_suppkey = ps_suppkey WHERE l_orderkey in (select distinct l_orderkey from data_lineitem);
select * into data_part from part where p_partkey in (select distinct ps_partkey from data_partsupp);
select * into data_supplier from supplier where s_suppkey in (select distinct ps_suppkey from data_partsupp);
select * into data_nations from nation where n_nationkey in (select distinct c_nationkey from data_customer union all select distinct s_nationkey from data_supplier);
select * into data_region from region where r_regionkey in (select distinct n_regionkey from data_nations);

-- Counts total number of vertices
select sum(count) from (select count(*) from data_lineitem UNION ALL
select count(*) from data_orders UNION ALL
select count(*) from data_customer UNION ALL
select count(*) from data_nations UNION ALL
select count(*) from data_region UNION ALL
select count(*) from data_supplier UNION ALL
select count(*) from data_partsupp UNION ALL
select count(*) from data_part) as foo;
```
