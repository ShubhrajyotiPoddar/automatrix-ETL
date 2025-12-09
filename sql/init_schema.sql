--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: grn_daily_main; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grn_daily_main (
    id bigint NOT NULL,
    grn_date timestamp without time zone,
    supplier_code character varying(255),
    supplier_name character varying(255),
    item_ctag_code character varying(255),
    item_ctag_name character varying(255),
    item_code character varying(255),
    item_name character varying(255),
    um character varying(255),
    stock_type_name character varying(255),
    grn_number character varying(255),
    purchase_order_number character varying(255),
    department character varying(255),
    department_name character varying(255),
    indent_number character varying(255),
    currency_code character varying(255),
    exchange_rate character varying(255),
    cost_project character varying(255),
    cost_project_name character varying(255),
    currency_name character varying(255),
    challan_qty character varying(255),
    rate character varying(255),
    net_amount character varying(255)
);


ALTER TABLE public.grn_daily_main OWNER TO postgres;

--
-- Name: pur_order_daily_main; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pur_order_daily_main (
    id bigint NOT NULL,
    order_date timestamp without time zone,
    supplier_code character varying(255),
    supplier_name character varying(255),
    item_category_code character varying(255),
    item_category_name character varying(255),
    item_code character varying(255),
    item_name character varying(255),
    um character varying(255),
    order_number character varying(255),
    entered_by_name character varying(255),
    indent_number character varying(255),
    department character varying(255),
    department_name character varying(255),
    cost_project character varying(255),
    cost_project_name character varying(255),
    currency_code character varying(255),
    currency_name character varying(255),
    exchange_rate character varying(255),
    stock_type_name character varying(255),
    order_value character varying(255),
    order_quantity character varying(255),
    bal_qty character varying(255),
    rate character varying(255)
);


ALTER TABLE public.pur_order_daily_main OWNER TO postgres;

--
-- Name: issue_daily_main; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issue_daily_main (
    id bigint NOT NULL,
    issue_date timestamp without time zone,
    item_category_code character varying(255),
    item_category_name character varying(255),
    department_code character varying(255),
    department_name character varying(255),
    item_code character varying(255),
    cost_centre_code character varying(255),
    cost_name character varying(255),
    item_name character varying(255),
    um character varying(255),
    quantity character varying(255),
    rate character varying(255),
    value character varying(255),
    stock_type_name character varying(255)
);


ALTER TABLE public.issue_daily_main OWNER TO postgres;

--
-- Name: cost_master_main; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.cost_master_main AS
 WITH combined_cost_projects AS (
         SELECT pur_order_daily_main.cost_project,
            pur_order_daily_main.cost_project_name
           FROM public.pur_order_daily_main
          WHERE (pur_order_daily_main.cost_project IS NOT NULL)
        UNION
         SELECT grn_daily_main.cost_project,
            grn_daily_main.cost_project_name
           FROM public.grn_daily_main
          WHERE (grn_daily_main.cost_project IS NOT NULL)
        UNION
         SELECT issue_daily_main.cost_centre_code AS cost_project,
            issue_daily_main.cost_name AS cost_project_name
           FROM public.issue_daily_main
          WHERE (issue_daily_main.cost_centre_code IS NOT NULL)
        ), ranked_cost_projects AS (
         SELECT combined_cost_projects.cost_project,
            combined_cost_projects.cost_project_name,
            row_number() OVER (PARTITION BY combined_cost_projects.cost_project ORDER BY (length((combined_cost_projects.cost_project_name)::text)) DESC) AS rn
           FROM combined_cost_projects
        )
 SELECT cost_project AS cost_code,
    cost_project_name
   FROM ranked_cost_projects
  WHERE (rn = 1)
  ORDER BY cost_project;


ALTER VIEW public.cost_master_main OWNER TO postgres;

--
-- Name: department_master_main; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.department_master_main AS
 WITH combined_departments AS (
         SELECT pur_order_daily_main.department,
            pur_order_daily_main.department_name
           FROM public.pur_order_daily_main
          WHERE (pur_order_daily_main.department IS NOT NULL)
        UNION
         SELECT grn_daily_main.department,
            grn_daily_main.department_name
           FROM public.grn_daily_main
          WHERE (grn_daily_main.department IS NOT NULL)
        UNION
         SELECT issue_daily_main.department_code AS department,
            issue_daily_main.department_name
           FROM public.issue_daily_main
          WHERE (issue_daily_main.department_code IS NOT NULL)
        ), ranked_departments AS (
         SELECT combined_departments.department,
            combined_departments.department_name,
            row_number() OVER (PARTITION BY combined_departments.department ORDER BY (length((combined_departments.department_name)::text)) DESC) AS rn
           FROM combined_departments
        )
 SELECT department AS department_code,
    department_name
   FROM ranked_departments
  WHERE (rn = 1)
  ORDER BY department;


ALTER VIEW public.department_master_main OWNER TO postgres;

--
-- Name: grn_daily_main_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grn_daily_main_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grn_daily_main_id_seq OWNER TO postgres;

--
-- Name: grn_daily_main_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grn_daily_main_id_seq OWNED BY public.grn_daily_main.id;


--
-- Name: issue_daily_main_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issue_daily_main_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.issue_daily_main_id_seq OWNER TO postgres;

--
-- Name: issue_daily_main_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issue_daily_main_id_seq OWNED BY public.issue_daily_main.id;


--
-- Name: item_master_main; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.item_master_main AS
 WITH combined_data AS (
         SELECT issue_daily_main.item_category_code,
            issue_daily_main.item_category_name,
            issue_daily_main.item_code,
            issue_daily_main.item_name
           FROM public.issue_daily_main
          WHERE ((issue_daily_main.item_category_code IS NOT NULL) AND (issue_daily_main.item_code IS NOT NULL))
        UNION ALL
         SELECT pur_order_daily_main.item_category_code,
            pur_order_daily_main.item_category_name,
            pur_order_daily_main.item_code,
            pur_order_daily_main.item_name
           FROM public.pur_order_daily_main
          WHERE ((pur_order_daily_main.item_category_code IS NOT NULL) AND (pur_order_daily_main.item_code IS NOT NULL))
        UNION ALL
         SELECT grn_daily_main.item_ctag_code,
            grn_daily_main.item_ctag_name,
            grn_daily_main.item_code,
            grn_daily_main.item_name
           FROM public.grn_daily_main
          WHERE ((grn_daily_main.item_ctag_code IS NOT NULL) AND (grn_daily_main.item_code IS NOT NULL))
        ), ranked_data AS (
         SELECT combined_data.item_category_code,
            combined_data.item_code,
            combined_data.item_category_name,
            combined_data.item_name,
            row_number() OVER (PARTITION BY combined_data.item_category_code, combined_data.item_code ORDER BY (length((combined_data.item_category_name)::text)) DESC, (length((combined_data.item_name)::text)) DESC) AS rn
           FROM combined_data
        )
 SELECT item_category_code,
    item_category_name,
    item_code,
    item_name
   FROM ranked_data
  WHERE (rn = 1)
  ORDER BY item_category_code, item_code;


ALTER VIEW public.item_master_main OWNER TO postgres;

--
-- Name: pur_grn; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.pur_grn AS
 SELECT p.order_date AS pur_order_date,
    p.item_category_code,
    p.item_code AS pur_item_code,
    p.order_number AS pur_order_number,
    p.supplier_code,
    p.supplier_name,
    p.department,
    p.department_name,
    p.cost_project,
    p.cost_project_name,
    p.rate,
        CASE
            WHEN (row_number() OVER (PARTITION BY p.order_number, p.item_code ORDER BY g.grn_date) = 1) THEN p.order_value
            ELSE '0'::character varying
        END AS pur_order_value,
    g.grn_date,
    g.grn_number,
    g.net_amount AS grn_net_amount
   FROM (public.pur_order_daily_main p
     LEFT JOIN public.grn_daily_main g ON (((TRIM(BOTH FROM (p.order_number)::text) = TRIM(BOTH FROM (g.purchase_order_number)::text)) AND (TRIM(BOTH FROM (p.item_code)::text) = TRIM(BOTH FROM (g.item_code)::text)))));


ALTER VIEW public.pur_grn OWNER TO postgres;

--
-- Name: pur_order_daily_main_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pur_order_daily_main_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pur_order_daily_main_id_seq OWNER TO postgres;

--
-- Name: pur_order_daily_main_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pur_order_daily_main_id_seq OWNED BY public.pur_order_daily_main.id;


--
-- Name: supplier_master_main; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.supplier_master_main AS
 WITH combined_suppliers AS (
         SELECT pur_order_daily_main.supplier_code,
            pur_order_daily_main.supplier_name
           FROM public.pur_order_daily_main
          WHERE (pur_order_daily_main.supplier_code IS NOT NULL)
        UNION
         SELECT grn_daily_main.supplier_code,
            grn_daily_main.supplier_name
           FROM public.grn_daily_main
          WHERE (grn_daily_main.supplier_code IS NOT NULL)
        ), ranked_suppliers AS (
         SELECT combined_suppliers.supplier_code,
            combined_suppliers.supplier_name,
            row_number() OVER (PARTITION BY combined_suppliers.supplier_code ORDER BY (length((combined_suppliers.supplier_name)::text)) DESC) AS rn
           FROM combined_suppliers
        )
 SELECT supplier_code,
    supplier_name
   FROM ranked_suppliers
  WHERE (rn = 1)
  ORDER BY supplier_code;


ALTER VIEW public.supplier_master_main OWNER TO postgres;

--
-- Name: grn_daily_main id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grn_daily_main ALTER COLUMN id SET DEFAULT nextval('public.grn_daily_main_id_seq'::regclass);


--
-- Name: issue_daily_main id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_daily_main ALTER COLUMN id SET DEFAULT nextval('public.issue_daily_main_id_seq'::regclass);


--
-- Name: pur_order_daily_main id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pur_order_daily_main ALTER COLUMN id SET DEFAULT nextval('public.pur_order_daily_main_id_seq'::regclass);


--
-- Name: grn_daily_main grn_daily_main_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grn_daily_main
    ADD CONSTRAINT grn_daily_main_pkey PRIMARY KEY (id);


--
-- Name: grn_daily_main grn_main_unique_cols; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grn_daily_main
    ADD CONSTRAINT grn_main_unique_cols UNIQUE (grn_date, item_code, grn_number, purchase_order_number, department, cost_project);


--
-- Name: issue_daily_main issue_daily_main_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_daily_main
    ADD CONSTRAINT issue_daily_main_pkey PRIMARY KEY (id);


--
-- Name: issue_daily_main issue_main_unique_cols; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_daily_main
    ADD CONSTRAINT issue_main_unique_cols UNIQUE (issue_date, item_code, cost_centre_code, department_code);


--
-- Name: pur_order_daily_main pur_main_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pur_order_daily_main
    ADD CONSTRAINT pur_main_unique UNIQUE (order_date, item_code, order_number, department, cost_project);


--
-- Name: pur_order_daily_main pur_order_daily_main_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pur_order_daily_main
    ADD CONSTRAINT pur_order_daily_main_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

