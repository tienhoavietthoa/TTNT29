--
-- PostgreSQL database dump
--

\restrict pguqbaiaeuLaTxS7I32eWb4czbB1zgxibGQeDey6AtAsbsXTGn1opgKtwQKMqqY

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-04 04:40:31

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
-- TOC entry 224 (class 1259 OID 16422)
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    id_account integer NOT NULL,
    name_account character varying(100) NOT NULL,
    email_account character varying(200) NOT NULL,
    phone_account character varying(20),
    id_login integer
);


ALTER TABLE public.account OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16421)
-- Name: account_id_account_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_id_account_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_id_account_seq OWNER TO postgres;

--
-- TOC entry 5191 (class 0 OID 0)
-- Dependencies: 223
-- Name: account_id_account_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_id_account_seq OWNED BY public.account.id_account;


--
-- TOC entry 240 (class 1259 OID 16569)
-- Name: attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendance (
    id_attendance integer NOT NULL,
    id_session_attendance integer NOT NULL,
    id_student integer NOT NULL,
    id_class_attendance integer NOT NULL,
    status_attendance character varying(20) NOT NULL,
    checkin_time_attendance timestamp without time zone,
    img_filename_attendance character varying(255),
    id_embedding integer,
    notes_attendance text,
    created_at_attendance timestamp without time zone DEFAULT now()
);


ALTER TABLE public.attendance OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16568)
-- Name: attendance_id_attendance_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attendance_id_attendance_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.attendance_id_attendance_seq OWNER TO postgres;

--
-- TOC entry 5192 (class 0 OID 0)
-- Dependencies: 239
-- Name: attendance_id_attendance_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attendance_id_attendance_seq OWNED BY public.attendance.id_attendance;


--
-- TOC entry 230 (class 1259 OID 16469)
-- Name: class_admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_admin (
    id_class_admin integer NOT NULL,
    name_class_admin character varying(50) NOT NULL,
    id_faculty integer,
    id_course integer
);


ALTER TABLE public.class_admin OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16468)
-- Name: class_admin_id_class_admin_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.class_admin_id_class_admin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.class_admin_id_class_admin_seq OWNER TO postgres;

--
-- TOC entry 5193 (class 0 OID 0)
-- Dependencies: 229
-- Name: class_admin_id_class_admin_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.class_admin_id_class_admin_seq OWNED BY public.class_admin.id_class_admin;


--
-- TOC entry 234 (class 1259 OID 16507)
-- Name: class_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_attendance (
    id_class_attendance integer NOT NULL,
    code_class_attendance character varying(50) NOT NULL,
    name_class_attendance character varying(100) NOT NULL,
    id_faculty integer,
    id_course integer,
    id_account_teacher integer,
    total_students_class_attendance integer DEFAULT 0,
    status_class_attendance character varying(10) DEFAULT 'ON'::character varying,
    lesson_day_class_attendance character varying(10),
    lesson_start_hour time without time zone,
    lesson_end_hour time without time zone,
    start_date_class_attendance date,
    end_date_class_attendance date
);


ALTER TABLE public.class_attendance OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16506)
-- Name: class_attendance_id_class_attendance_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.class_attendance_id_class_attendance_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.class_attendance_id_class_attendance_seq OWNER TO postgres;

--
-- TOC entry 5194 (class 0 OID 0)
-- Dependencies: 233
-- Name: class_attendance_id_class_attendance_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.class_attendance_id_class_attendance_seq OWNED BY public.class_attendance.id_class_attendance;


--
-- TOC entry 246 (class 1259 OID 16650)
-- Name: contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contact (
    id_contact integer NOT NULL,
    sender_name_contact character varying(100) NOT NULL,
    user_type_contact character varying(20) NOT NULL,
    email_contact character varying(200) NOT NULL,
    phone_contact character varying(20),
    content_contact text NOT NULL,
    created_at_contact timestamp without time zone DEFAULT now(),
    CONSTRAINT contact_user_type_contact_check CHECK (((user_type_contact)::text = ANY ((ARRAY['teacher'::character varying, 'student'::character varying, 'other'::character varying])::text[])))
);


ALTER TABLE public.contact OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16649)
-- Name: contact_id_contact_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contact_id_contact_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contact_id_contact_seq OWNER TO postgres;

--
-- TOC entry 5195 (class 0 OID 0)
-- Dependencies: 245
-- Name: contact_id_contact_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contact_id_contact_seq OWNED BY public.contact.id_contact;


--
-- TOC entry 226 (class 1259 OID 16441)
-- Name: course; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course (
    id_course integer NOT NULL,
    start_year_course integer NOT NULL,
    end_year_course integer NOT NULL,
    name_course character varying(20) NOT NULL
);


ALTER TABLE public.course OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16440)
-- Name: course_id_course_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_id_course_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_id_course_seq OWNER TO postgres;

--
-- TOC entry 5196 (class 0 OID 0)
-- Dependencies: 225
-- Name: course_id_course_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_id_course_seq OWNED BY public.course.id_course;


--
-- TOC entry 242 (class 1259 OID 16601)
-- Name: face_embedding; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.face_embedding (
    id_embedding integer NOT NULL,
    id_student integer NOT NULL,
    id_class_attendance integer NOT NULL,
    img_filename_embedding character varying(255),
    embedding_data bytea,
    created_at_embedding timestamp without time zone DEFAULT now(),
    notes_embedding text
);


ALTER TABLE public.face_embedding OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16600)
-- Name: face_embedding_id_embedding_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.face_embedding_id_embedding_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.face_embedding_id_embedding_seq OWNER TO postgres;

--
-- TOC entry 5197 (class 0 OID 0)
-- Dependencies: 241
-- Name: face_embedding_id_embedding_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.face_embedding_id_embedding_seq OWNED BY public.face_embedding.id_embedding;


--
-- TOC entry 228 (class 1259 OID 16454)
-- Name: faculty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.faculty (
    id_faculty integer NOT NULL,
    fullname_faculty character varying(100) NOT NULL,
    shortname_faculty character varying(20) NOT NULL,
    id_course integer
);


ALTER TABLE public.faculty OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16453)
-- Name: faculty_id_faculty_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.faculty_id_faculty_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.faculty_id_faculty_seq OWNER TO postgres;

--
-- TOC entry 5198 (class 0 OID 0)
-- Dependencies: 227
-- Name: faculty_id_faculty_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.faculty_id_faculty_seq OWNED BY public.faculty.id_faculty;


--
-- TOC entry 220 (class 1259 OID 16391)
-- Name: level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.level (
    id_level integer NOT NULL,
    name_level character varying(20) NOT NULL
);


ALTER TABLE public.level OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16390)
-- Name: level_id_level_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.level_id_level_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.level_id_level_seq OWNER TO postgres;

--
-- TOC entry 5199 (class 0 OID 0)
-- Dependencies: 219
-- Name: level_id_level_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.level_id_level_seq OWNED BY public.level.id_level;


--
-- TOC entry 222 (class 1259 OID 16402)
-- Name: login; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.login (
    id_login integer NOT NULL,
    code_login character varying(50) NOT NULL,
    pass_login character varying(255) NOT NULL,
    created_at_login timestamp without time zone DEFAULT now(),
    id_level integer NOT NULL,
    status_login character varying(20) DEFAULT 'OFF'::character varying
);


ALTER TABLE public.login OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16401)
-- Name: login_id_login_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.login_id_login_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.login_id_login_seq OWNER TO postgres;

--
-- TOC entry 5200 (class 0 OID 0)
-- Dependencies: 221
-- Name: login_id_login_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.login_id_login_seq OWNED BY public.login.id_login;


--
-- TOC entry 244 (class 1259 OID 16626)
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    id_message integer NOT NULL,
    sender_id_login integer NOT NULL,
    receiver_id_login integer NOT NULL,
    content_message text NOT NULL,
    sent_at_message timestamp without time zone DEFAULT now()
);


ALTER TABLE public.message OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16625)
-- Name: message_id_message_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_message_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_id_message_seq OWNER TO postgres;

--
-- TOC entry 5201 (class 0 OID 0)
-- Dependencies: 243
-- Name: message_id_message_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_message_seq OWNED BY public.message.id_message;


--
-- TOC entry 238 (class 1259 OID 16554)
-- Name: session_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.session_attendance (
    id_session_attendance integer NOT NULL,
    id_class_attendance integer,
    session_number integer NOT NULL,
    session_date date NOT NULL,
    session_start_hour time without time zone,
    session_end_hour time without time zone,
    status_session character varying(20)
);


ALTER TABLE public.session_attendance OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16553)
-- Name: session_attendance_id_session_attendance_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.session_attendance_id_session_attendance_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.session_attendance_id_session_attendance_seq OWNER TO postgres;

--
-- TOC entry 5202 (class 0 OID 0)
-- Dependencies: 237
-- Name: session_attendance_id_session_attendance_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.session_attendance_id_session_attendance_seq OWNED BY public.session_attendance.id_session_attendance;


--
-- TOC entry 232 (class 1259 OID 16488)
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    id_student integer NOT NULL,
    code_student character varying(50) NOT NULL,
    name_student character varying(100) NOT NULL,
    email_student character varying(200),
    phone_student character varying(20),
    dob_student date,
    id_class_admin integer,
    status_student character varying(10) DEFAULT 'ON'::character varying,
    created_at_student timestamp without time zone DEFAULT now()
);


ALTER TABLE public.student OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16536)
-- Name: student_class_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_class_attendance (
    id_student_class_attendance integer NOT NULL,
    id_student integer,
    id_class_attendance integer
);


ALTER TABLE public.student_class_attendance OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16535)
-- Name: student_class_attendance_id_student_class_attendance_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_class_attendance_id_student_class_attendance_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_class_attendance_id_student_class_attendance_seq OWNER TO postgres;

--
-- TOC entry 5203 (class 0 OID 0)
-- Dependencies: 235
-- Name: student_class_attendance_id_student_class_attendance_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_class_attendance_id_student_class_attendance_seq OWNED BY public.student_class_attendance.id_student_class_attendance;


--
-- TOC entry 231 (class 1259 OID 16487)
-- Name: student_id_student_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_id_student_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_id_student_seq OWNER TO postgres;

--
-- TOC entry 5204 (class 0 OID 0)
-- Dependencies: 231
-- Name: student_id_student_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_id_student_seq OWNED BY public.student.id_student;


--
-- TOC entry 4925 (class 2604 OID 16425)
-- Name: account id_account; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account ALTER COLUMN id_account SET DEFAULT nextval('public.account_id_account_seq'::regclass);


--
-- TOC entry 4937 (class 2604 OID 16572)
-- Name: attendance id_attendance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance ALTER COLUMN id_attendance SET DEFAULT nextval('public.attendance_id_attendance_seq'::regclass);


--
-- TOC entry 4928 (class 2604 OID 16472)
-- Name: class_admin id_class_admin; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_admin ALTER COLUMN id_class_admin SET DEFAULT nextval('public.class_admin_id_class_admin_seq'::regclass);


--
-- TOC entry 4932 (class 2604 OID 16510)
-- Name: class_attendance id_class_attendance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance ALTER COLUMN id_class_attendance SET DEFAULT nextval('public.class_attendance_id_class_attendance_seq'::regclass);


--
-- TOC entry 4943 (class 2604 OID 16653)
-- Name: contact id_contact; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact ALTER COLUMN id_contact SET DEFAULT nextval('public.contact_id_contact_seq'::regclass);


--
-- TOC entry 4926 (class 2604 OID 16444)
-- Name: course id_course; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course ALTER COLUMN id_course SET DEFAULT nextval('public.course_id_course_seq'::regclass);


--
-- TOC entry 4939 (class 2604 OID 16604)
-- Name: face_embedding id_embedding; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_embedding ALTER COLUMN id_embedding SET DEFAULT nextval('public.face_embedding_id_embedding_seq'::regclass);


--
-- TOC entry 4927 (class 2604 OID 16457)
-- Name: faculty id_faculty; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faculty ALTER COLUMN id_faculty SET DEFAULT nextval('public.faculty_id_faculty_seq'::regclass);


--
-- TOC entry 4921 (class 2604 OID 16394)
-- Name: level id_level; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.level ALTER COLUMN id_level SET DEFAULT nextval('public.level_id_level_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 16405)
-- Name: login id_login; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login ALTER COLUMN id_login SET DEFAULT nextval('public.login_id_login_seq'::regclass);


--
-- TOC entry 4941 (class 2604 OID 16629)
-- Name: message id_message; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id_message SET DEFAULT nextval('public.message_id_message_seq'::regclass);


--
-- TOC entry 4936 (class 2604 OID 16557)
-- Name: session_attendance id_session_attendance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_attendance ALTER COLUMN id_session_attendance SET DEFAULT nextval('public.session_attendance_id_session_attendance_seq'::regclass);


--
-- TOC entry 4929 (class 2604 OID 16491)
-- Name: student id_student; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN id_student SET DEFAULT nextval('public.student_id_student_seq'::regclass);


--
-- TOC entry 4935 (class 2604 OID 16539)
-- Name: student_class_attendance id_student_class_attendance; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_class_attendance ALTER COLUMN id_student_class_attendance SET DEFAULT nextval('public.student_class_attendance_id_student_class_attendance_seq'::regclass);


--
-- TOC entry 5163 (class 0 OID 16422)
-- Dependencies: 224
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5179 (class 0 OID 16569)
-- Dependencies: 240
-- Data for Name: attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5169 (class 0 OID 16469)
-- Dependencies: 230
-- Data for Name: class_admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (1, 'ĐHTT01', 1, 1);
INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (2, 'ĐHTT02', 1, 1);
INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (3, 'ĐHTT03', 1, 1);
INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (4, 'ĐHTT04', 1, 1);
INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (5, 'ĐHTT05', 1, 1);
INSERT INTO public.class_admin (id_class_admin, name_class_admin, id_faculty, id_course) VALUES (6, 'ĐHTT06', 1, 1);


--
-- TOC entry 5173 (class 0 OID 16507)
-- Dependencies: 234
-- Data for Name: class_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5185 (class 0 OID 16650)
-- Dependencies: 246
-- Data for Name: contact; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5165 (class 0 OID 16441)
-- Dependencies: 226
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (1, 2020, 2024, 'K14');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (2, 2021, 2025, 'K15');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (3, 2022, 2026, 'K16');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (4, 2023, 2027, 'K17');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (5, 2024, 2028, 'K18');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (6, 2025, 2029, 'K29');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (7, 2026, 2030, 'K20');
INSERT INTO public.course (id_course, start_year_course, end_year_course, name_course) VALUES (8, 2027, 2031, 'K21');


--
-- TOC entry 5181 (class 0 OID 16601)
-- Dependencies: 242
-- Data for Name: face_embedding; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5167 (class 0 OID 16454)
-- Dependencies: 228
-- Data for Name: faculty; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.faculty (id_faculty, fullname_faculty, shortname_faculty, id_course) VALUES (1, 'Công nghệ Thông tin', 'CNTT', 1);


--
-- TOC entry 5159 (class 0 OID 16391)
-- Dependencies: 220
-- Data for Name: level; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.level (id_level, name_level) VALUES (1, 'teacher');
INSERT INTO public.level (id_level, name_level) VALUES (2, 'admin');
INSERT INTO public.level (id_level, name_level) VALUES (3, 'OFF');


--
-- TOC entry 5161 (class 0 OID 16402)
-- Dependencies: 222
-- Data for Name: login; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5183 (class 0 OID 16626)
-- Dependencies: 244
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5177 (class 0 OID 16554)
-- Dependencies: 238
-- Data for Name: session_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5171 (class 0 OID 16488)
-- Dependencies: 232
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5175 (class 0 OID 16536)
-- Dependencies: 236
-- Data for Name: student_class_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5205 (class 0 OID 0)
-- Dependencies: 223
-- Name: account_id_account_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_id_account_seq', 1, false);


--
-- TOC entry 5206 (class 0 OID 0)
-- Dependencies: 239
-- Name: attendance_id_attendance_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.attendance_id_attendance_seq', 1, false);


--
-- TOC entry 5207 (class 0 OID 0)
-- Dependencies: 229
-- Name: class_admin_id_class_admin_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.class_admin_id_class_admin_seq', 1, false);


--
-- TOC entry 5208 (class 0 OID 0)
-- Dependencies: 233
-- Name: class_attendance_id_class_attendance_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.class_attendance_id_class_attendance_seq', 1, false);


--
-- TOC entry 5209 (class 0 OID 0)
-- Dependencies: 245
-- Name: contact_id_contact_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contact_id_contact_seq', 1, false);


--
-- TOC entry 5210 (class 0 OID 0)
-- Dependencies: 225
-- Name: course_id_course_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.course_id_course_seq', 1, false);


--
-- TOC entry 5211 (class 0 OID 0)
-- Dependencies: 241
-- Name: face_embedding_id_embedding_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.face_embedding_id_embedding_seq', 1, false);


--
-- TOC entry 5212 (class 0 OID 0)
-- Dependencies: 227
-- Name: faculty_id_faculty_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.faculty_id_faculty_seq', 1, false);


--
-- TOC entry 5213 (class 0 OID 0)
-- Dependencies: 219
-- Name: level_id_level_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.level_id_level_seq', 1, false);


--
-- TOC entry 5214 (class 0 OID 0)
-- Dependencies: 221
-- Name: login_id_login_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_id_login_seq', 1, false);


--
-- TOC entry 5215 (class 0 OID 0)
-- Dependencies: 243
-- Name: message_id_message_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_message_seq', 1, false);


--
-- TOC entry 5216 (class 0 OID 0)
-- Dependencies: 237
-- Name: session_attendance_id_session_attendance_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.session_attendance_id_session_attendance_seq', 1, false);


--
-- TOC entry 5217 (class 0 OID 0)
-- Dependencies: 235
-- Name: student_class_attendance_id_student_class_attendance_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_class_attendance_id_student_class_attendance_seq', 1, false);


--
-- TOC entry 5218 (class 0 OID 0)
-- Dependencies: 231
-- Name: student_id_student_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_id_student_seq', 1, false);


--
-- TOC entry 4955 (class 2606 OID 16432)
-- Name: account account_email_account_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_email_account_key UNIQUE (email_account);


--
-- TOC entry 4957 (class 2606 OID 16434)
-- Name: account account_id_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_id_login_key UNIQUE (id_login);


--
-- TOC entry 4959 (class 2606 OID 16430)
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id_account);


--
-- TOC entry 4981 (class 2606 OID 16584)
-- Name: attendance attendance_id_session_attendance_id_student_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_id_session_attendance_id_student_key UNIQUE (id_session_attendance, id_student);


--
-- TOC entry 4983 (class 2606 OID 16582)
-- Name: attendance attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (id_attendance);


--
-- TOC entry 4967 (class 2606 OID 16476)
-- Name: class_admin class_admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_admin
    ADD CONSTRAINT class_admin_pkey PRIMARY KEY (id_class_admin);


--
-- TOC entry 4973 (class 2606 OID 16519)
-- Name: class_attendance class_attendance_code_class_attendance_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance
    ADD CONSTRAINT class_attendance_code_class_attendance_key UNIQUE (code_class_attendance);


--
-- TOC entry 4975 (class 2606 OID 16517)
-- Name: class_attendance class_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance
    ADD CONSTRAINT class_attendance_pkey PRIMARY KEY (id_class_attendance);


--
-- TOC entry 4991 (class 2606 OID 16664)
-- Name: contact contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id_contact);


--
-- TOC entry 4961 (class 2606 OID 16452)
-- Name: course course_name_course_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_name_course_key UNIQUE (name_course);


--
-- TOC entry 4963 (class 2606 OID 16450)
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (id_course);


--
-- TOC entry 4985 (class 2606 OID 16614)
-- Name: face_embedding face_embedding_id_student_id_class_attendance_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_embedding
    ADD CONSTRAINT face_embedding_id_student_id_class_attendance_key UNIQUE (id_student, id_class_attendance);


--
-- TOC entry 4987 (class 2606 OID 16612)
-- Name: face_embedding face_embedding_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_embedding
    ADD CONSTRAINT face_embedding_pkey PRIMARY KEY (id_embedding);


--
-- TOC entry 4965 (class 2606 OID 16462)
-- Name: faculty faculty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faculty
    ADD CONSTRAINT faculty_pkey PRIMARY KEY (id_faculty);


--
-- TOC entry 4947 (class 2606 OID 16400)
-- Name: level level_name_level_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.level
    ADD CONSTRAINT level_name_level_key UNIQUE (name_level);


--
-- TOC entry 4949 (class 2606 OID 16398)
-- Name: level level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.level
    ADD CONSTRAINT level_pkey PRIMARY KEY (id_level);


--
-- TOC entry 4951 (class 2606 OID 16415)
-- Name: login login_code_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_code_login_key UNIQUE (code_login);


--
-- TOC entry 4953 (class 2606 OID 16413)
-- Name: login login_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY (id_login);


--
-- TOC entry 4989 (class 2606 OID 16638)
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id_message);


--
-- TOC entry 4979 (class 2606 OID 16562)
-- Name: session_attendance session_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_attendance
    ADD CONSTRAINT session_attendance_pkey PRIMARY KEY (id_session_attendance);


--
-- TOC entry 4977 (class 2606 OID 16542)
-- Name: student_class_attendance student_class_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_class_attendance
    ADD CONSTRAINT student_class_attendance_pkey PRIMARY KEY (id_student_class_attendance);


--
-- TOC entry 4969 (class 2606 OID 16500)
-- Name: student student_code_student_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_code_student_key UNIQUE (code_student);


--
-- TOC entry 4971 (class 2606 OID 16498)
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id_student);


--
-- TOC entry 4993 (class 2606 OID 16435)
-- Name: account account_id_login_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_id_login_fkey FOREIGN KEY (id_login) REFERENCES public.login(id_login) ON DELETE CASCADE;


--
-- TOC entry 5004 (class 2606 OID 16595)
-- Name: attendance attendance_id_class_attendance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_id_class_attendance_fkey FOREIGN KEY (id_class_attendance) REFERENCES public.class_attendance(id_class_attendance);


--
-- TOC entry 5005 (class 2606 OID 16585)
-- Name: attendance attendance_id_session_attendance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_id_session_attendance_fkey FOREIGN KEY (id_session_attendance) REFERENCES public.session_attendance(id_session_attendance);


--
-- TOC entry 5006 (class 2606 OID 16590)
-- Name: attendance attendance_id_student_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance
    ADD CONSTRAINT attendance_id_student_fkey FOREIGN KEY (id_student) REFERENCES public.student(id_student);


--
-- TOC entry 4995 (class 2606 OID 16482)
-- Name: class_admin class_admin_id_course_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_admin
    ADD CONSTRAINT class_admin_id_course_fkey FOREIGN KEY (id_course) REFERENCES public.course(id_course);


--
-- TOC entry 4996 (class 2606 OID 16477)
-- Name: class_admin class_admin_id_faculty_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_admin
    ADD CONSTRAINT class_admin_id_faculty_fkey FOREIGN KEY (id_faculty) REFERENCES public.faculty(id_faculty);


--
-- TOC entry 4998 (class 2606 OID 16530)
-- Name: class_attendance class_attendance_id_account_teacher_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance
    ADD CONSTRAINT class_attendance_id_account_teacher_fkey FOREIGN KEY (id_account_teacher) REFERENCES public.account(id_account);


--
-- TOC entry 4999 (class 2606 OID 16525)
-- Name: class_attendance class_attendance_id_course_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance
    ADD CONSTRAINT class_attendance_id_course_fkey FOREIGN KEY (id_course) REFERENCES public.course(id_course);


--
-- TOC entry 5000 (class 2606 OID 16520)
-- Name: class_attendance class_attendance_id_faculty_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_attendance
    ADD CONSTRAINT class_attendance_id_faculty_fkey FOREIGN KEY (id_faculty) REFERENCES public.faculty(id_faculty);


--
-- TOC entry 5007 (class 2606 OID 16620)
-- Name: face_embedding face_embedding_id_class_attendance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_embedding
    ADD CONSTRAINT face_embedding_id_class_attendance_fkey FOREIGN KEY (id_class_attendance) REFERENCES public.class_attendance(id_class_attendance);


--
-- TOC entry 5008 (class 2606 OID 16615)
-- Name: face_embedding face_embedding_id_student_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.face_embedding
    ADD CONSTRAINT face_embedding_id_student_fkey FOREIGN KEY (id_student) REFERENCES public.student(id_student);


--
-- TOC entry 4994 (class 2606 OID 16463)
-- Name: faculty faculty_id_course_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faculty
    ADD CONSTRAINT faculty_id_course_fkey FOREIGN KEY (id_course) REFERENCES public.course(id_course);


--
-- TOC entry 4992 (class 2606 OID 16416)
-- Name: login login_id_level_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_id_level_fkey FOREIGN KEY (id_level) REFERENCES public.level(id_level);


--
-- TOC entry 5009 (class 2606 OID 16644)
-- Name: message message_receiver_id_login_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_receiver_id_login_fkey FOREIGN KEY (receiver_id_login) REFERENCES public.login(id_login);


--
-- TOC entry 5010 (class 2606 OID 16639)
-- Name: message message_sender_id_login_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_sender_id_login_fkey FOREIGN KEY (sender_id_login) REFERENCES public.login(id_login);


--
-- TOC entry 5003 (class 2606 OID 16563)
-- Name: session_attendance session_attendance_id_class_attendance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_attendance
    ADD CONSTRAINT session_attendance_id_class_attendance_fkey FOREIGN KEY (id_class_attendance) REFERENCES public.class_attendance(id_class_attendance);


--
-- TOC entry 5001 (class 2606 OID 16548)
-- Name: student_class_attendance student_class_attendance_id_class_attendance_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_class_attendance
    ADD CONSTRAINT student_class_attendance_id_class_attendance_fkey FOREIGN KEY (id_class_attendance) REFERENCES public.class_attendance(id_class_attendance);


--
-- TOC entry 5002 (class 2606 OID 16543)
-- Name: student_class_attendance student_class_attendance_id_student_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_class_attendance
    ADD CONSTRAINT student_class_attendance_id_student_fkey FOREIGN KEY (id_student) REFERENCES public.student(id_student);


--
-- TOC entry 4997 (class 2606 OID 16501)
-- Name: student student_id_class_admin_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_id_class_admin_fkey FOREIGN KEY (id_class_admin) REFERENCES public.class_admin(id_class_admin);


-- Completed on 2026-05-04 04:40:32

--
-- PostgreSQL database dump complete
--

\unrestrict pguqbaiaeuLaTxS7I32eWb4czbB1zgxibGQeDey6AtAsbsXTGn1opgKtwQKMqqY

