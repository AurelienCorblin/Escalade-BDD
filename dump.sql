--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.adherents (
    email character varying(30) NOT NULL,
    mdp text NOT NULL,
    nom character varying(25),
    prenom character varying(25),
    niveau integer
);



CREATE TABLE public.appartient (
    id_ad character varying(30) NOT NULL,
    nom_cordee character varying(25) NOT NULL
);



CREATE TABLE public.guides (
    id_guide character varying(30) NOT NULL,
    niv_max integer NOT NULL
);




CREATE TABLE public.sorties (
    id_sortie integer NOT NULL,
    sortie_desc text NOT NULL,
    date_sortie date NOT NULL,
    niv_min integer NOT NULL,
    site_sortie character varying(25) NOT NULL,
    max_part integer NOT NULL,
    createur character varying(30) NOT NULL
);



CREATE VIEW public.controle_guide AS
 SELECT guides.id_guide,
    adherents.nom,
    adherents.prenom
   FROM (public.guides
     JOIN public.adherents ON (((guides.id_guide)::text = (adherents.email)::text)))
EXCEPT
 SELECT guides.id_guide,
    adherents.nom,
    adherents.prenom
   FROM ((public.guides
     JOIN public.adherents ON (((guides.id_guide)::text = (adherents.email)::text)))
     JOIN public.sorties ON (((guides.id_guide)::text = (sorties.createur)::text)))
  WHERE (sorties.date_sortie >= (CURRENT_DATE - '1 year'::interval));




CREATE TABLE public.cordee (
    nom_cordee character varying(25) NOT NULL
);


ALTER TABLE public.cordee OWNER TO aurelien;



CREATE TABLE public.difficulte (
    id_diff integer NOT NULL,
    diff_fr character varying(2),
    diff_am character varying(5),
    diff_en character varying(4)
);




CREATE SEQUENCE public.difficulte_id_diff_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;






CREATE TABLE public.escalade (
    esc_date date NOT NULL,
    nom_cordee character varying(25) NOT NULL,
    id_voie integer NOT NULL,
    nom_type character varying(25) NOT NULL
);



CREATE TABLE public.exerce (
    id_guide character varying(30) NOT NULL,
    localite character varying(25) NOT NULL
);




CREATE TABLE public.participe (
    id_ad character varying(30) NOT NULL,
    id_sortie integer NOT NULL
);




CREATE TABLE public.sitesescalade (
    nom_site character varying(25) NOT NULL,
    localite character varying(25)
);




CREATE SEQUENCE public.sorties_id_sortie_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;





CREATE TABLE public.suit (
    voie_suivi integer NOT NULL,
    id_voie2 integer NOT NULL
);




CREATE TABLE public.voie (
    id_voie integer NOT NULL,
    nom_voie character varying(25),
    longueur integer,
    type_voie character varying(25),
    nom_site character varying(25),
    diff integer
);




CREATE VIEW public.top_5_sites AS
 SELECT voie.nom_site
   FROM ((public.escalade
     JOIN public.voie USING (id_voie))
     JOIN public.appartient USING (nom_cordee))
  WHERE (( SELECT EXTRACT(year FROM escalade.esc_date) AS "extract") = ( SELECT EXTRACT(year FROM CURRENT_DATE) AS "extract"))
  GROUP BY voie.nom_site
  ORDER BY (count(voie.nom_voie)) DESC
 LIMIT 5;




CREATE TABLE public.typesescalade (
    nom_type character varying(25) NOT NULL,
    desc_type text
);




CREATE SEQUENCE public.voie_id_voie_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;








ALTER TABLE ONLY public.difficulte ALTER COLUMN id_diff SET DEFAULT nextval('public.difficulte_id_diff_seq'::regclass);




ALTER TABLE ONLY public.sorties ALTER COLUMN id_sortie SET DEFAULT nextval('public.sorties_id_sortie_seq'::regclass);




ALTER TABLE ONLY public.voie ALTER COLUMN id_voie SET DEFAULT nextval('public.voie_id_voie_seq'::regclass);




COPY public.adherents (email, mdp, nom, prenom, niveau) FROM stdin;
martin3424@gmail.com	$2b$12$zg1CHK/DNfQPjU0t/JyZlOa4tT3Qdv3vR7Uonw.hDN.ixcO6MwDKW	martin	thomas	14
fabremax@gmail.com	$2b$12$1vk8RX1DRmWk44l.nK04A.ZCoVk/EDnknZKUpzv7kaSKYmIcN5OVG	fabre	max	5
milletemma@gmail.com	$2b$12$1KyfRJs1OKrcVEiZE.bvVO9rTIlw4iRg7MwUfikKgNLC0b1TAfE3K	millet	emma	11
duboischarlie@gmail.com	$2b$12$JFcrzdQ4gVaYcsoB8GMx4uWeqc5HtYalLzG4xomvt0fZqIPdWELhi	dubois	charlie	17
rouxsophie@gmail.com	$2b$12$n3wYTza3ChqyEvyFSH7u2O5YL8eI2RDMJ5yxsYpBAW1vwHe2ybWeG	roux	sophie	15
\.




COPY public.appartient (id_ad, nom_cordee) FROM stdin;
rouxsophie@gmail.com	groupe amies
martin3424@gmail.com	groupe amies
milletemma@gmail.com	groupe amies
duboischarlie@gmail.com	groupe pro
fabremax@gmail.com	groupe pro
fabremax@gmail.com	groupe amies
rouxsophie@gmail.com	amateur
martin3424@gmail.com	amateur
\.



COPY public.cordee (nom_cordee) FROM stdin;
groupe amies
groupe pro
amateur
\.




COPY public.difficulte (id_diff, diff_fr, diff_am, diff_en) FROM stdin;
1	1	5.1	easy
2	2	5.3	M
3	3	5.4	D
4	4	5.5	HVD
5	5a	5.6	MS
6	5b	5.7	VS
7	5c	5.8	HVS
8	6a	5.9	E1
9	6b	5.10c	E2
10	6c	5.11a	E3
11	7a	5.11d	E4
12	7b	5.12b	E5
13	7c	5.12d	E6
14	8a	5.13b	E7
15	8b	5.13d	E8
16	8c	5.14b	E9
17	9a	5.14d	E10
18	9b	5.15b	E11
19	9c	5.15d	E12
\.




COPY public.escalade (esc_date, nom_cordee, id_voie, nom_type) FROM stdin;
2022-01-13	groupe amies	1	traditionnelle
2022-02-02	groupe amies	3	solo intégral
2022-04-03	groupe amies	5	libre
2022-09-01	groupe amies	7	sportive
2022-02-05	groupe amies	16	libre
2022-09-17	groupe amies	13	traditionnelle
2022-07-30	groupe amies	11	traditionnelle
2022-12-24	groupe pro	3	sportive
2022-10-12	groupe pro	5	artificielle
2022-05-06	groupe pro	7	solo intégral
2020-05-06	groupe pro	15	solo intégral
2018-05-06	groupe amies	12	solo intégral
2022-10-27	groupe pro	9	traditionnelle
2022-11-20	groupe amies	16	sportive
2022-05-23	groupe amies	11	libre
2022-10-28	groupe amies	9	solo intégral
2022-01-07	groupe pro	7	traditionnelle
2022-03-02	groupe amies	5	traditionnelle
2022-03-03	groupe amies	5	traditionnelle
2022-03-05	groupe amies	5	traditionnelle
\.




COPY public.exerce (id_guide, localite) FROM stdin;
rouxsophie@gmail.com	Thorens
rouxsophie@gmail.com	Nice
rouxsophie@gmail.com	arudy
martin3424@gmail.com	Thorens
fabremax@gmail.com	Ailefroide
martin3424@gmail.com	Nice
\.




COPY public.guides (id_guide, niv_max) FROM stdin;
rouxsophie@gmail.com	15
fabremax@gmail.com	5
martin3424@gmail.com	14
\.




COPY public.participe (id_ad, id_sortie) FROM stdin;
martin3424@gmail.com	1
martin3424@gmail.com	3
milletemma@gmail.com	1
duboischarlie@gmail.com	2
rouxsophie@gmail.com	2
fabremax@gmail.com	1
duboischarlie@gmail.com	3
\.




COPY public.sitesescalade (nom_site, localite) FROM stdin;
ablon	Thorens
annot	Nice
ailefroide	Ailefroide
arsine	Villar-d’Arêne
arudy	arudy
autoire	autoire
\.




COPY public.sorties (id_sortie, sortie_desc, date_sortie, niv_min, site_sortie, max_part, createur) FROM stdin;
1	sortie entre amies	2022-04-03	2	ablon	5	rouxsophie@gmail.com
2	sortie entre amies	2022-11-21	5	annot	5	milletemma@gmail.com
3	sortie entre amies	2020-05-12	7	autoire	5	rouxsophie@gmail.com
4	sortie pro	2021-11-13	1	arsine	5	fabremax@gmail.com
\.




COPY public.suit (voie_suivi, id_voie2) FROM stdin;
1	4
3	2
6	7
3	11
13	14
7	3
9	5
10	9
\.




COPY public.typesescalade (nom_type, desc_type) FROM stdin;
traditionnelle	le grimpeur pose ses points d’ancrage au fur et à mesure qu’il monte
sportive	les ancrages sont permanent et fixé sur la voie à son ouverture
artificielle	le grimpeur use d’outils en plus des prises de la voie pour l’aider dans son ascension
libre	ascension, généralement courte, sans être assuré
solo intégral	grimper de grandes voies sans être assuré
\.



COPY public.voie (id_voie, nom_voie, longueur, type_voie, nom_site, diff) FROM stdin;
1	voie 1	4	bloc	ablon	1
2	voie 2	2	falaise	annot	5
3	voie 3	1	falaise	ailefroide	5
4	voie 4	6	falaise	arsine	3
5	voie 5	4	bloc	autoire	2
6	voie 6	3	bloc	ablon	1
7	voie 7	5	bloc	arudy	9
8	voie 8	9	falaise	ailefroide	2
9	voie 9	1	bloc	annot	4
10	voie 10	3	bloc	arudy	3
11	voie 11	3	falaise	ablon	4
12	voie 12	5	bloc	autoire	7
13	voie 13	2	falaise	arsine	2
14	voie 14	7	bloc	autoire	4
15	voie 15	6	bloc	ailefroide	11
16	voie 16	8	falaise	annot	1
17	voie 17	3	falaise	arudy	2
18	voie 18	1	falaise	arsine	3
\.




SELECT pg_catalog.setval('public.difficulte_id_diff_seq', 19, true);




SELECT pg_catalog.setval('public.sorties_id_sortie_seq', 4, true);




SELECT pg_catalog.setval('public.voie_id_voie_seq', 18, true);




ALTER TABLE ONLY public.adherents
    ADD CONSTRAINT adherents_pkey PRIMARY KEY (email);




ALTER TABLE ONLY public.appartient
    ADD CONSTRAINT appartient_pkey PRIMARY KEY (id_ad, nom_cordee);



ALTER TABLE ONLY public.cordee
    ADD CONSTRAINT cordee_pkey PRIMARY KEY (nom_cordee);



ALTER TABLE ONLY public.difficulte
    ADD CONSTRAINT difficulte_pkey PRIMARY KEY (id_diff);



ALTER TABLE ONLY public.escalade
    ADD CONSTRAINT escalade_pkey PRIMARY KEY (esc_date, nom_cordee, id_voie, nom_type);



ALTER TABLE ONLY public.exerce
    ADD CONSTRAINT exerce_pkey PRIMARY KEY (id_guide, localite);




ALTER TABLE ONLY public.guides
    ADD CONSTRAINT guides_pkey PRIMARY KEY (id_guide);




ALTER TABLE ONLY public.participe
    ADD CONSTRAINT participe_pkey PRIMARY KEY (id_ad, id_sortie);


ALTER TABLE ONLY public.sitesescalade
    ADD CONSTRAINT sitesescalade_localite_key UNIQUE (localite);



ALTER TABLE ONLY public.sitesescalade
    ADD CONSTRAINT sitesescalade_pkey PRIMARY KEY (nom_site);




ALTER TABLE ONLY public.sorties
    ADD CONSTRAINT sorties_pkey PRIMARY KEY (id_sortie);




ALTER TABLE ONLY public.suit
    ADD CONSTRAINT suit_pkey PRIMARY KEY (voie_suivi, id_voie2);




ALTER TABLE ONLY public.typesescalade
    ADD CONSTRAINT typesescalade_pkey PRIMARY KEY (nom_type);




ALTER TABLE ONLY public.voie
    ADD CONSTRAINT voie_pkey PRIMARY KEY (id_voie);




ALTER TABLE ONLY public.adherents
    ADD CONSTRAINT adherents_niveau_fkey FOREIGN KEY (niveau) REFERENCES public.difficulte(id_diff) ON UPDATE CASCADE;




ALTER TABLE ONLY public.appartient
    ADD CONSTRAINT appartient_id_ad_fkey FOREIGN KEY (id_ad) REFERENCES public.adherents(email);




ALTER TABLE ONLY public.appartient
    ADD CONSTRAINT appartient_nom_cordee_fkey FOREIGN KEY (nom_cordee) REFERENCES public.cordee(nom_cordee) ON UPDATE CASCADE;




ALTER TABLE ONLY public.escalade
    ADD CONSTRAINT escalade_id_voie_fkey FOREIGN KEY (id_voie) REFERENCES public.voie(id_voie);



ALTER TABLE ONLY public.escalade
    ADD CONSTRAINT escalade_nom_cordee_fkey FOREIGN KEY (nom_cordee) REFERENCES public.cordee(nom_cordee);



ALTER TABLE ONLY public.escalade
    ADD CONSTRAINT escalade_nom_type_fkey FOREIGN KEY (nom_type) REFERENCES public.typesescalade(nom_type) ON UPDATE CASCADE;




ALTER TABLE ONLY public.exerce
    ADD CONSTRAINT exerce_id_guide_fkey FOREIGN KEY (id_guide) REFERENCES public.guides(id_guide);



ALTER TABLE ONLY public.exerce
    ADD CONSTRAINT exerce_localite_fkey FOREIGN KEY (localite) REFERENCES public.sitesescalade(localite) ON UPDATE CASCADE;




ALTER TABLE ONLY public.guides
    ADD CONSTRAINT guides_id_guide_fkey FOREIGN KEY (id_guide) REFERENCES public.adherents(email);




ALTER TABLE ONLY public.guides
    ADD CONSTRAINT guides_niv_max_fkey FOREIGN KEY (niv_max) REFERENCES public.difficulte(id_diff) ON UPDATE CASCADE;




ALTER TABLE ONLY public.participe
    ADD CONSTRAINT participe_id_ad_fkey FOREIGN KEY (id_ad) REFERENCES public.adherents(email);



ALTER TABLE ONLY public.participe
    ADD CONSTRAINT participe_id_sortie_fkey FOREIGN KEY (id_sortie) REFERENCES public.sorties(id_sortie) ON UPDATE CASCADE;




ALTER TABLE ONLY public.sorties
    ADD CONSTRAINT sorties_niv_min_fkey FOREIGN KEY (niv_min) REFERENCES public.difficulte(id_diff) ON UPDATE CASCADE;




ALTER TABLE ONLY public.suit
    ADD CONSTRAINT suit_id_voie2_fkey FOREIGN KEY (id_voie2) REFERENCES public.voie(id_voie);




ALTER TABLE ONLY public.suit
    ADD CONSTRAINT suit_voie_suivi_fkey FOREIGN KEY (voie_suivi) REFERENCES public.voie(id_voie);



ALTER TABLE ONLY public.voie
    ADD CONSTRAINT voie_diff_fkey FOREIGN KEY (diff) REFERENCES public.difficulte(id_diff) ON UPDATE CASCADE;




ALTER TABLE ONLY public.voie
    ADD CONSTRAINT voie_nom_site_fkey FOREIGN KEY (nom_site) REFERENCES public.sitesescalade(nom_site);


--
-- PostgreSQL database dump complete
--

