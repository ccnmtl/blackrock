--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: mammals_labelmenu; Type: TABLE DATA; Schema: public; Owner: eddie
--

INSERT INTO mammals_labelmenu (id, label) VALUES (1, 'Adult');
INSERT INTO mammals_labelmenu (id, label) VALUES (2, 'Juvenile');
INSERT INTO mammals_labelmenu (id, label) VALUES (3, 'Young of year');
INSERT INTO mammals_labelmenu (id, label) VALUES (4, 'Male');
INSERT INTO mammals_labelmenu (id, label) VALUES (5, 'Female');
INSERT INTO mammals_labelmenu (id, label) VALUES (6, '30g');
INSERT INTO mammals_labelmenu (id, label) VALUES (7, '100g');
INSERT INTO mammals_labelmenu (id, label) VALUES (8, '300g');
INSERT INTO mammals_labelmenu (id, label) VALUES (9, '1kg');
INSERT INTO mammals_labelmenu (id, label) VALUES (10, '5kg');
INSERT INTO mammals_labelmenu (id, label) VALUES (11, '20kg');
INSERT INTO mammals_labelmenu (id, label) VALUES (12, '50kg');
INSERT INTO mammals_labelmenu (id, label) VALUES (13, '10 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (14, '20 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (15, '30 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (16, '40 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (17, '50 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (18, '60 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (19, '70 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (21, '80 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (22, '90 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (23, '100 %');
INSERT INTO mammals_labelmenu (id, label) VALUES (33, 'Rain');
INSERT INTO mammals_labelmenu (id, label) VALUES (34, 'Snow');
INSERT INTO mammals_labelmenu (id, label) VALUES (35, '0 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (36, '1 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (37, '2 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (38, '3 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (39, '4 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (40, '5 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (41, '6 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (42, '7 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (43, '8 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (44, '9 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (45, '10 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (46, '> 10 cm');
INSERT INTO mammals_labelmenu (id, label) VALUES (47, '-10');
INSERT INTO mammals_labelmenu (id, label) VALUES (48, '-5');
INSERT INTO mammals_labelmenu (id, label) VALUES (49, '0');
INSERT INTO mammals_labelmenu (id, label) VALUES (50, '5');
INSERT INTO mammals_labelmenu (id, label) VALUES (51, '10');
INSERT INTO mammals_labelmenu (id, label) VALUES (52, '15');
INSERT INTO mammals_labelmenu (id, label) VALUES (53, '20');
INSERT INTO mammals_labelmenu (id, label) VALUES (54, '25');
INSERT INTO mammals_labelmenu (id, label) VALUES (55, '30');
INSERT INTO mammals_labelmenu (id, label) VALUES (56, '100lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (57, '200lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (58, '500lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (59, '1,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (60, '2,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (61, '5,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (62, '10,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (63, '20,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (64, '50,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (65, '100,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (66, '>100,000lx');
INSERT INTO mammals_labelmenu (id, label) VALUES (32, '1-New moon');
INSERT INTO mammals_labelmenu (id, label) VALUES (31, '2');
INSERT INTO mammals_labelmenu (id, label) VALUES (30, '3');
INSERT INTO mammals_labelmenu (id, label) VALUES (29, '4');
INSERT INTO mammals_labelmenu (id, label) VALUES (28, '5');
INSERT INTO mammals_labelmenu (id, label) VALUES (27, '6');
INSERT INTO mammals_labelmenu (id, label) VALUES (26, '7');
INSERT INTO mammals_labelmenu (id, label) VALUES (25, '8');
INSERT INTO mammals_labelmenu (id, label) VALUES (24, '9');
INSERT INTO mammals_labelmenu (id, label) VALUES (67, '10');
INSERT INTO mammals_labelmenu (id, label) VALUES (68, '11');
INSERT INTO mammals_labelmenu (id, label) VALUES (69, '12');
INSERT INTO mammals_labelmenu (id, label) VALUES (70, '13');
INSERT INTO mammals_labelmenu (id, label) VALUES (71, '14');
INSERT INTO mammals_labelmenu (id, label) VALUES (73, '16');
INSERT INTO mammals_labelmenu (id, label) VALUES (74, '17');
INSERT INTO mammals_labelmenu (id, label) VALUES (75, '18');
INSERT INTO mammals_labelmenu (id, label) VALUES (76, '19');
INSERT INTO mammals_labelmenu (id, label) VALUES (77, '20');
INSERT INTO mammals_labelmenu (id, label) VALUES (78, '21');
INSERT INTO mammals_labelmenu (id, label) VALUES (79, '22');
INSERT INTO mammals_labelmenu (id, label) VALUES (80, '23');
INSERT INTO mammals_labelmenu (id, label) VALUES (81, '24');
INSERT INTO mammals_labelmenu (id, label) VALUES (82, '25');
INSERT INTO mammals_labelmenu (id, label) VALUES (83, '26');
INSERT INTO mammals_labelmenu (id, label) VALUES (84, '27');
INSERT INTO mammals_labelmenu (id, label) VALUES (85, '28');
INSERT INTO mammals_labelmenu (id, label) VALUES (86, '29-Day before new');
INSERT INTO mammals_labelmenu (id, label) VALUES (72, '15-Full moon');
INSERT INTO mammals_labelmenu (id, label) VALUES (91, 'Sighting');
INSERT INTO mammals_labelmenu (id, label) VALUES (92, 'Camera-trapped');
INSERT INTO mammals_labelmenu (id, label) VALUES (93, 'Mortality');
INSERT INTO mammals_labelmenu (id, label) VALUES (94, 'Scat');
INSERT INTO mammals_labelmenu (id, label) VALUES (95, 'Tracks');
INSERT INTO mammals_labelmenu (id, label) VALUES (96, 'Hair');
INSERT INTO mammals_labelmenu (id, label) VALUES (97, 'Scratching');
INSERT INTO mammals_labelmenu (id, label) VALUES (98, 'Sound heard');
INSERT INTO mammals_labelmenu (id, label) VALUES (99, 'Beaver Dam');
INSERT INTO mammals_labelmenu (id, label) VALUES (100, 'Other (see notes)');


--
-- Name: mammals_labelmenu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eddie
--

SELECT pg_catalog.setval('mammals_labelmenu_id_seq', 97, true);


--
-- Data for Name: mammals_observationtype; Type: TABLE DATA; Schema: public; Owner: eddie
--

INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (87);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (89);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (90);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (91);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (92);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (93);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (94);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (95);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (96);
INSERT INTO mammals_observationtype (labelmenu_ptr_id) VALUES (97);


--
-- PostgreSQL database dump complete
--

