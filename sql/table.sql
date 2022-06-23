-- create table based on example schema
CREATE TABLE IF NOT EXISTS public.sales_target
(
    id     INTEGER PRIMARY KEY,
    sale_value INTEGER,
	created_at TIMESTAMP DEFAULT NOW()
);

