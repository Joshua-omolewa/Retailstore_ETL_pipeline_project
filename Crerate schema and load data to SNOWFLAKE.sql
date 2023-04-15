
USE DATABASE PROJECT_DB;
USE SCHEMA RAW;

---STORE
CREATE OR REPLACE TABLE PROJECT_DB.RAW.store
(
	store_key	INTEGER,
	store_num	varchar(30),
	store_desc	varchar(150),
	addr	varchar(500),
	city	varchar(50),
	region varchar(100),
	cntry_cd	varchar(30),
	cntry_nm	varchar(150),
	postal_zip_cd	varchar(10),
	prov_state_desc	varchar(30),
	prov_state_cd	varchar(30),
    store_type_cd varchar(30),
    store_type_desc varchar(150),
	frnchs_flg	boolean,
	store_size numeric(19,3),
	market_key	integer,
	market_name	varchar(150),
    submarket_key	integer,
	submarket_name	varchar(150),
	latitude	NUMERIC(19, 6),
	longitude	NUMERIC(19, 6)
);


COPY INTO PROJECT_DB.RAW.store FROM @raw_data_stage/store_mid.csv;



-----SALES
CREATE OR REPLACE TABLE sales(
trans_id int,
prod_key int,
store_key int,
trans_dt date,
trans_time int,
sales_qty numeric(38,2),
sales_price numeric(38,2),
sales_amt NUMERIC(38,2),
discount numeric(38,2),
sales_cost numeric(38,2),
sales_mgrn numeric(38,2),
ship_cost numeric(38,2)
);


COPY INTO PROJECT_DB.RAW.sales FROM @raw_data_stage/sales_mid.csv;


---CALENDAR
CREATE OR REPLACE TABLE PROJECT_DB.RAW.calendar
(	
	cal_dt	date NOT NULL,
	cal_type_desc	varchar(20),
	day_of_wk_num	 varchar(30),
	day_of_wk_desc varchar,
	yr_num	integer,
	wk_num	integer,
	yr_wk_num	integer,
	mnth_num	integer,
	yr_mnth_num	integer,
	qtr_num	integer,
	yr_qtr_num	integer
);

COPY INTO PROJECT_DB.RAW.calendar FROM @raw_data_stage/calendar_mid.csv;

----PRODUCT
CREATE OR REPLACE TABLE product 
(
	prod_key int ,
	prod_name varchar,
	vol NUMERIC (38,2),
	wgt NUMERIC (38,2),
	brand_name varchar, 
	status_code int,
	status_code_name varchar,
	category_key int,
	category_name varchar,
	subcategory_key int,
	subcategory_name varchar
);

COPY INTO PROJECT_DB.RAW.product FROM @raw_data_stage/product_mid.csv;


------- INVENTORY
CREATE OR REPLACE TABLE RAW.inventory (
cal_dt date,
store_key int,
prod_key int,
inventory_on_hand_qty NUMERIC(38,2),
inventory_on_order_qty NUMERIC(38,2),
out_of_stock_flg int,
waste_qty number(38,2),
promotion_flg boolean,
next_delivery_dt date
);

COPY INTO PROJECT_DB.RAW.inventory FROM @raw_data_stage/inventory_mid.csv;


