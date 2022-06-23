
-- create table based on example schema
CREATE TABLE IF NOT EXISTS public.sales_target
(
    id     INTEGER PRIMARY KEY,
    sale_value INTEGER,
	created_at TIMESTAMP DEFAULT NOW()
);


-- insert dummy data
INSERT INTO public.sales_target (id, sale_value)
VALUES 
(1, 1000),
(2, 1500),
(3, 2000);
