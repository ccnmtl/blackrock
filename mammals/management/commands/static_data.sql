--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: portal_digitalformat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_digitalformat_id_seq', 7, true);


--
-- Name: portal_digitalobjecttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_digitalobjecttype_id_seq', 4, true);


--
-- Name: portal_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_institution_id_seq', 4, true);


--
-- Name: portal_keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_keyword_id_seq', 8, true);


--
-- Name: portal_locationsubtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_locationsubtype_id_seq', 2, true);


--
-- Name: portal_locationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_locationtype_id_seq', 5, true);


--
-- Name: portal_persontype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_persontype_id_seq', 9, true);


--
-- Name: portal_publicationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_publicationtype_id_seq', 2, true);


--
-- Name: portal_regiontype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_regiontype_id_seq', 3, true);


--
-- Name: portal_rightstype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('portal_rightstype_id_seq', 1, true);


--
-- Data for Name: portal_digitalformat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_digitalformat (id, name) FROM stdin;
1	text
2	audio
3	software
4	video
5	map
6	image
7	web
\.


--
-- Data for Name: portal_digitalobjecttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_digitalobjecttype (id, name) FROM stdin;
1	trail
2	topographical
3	historical
4	aerial
\.


--
-- Data for Name: portal_institution; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_institution (id, name) FROM stdin;
1	Black Rock Forest
2	Columbia University
3	Lamont-Doherty
4	Barnard College
\.


--
-- Data for Name: portal_keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_keyword (id, name) FROM stdin;
1	location
2	map
3	pond
4	hill
5	station
6	blackrock staff
7	Lamont-Doherty
8	research
\.


--
-- Data for Name: portal_locationsubtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_locationsubtype (id, name) FROM stdin;
1	Thinned
2	Control
\.


--
-- Data for Name: portal_locationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_locationtype (id, name) FROM stdin;
1	Long-term Tree Plot
2	Hill
3	Building
4	Water Body
5	Forest
\.


--
-- Data for Name: portal_persontype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_persontype (id, name) FROM stdin;
1	College Instructor
2	Scientist
3	Forest Staff
4	Master's Candidate
5	Undergraduate Student
6	Museum Curator
7	High School Teacher
8	Self Learner
9	Academic Group
\.


--
-- Data for Name: portal_publicationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_publicationtype (id, name) FROM stdin;
1	Journal
2	Book
\.


--
-- Data for Name: portal_regiontype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_regiontype (id, name) FROM stdin;
1	Watershed
2	Vegetation
3	Compartment
\.


--
-- Data for Name: portal_rightstype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY portal_rightstype (id, name) FROM stdin;
1	Open
\.


--
-- PostgreSQL database dump complete
--

