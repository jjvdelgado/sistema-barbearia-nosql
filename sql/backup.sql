--
-- PostgreSQL database dump
--

\restrict hA2cZzjZ7y7RMxtUIARxtlh2Vz6ArHbQOFGaucfOFO3MNNn2wNo0DLfIm7ddJd4

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

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
-- Name: atendimento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.atendimento (
    id_atendimento integer NOT NULL,
    id_cliente integer NOT NULL,
    id_barbeiro integer NOT NULL,
    tipo character varying(20) DEFAULT 'walkin'::character varying,
    data_agendada date,
    horario_agendado time without time zone,
    data_atendimento date DEFAULT CURRENT_DATE,
    horario_inicio time without time zone,
    horario_fim time without time zone,
    status character varying(20) DEFAULT 'agendado'::character varying,
    valor_total numeric(10,2),
    forma_pagamento character varying(20),
    observacoes text
);


ALTER TABLE public.atendimento OWNER TO postgres;

--
-- Name: atendimento_id_atendimento_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.atendimento_id_atendimento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.atendimento_id_atendimento_seq OWNER TO postgres;

--
-- Name: atendimento_id_atendimento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.atendimento_id_atendimento_seq OWNED BY public.atendimento.id_atendimento;


--
-- Name: atendimento_servico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.atendimento_servico (
    id_atendimento integer NOT NULL,
    id_servico integer NOT NULL,
    preco_cobrado numeric(10,2) NOT NULL
);


ALTER TABLE public.atendimento_servico OWNER TO postgres;

--
-- Name: barbeiro; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.barbeiro (
    id_barbeiro integer NOT NULL,
    nome character varying(100) NOT NULL,
    cpf character varying(11) NOT NULL,
    telefone character varying(15) NOT NULL,
    email character varying(100),
    data_contratacao date DEFAULT CURRENT_DATE,
    especialidade character varying(50),
    comissao_percentual numeric(5,2) DEFAULT 30.00,
    ativo boolean DEFAULT true
);


ALTER TABLE public.barbeiro OWNER TO postgres;

--
-- Name: barbeiro_id_barbeiro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.barbeiro_id_barbeiro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.barbeiro_id_barbeiro_seq OWNER TO postgres;

--
-- Name: barbeiro_id_barbeiro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.barbeiro_id_barbeiro_seq OWNED BY public.barbeiro.id_barbeiro;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    id_cliente integer NOT NULL,
    nome character varying(100) NOT NULL,
    cpf character varying(11) NOT NULL,
    telefone character varying(15) NOT NULL,
    email character varying(100),
    data_nascimento date,
    data_cadastro date DEFAULT CURRENT_DATE,
    observacoes text
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_id_cliente_seq OWNER TO postgres;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_cliente_seq OWNED BY public.cliente.id_cliente;


--
-- Name: horario_trabalho; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horario_trabalho (
    id_horario integer NOT NULL,
    id_barbeiro integer NOT NULL,
    dia_semana integer NOT NULL,
    horario_inicio time without time zone NOT NULL,
    horario_fim time without time zone NOT NULL,
    ativo boolean DEFAULT true
);


ALTER TABLE public.horario_trabalho OWNER TO postgres;

--
-- Name: horario_trabalho_id_horario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horario_trabalho_id_horario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horario_trabalho_id_horario_seq OWNER TO postgres;

--
-- Name: horario_trabalho_id_horario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horario_trabalho_id_horario_seq OWNED BY public.horario_trabalho.id_horario;


--
-- Name: produto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produto (
    id_produto integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    preco_venda numeric(10,2) NOT NULL,
    estoque_atual integer DEFAULT 0,
    estoque_minimo integer DEFAULT 5,
    ativo boolean DEFAULT true
);


ALTER TABLE public.produto OWNER TO postgres;

--
-- Name: produto_id_produto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produto_id_produto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produto_id_produto_seq OWNER TO postgres;

--
-- Name: produto_id_produto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produto_id_produto_seq OWNED BY public.produto.id_produto;


--
-- Name: servico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servico (
    id_servico integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    preco numeric(10,2) NOT NULL,
    duracao_estimada integer NOT NULL,
    ativo boolean DEFAULT true
);


ALTER TABLE public.servico OWNER TO postgres;

--
-- Name: servico_id_servico_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servico_id_servico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.servico_id_servico_seq OWNER TO postgres;

--
-- Name: servico_id_servico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servico_id_servico_seq OWNED BY public.servico.id_servico;


--
-- Name: venda_produto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venda_produto (
    id_venda integer NOT NULL,
    id_atendimento integer NOT NULL,
    id_produto integer NOT NULL,
    quantidade integer NOT NULL,
    preco_unitario numeric(10,2) NOT NULL,
    subtotal numeric(10,2) NOT NULL
);


ALTER TABLE public.venda_produto OWNER TO postgres;

--
-- Name: venda_produto_id_venda_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.venda_produto_id_venda_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.venda_produto_id_venda_seq OWNER TO postgres;

--
-- Name: venda_produto_id_venda_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.venda_produto_id_venda_seq OWNED BY public.venda_produto.id_venda;


--
-- Name: atendimento id_atendimento; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento ALTER COLUMN id_atendimento SET DEFAULT nextval('public.atendimento_id_atendimento_seq'::regclass);


--
-- Name: barbeiro id_barbeiro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.barbeiro ALTER COLUMN id_barbeiro SET DEFAULT nextval('public.barbeiro_id_barbeiro_seq'::regclass);


--
-- Name: cliente id_cliente; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id_cliente SET DEFAULT nextval('public.cliente_id_cliente_seq'::regclass);


--
-- Name: horario_trabalho id_horario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario_trabalho ALTER COLUMN id_horario SET DEFAULT nextval('public.horario_trabalho_id_horario_seq'::regclass);


--
-- Name: produto id_produto; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto ALTER COLUMN id_produto SET DEFAULT nextval('public.produto_id_produto_seq'::regclass);


--
-- Name: servico id_servico; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servico ALTER COLUMN id_servico SET DEFAULT nextval('public.servico_id_servico_seq'::regclass);


--
-- Name: venda_produto id_venda; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venda_produto ALTER COLUMN id_venda SET DEFAULT nextval('public.venda_produto_id_venda_seq'::regclass);


--
-- Data for Name: atendimento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.atendimento (id_atendimento, id_cliente, id_barbeiro, tipo, data_agendada, horario_agendado, data_atendimento, horario_inicio, horario_fim, status, valor_total, forma_pagamento, observacoes) FROM stdin;
1	1	1	agendado	2025-10-03	09:00:00	\N	\N	\N	agendado	\N	\N	\N
2	2	2	agendado	2025-10-03	10:00:00	\N	\N	\N	agendado	\N	\N	\N
3	3	3	agendado	2025-10-04	14:00:00	\N	\N	\N	agendado	\N	\N	\N
4	4	1	agendado	2025-10-04	11:00:00	\N	\N	\N	agendado	\N	\N	\N
5	5	4	agendado	2025-10-05	15:00:00	\N	\N	\N	agendado	\N	\N	\N
6	1	1	walkin	\N	\N	2025-09-27	09:00:00	09:30:00	finalizado	40.00	pix	Cliente satisfeito
7	3	3	walkin	\N	\N	2025-09-29	14:00:00	14:40:00	finalizado	50.00	dinheiro	\N
8	5	2	walkin	\N	\N	2025-10-01	15:00:00	15:25:00	finalizado	35.00	cartao_credito	\N
9	2	2	agendado	2025-09-28	10:00:00	2025-09-28	10:05:00	10:50:00	finalizado	70.00	cartao_debito	Cliente chegou no horário
10	4	1	agendado	2025-09-30	11:00:00	2025-09-30	11:00:00	11:50:00	finalizado	70.00	pix	\N
12	8	1	agendado	2025-10-03	15:15:00	\N	\N	\N	agendado	\N	\N	\N
11	8	2	walkin	\N	\N	2025-10-02	00:17:00	00:19:00	finalizado	140.00	pix	\N
\.


--
-- Data for Name: atendimento_servico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.atendimento_servico (id_atendimento, id_servico, preco_cobrado) FROM stdin;
6	1	40.00
7	2	70.00
8	5	50.00
9	2	70.00
10	3	35.00
11	8	120.00
11	7	20.00
\.


--
-- Data for Name: barbeiro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.barbeiro (id_barbeiro, nome, cpf, telefone, email, data_contratacao, especialidade, comissao_percentual, ativo) FROM stdin;
1	Roberto "Tesoura de Ouro" Silva	11122233344	47988887777	roberto.silva@barbearia.com	2020-01-15	corte	35.00	t
2	Anderson "Barba Perfeita" Costa	22233344455	47977776666	anderson.costa@barbearia.com	2020-06-20	barba	30.00	t
3	Felipe "Designer" Santos	33344455566	47966665555	felipe.santos@barbearia.com	2021-03-10	designer	32.00	t
4	Marcelo "Estilista" Oliveira	44455566677	47955554444	marcelo.oliveira@barbearia.com	2021-09-01	coloração	35.00	t
5	Thiago "Clássico" Pereira	55566677788	47944443333	thiago.pereira@barbearia.com	2022-02-14	corte	30.00	t
\.


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (id_cliente, nome, cpf, telefone, email, data_nascimento, data_cadastro, observacoes) FROM stdin;
1	João Silva Santos	12345678901	47999887766	joao.silva@email.com	1985-03-15	2025-10-02	Alérgico a produtos com mentol
2	Pedro Oliveira Costa	23456789012	47988776655	pedro.oliveira@email.com	1990-07-22	2025-10-02	\N
3	Carlos Eduardo Souza	34567890123	47977665544	carlos.souza@email.com	1988-11-30	2025-10-02	Prefere cortes degradê
4	Lucas Ferreira Lima	45678901234	47966554433	lucas.lima@email.com	1995-05-18	2025-10-02	\N
5	Rafael Mendes Alves	56789012345	47955443322	rafael.alves@email.com	1992-09-25	2025-10-02	Cliente VIP
6	Marcos Paulo Santos	67890123456	47944332211	marcos.santos@email.com	1987-01-10	2025-10-02	\N
7	Fernando Costa Silva	78901234567	47933221100	fernando.silva@email.com	1993-06-08	2025-10-02	Gosta de conversar durante o corte
8	André Luiz Pereira	89012345678	47922110099	andre.pereira@email.com	1991-12-14	2025-10-02	\N
9	Bruno Henrique Rocha	90123456789	47911009988	bruno.rocha@email.com	1989-04-20	2025-10-02	Pele sensível
10	Rodrigo Martins Dias	01234567890	47900998877	rodrigo.dias@email.com	1994-08-03	2025-10-02	\N
\.


--
-- Data for Name: horario_trabalho; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horario_trabalho (id_horario, id_barbeiro, dia_semana, horario_inicio, horario_fim, ativo) FROM stdin;
1	1	1	08:00:00	18:00:00	t
2	1	2	08:00:00	18:00:00	t
3	1	3	08:00:00	18:00:00	t
4	1	4	08:00:00	18:00:00	t
5	1	5	08:00:00	18:00:00	t
6	2	1	09:00:00	19:00:00	t
7	2	2	09:00:00	19:00:00	t
8	2	3	09:00:00	19:00:00	t
9	2	4	09:00:00	19:00:00	t
10	2	5	09:00:00	19:00:00	t
11	2	6	09:00:00	17:00:00	t
12	3	2	10:00:00	20:00:00	t
13	3	3	10:00:00	20:00:00	t
14	3	4	10:00:00	20:00:00	t
15	3	5	10:00:00	20:00:00	t
16	3	6	10:00:00	18:00:00	t
17	4	1	09:00:00	18:00:00	t
18	4	2	09:00:00	18:00:00	t
19	4	3	09:00:00	18:00:00	t
20	4	4	09:00:00	18:00:00	t
21	4	5	09:00:00	18:00:00	t
22	5	3	10:00:00	20:00:00	t
23	5	4	10:00:00	20:00:00	t
24	5	5	10:00:00	20:00:00	t
25	5	6	10:00:00	18:00:00	t
26	5	0	10:00:00	16:00:00	t
\.


--
-- Data for Name: produto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produto (id_produto, nome, descricao, preco_venda, estoque_atual, estoque_minimo, ativo) FROM stdin;
1	Pomada Modeladora	Pomada para modelar cabelo - fixação forte	35.00	25	5	t
2	Cera Modeladora	Cera para finalização - fixação média	32.00	30	5	t
3	Óleo para Barba	Óleo hidratante para barba	45.00	15	3	t
4	Shampoo Anticaspa	Shampoo especial anticaspa	28.00	40	8	t
5	Gel Fixador	Gel para cabelo - fixação extra forte	25.00	20	5	t
6	Balm para Barba	Balm hidratante e modelador	40.00	18	3	t
7	Condicionador	Condicionador profissional	30.00	35	8	t
8	Spray Finalizador	Spray para finalização de corte	38.00	22	5	t
9	Máscara Capilar	Máscara de tratamento intensivo	55.00	12	3	t
10	Talco para Barba	Talco pós-barba	22.00	28	5	t
\.


--
-- Data for Name: servico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servico (id_servico, nome, descricao, preco, duracao_estimada, ativo) FROM stdin;
1	Corte Simples	Corte de cabelo tradicional	40.00	30	t
2	Corte + Barba	Corte de cabelo + barba completa	70.00	50	t
3	Barba Completa	Aparar, desenhar e finalizar barba	35.00	25	t
4	Designer de Barba	Designer e acabamento especial de barba	45.00	35	t
5	Corte Degradê	Corte degradê moderno	50.00	40	t
6	Corte + Barba + Sobrancelha	Combo completo	85.00	60	t
7	Sobrancelha	Designer de sobrancelha masculina	20.00	15	t
8	Platinado/Coloração	Coloração ou descoloração capilar	120.00	90	t
9	Luzes/Reflexos	Aplicação de luzes ou reflexos	150.00	120	t
10	Tratamento Capilar	Hidratação e tratamento	80.00	45	t
\.


--
-- Data for Name: venda_produto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venda_produto (id_venda, id_atendimento, id_produto, quantidade, preco_unitario, subtotal) FROM stdin;
1	6	1	1	35.00	35.00
2	7	3	1	45.00	45.00
3	9	1	1	35.00	35.00
4	9	6	1	40.00	40.00
5	10	10	1	22.00	22.00
\.


--
-- Name: atendimento_id_atendimento_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.atendimento_id_atendimento_seq', 12, true);


--
-- Name: barbeiro_id_barbeiro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.barbeiro_id_barbeiro_seq', 5, true);


--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_cliente_seq', 10, true);


--
-- Name: horario_trabalho_id_horario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horario_trabalho_id_horario_seq', 26, true);


--
-- Name: produto_id_produto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produto_id_produto_seq', 10, true);


--
-- Name: servico_id_servico_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servico_id_servico_seq', 10, true);


--
-- Name: venda_produto_id_venda_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venda_produto_id_venda_seq', 5, true);


--
-- Name: atendimento atendimento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento
    ADD CONSTRAINT atendimento_pkey PRIMARY KEY (id_atendimento);


--
-- Name: atendimento_servico atendimento_servico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento_servico
    ADD CONSTRAINT atendimento_servico_pkey PRIMARY KEY (id_atendimento, id_servico);


--
-- Name: barbeiro barbeiro_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.barbeiro
    ADD CONSTRAINT barbeiro_cpf_key UNIQUE (cpf);


--
-- Name: barbeiro barbeiro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.barbeiro
    ADD CONSTRAINT barbeiro_pkey PRIMARY KEY (id_barbeiro);


--
-- Name: cliente cliente_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_cpf_key UNIQUE (cpf);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cliente);


--
-- Name: horario_trabalho horario_trabalho_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario_trabalho
    ADD CONSTRAINT horario_trabalho_pkey PRIMARY KEY (id_horario);


--
-- Name: produto produto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produto
    ADD CONSTRAINT produto_pkey PRIMARY KEY (id_produto);


--
-- Name: servico servico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servico
    ADD CONSTRAINT servico_pkey PRIMARY KEY (id_servico);


--
-- Name: venda_produto venda_produto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venda_produto
    ADD CONSTRAINT venda_produto_pkey PRIMARY KEY (id_venda);


--
-- Name: idx_atendimento_agendado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_atendimento_agendado ON public.atendimento USING btree (data_agendada) WHERE (data_agendada IS NOT NULL);


--
-- Name: idx_atendimento_data; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_atendimento_data ON public.atendimento USING btree (data_atendimento);


--
-- Name: idx_barbeiro_cpf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_barbeiro_cpf ON public.barbeiro USING btree (cpf);


--
-- Name: idx_cliente_cpf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cliente_cpf ON public.cliente USING btree (cpf);


--
-- Name: atendimento atendimento_id_barbeiro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento
    ADD CONSTRAINT atendimento_id_barbeiro_fkey FOREIGN KEY (id_barbeiro) REFERENCES public.barbeiro(id_barbeiro) ON DELETE RESTRICT;


--
-- Name: atendimento atendimento_id_cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento
    ADD CONSTRAINT atendimento_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES public.cliente(id_cliente) ON DELETE RESTRICT;


--
-- Name: atendimento_servico atendimento_servico_id_atendimento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento_servico
    ADD CONSTRAINT atendimento_servico_id_atendimento_fkey FOREIGN KEY (id_atendimento) REFERENCES public.atendimento(id_atendimento) ON DELETE CASCADE;


--
-- Name: atendimento_servico atendimento_servico_id_servico_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.atendimento_servico
    ADD CONSTRAINT atendimento_servico_id_servico_fkey FOREIGN KEY (id_servico) REFERENCES public.servico(id_servico) ON DELETE RESTRICT;


--
-- Name: horario_trabalho horario_trabalho_id_barbeiro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horario_trabalho
    ADD CONSTRAINT horario_trabalho_id_barbeiro_fkey FOREIGN KEY (id_barbeiro) REFERENCES public.barbeiro(id_barbeiro) ON DELETE CASCADE;


--
-- Name: venda_produto venda_produto_id_atendimento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venda_produto
    ADD CONSTRAINT venda_produto_id_atendimento_fkey FOREIGN KEY (id_atendimento) REFERENCES public.atendimento(id_atendimento) ON DELETE CASCADE;


--
-- Name: venda_produto venda_produto_id_produto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venda_produto
    ADD CONSTRAINT venda_produto_id_produto_fkey FOREIGN KEY (id_produto) REFERENCES public.produto(id_produto) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict hA2cZzjZ7y7RMxtUIARxtlh2Vz6ArHbQOFGaucfOFO3MNNn2wNo0DLfIm7ddJd4

