--
-- ER/Studio 8.0 SQL Code Generation
-- Company :      yolo
-- Project :      Modelo Relacional.DM1
-- Author :       somexav
--
-- Date Created : Saturday, April 30, 2022 18:40:30
-- Target DBMS : MySQL 5.x
--

-- 
-- TABLE: ASENTAMIENTO 
--

CREATE TABLE ASENTAMIENTO(
    C_TIPO_ASENTAMIENTO    DECIMAL(2, 0)    NOT NULL,
    D_TIPO_ASENTAMIENTO    VARCHAR(20)      NOT NULL,
    PRIMARY KEY (C_TIPO_ASENTAMIENTO)
)ENGINE=MYISAM
;



-- 
-- TABLE: CIUDAD 
--

CREATE TABLE CIUDAD(
    C_CVE_CIUDAD    DECIMAL(3, 0)    NOT NULL,
    D_CIUDAD        VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_CVE_CIUDAD)
)ENGINE=MYISAM
;



-- 
-- TABLE: ESTADO 
--

CREATE TABLE ESTADO(
    C_ESATDO    DECIMAL(2, 0)    NOT NULL,
    D_ESTADO    VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_ESATDO)
)ENGINE=MYISAM
;



-- 
-- TABLE: MUNICIPIO 
--

CREATE TABLE MUNICIPIO(
    C_MUNICIPIO    DECIMAL(3, 0)    NOT NULL,
    D_MUNICIPIO    VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_MUNICIPIO)
)ENGINE=MYISAM
;



-- 
-- TABLE: SEPOMEX 
--

CREATE TABLE SEPOMEX(
    SEPOMEX_ID             DECIMAL(10, 0)    NOT NULL,
    D_CODIGO               DECIMAL(7, 0)     NOT NULL,
    D_ASENTA               VARCHAR(20)       NOT NULL,
    D_CP                   DECIMAL(5, 0)     NOT NULL,
    ID_ASENTA_CPCONS       DECIMAL(5, 0)     NOT NULL,
    D_ZONA                 BIT(1)            NOT NULL,
    C_ESATDO               DECIMAL(2, 0)     NOT NULL,
    C_MUNICIPIO            DECIMAL(3, 0)     NOT NULL,
    C_CVE_CIUDAD           DECIMAL(3, 0),
    C_TIPO_ASENTAMIENTO    DECIMAL(2, 0)     NOT NULL,
    PRIMARY KEY (SEPOMEX_ID), 
    CONSTRAINT RefESTADO5 FOREIGN KEY (C_ESATDO)
    REFERENCES ESTADO(C_ESATDO),
    CONSTRAINT RefMUNICIPIO6 FOREIGN KEY (C_MUNICIPIO)
    REFERENCES MUNICIPIO(C_MUNICIPIO),
    CONSTRAINT RefCIUDAD7 FOREIGN KEY (C_CVE_CIUDAD)
    REFERENCES CIUDAD(C_CVE_CIUDAD),
    CONSTRAINT RefASENTAMIENTO8 FOREIGN KEY (C_TIPO_ASENTAMIENTO)
    REFERENCES ASENTAMIENTO(C_TIPO_ASENTAMIENTO)
)ENGINE=MYISAM
;



