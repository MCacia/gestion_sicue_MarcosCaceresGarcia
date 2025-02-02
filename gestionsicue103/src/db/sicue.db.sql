BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "planes_convalidacion" (
	"id"	INTEGER,
	"universidad_origen"	TEXT,
	"universidad_destino"	TEXT,
	"duracion"	TEXT,
	"asignaturas"	TEXT,
	"asignaturas_convalidadas"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "estudiantes" (
	"nombre"	TEXT,
	"curso"	INTEGER,
	"dni"	TEXT,
	PRIMARY KEY("dni")
);
CREATE TABLE IF NOT EXISTS "profesores" (
	"DNI"	TEXT,
	"nombre"	TEXT,
	"correo"	TEXT,
	"grado"	TEXT,
	PRIMARY KEY("DNI")
);
CREATE TABLE IF NOT EXISTS "inscripciones_profesores" (
	"id"	INTEGER,
	"dni"	TEXT,
	"grado"	TEXT,
	"asignatura"	TEXT,
	"duracion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "grados" (
	"id"	INTEGER,
	"nombre"	TEXT,
	"asignaturas"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "inscripciones" (
	"id"	INTEGER,
	"estudiante_id"	INTEGER,
	"plan_id"	INTEGER,
	"fecha_inscripcion"	TEXT,
	"estado"	TEXT,
	FOREIGN KEY("plan_id") REFERENCES "planes_convalidacion"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "planes_convalidacion" VALUES (4,'Cordoba','Madrid','4','fisica,calculo','fisica,calculo');
INSERT INTO "planes_convalidacion" VALUES (5,'Sevilla','Madrid','12','Física,Cálculo,Programación','Empresas');
INSERT INTO "planes_convalidacion" VALUES (6,'Cordoba','Bilbao','10','Fisica','Calculo');
INSERT INTO "estudiantes" VALUES ('Marcos','2º','12345678A');
INSERT INTO "estudiantes" VALUES ('Pablo','3º','12345678T');
INSERT INTO "estudiantes" VALUES ('Marcos','1º','12345678X');
INSERT INTO "estudiantes" VALUES ('Marcos','1º','12345678K');
INSERT INTO "estudiantes" VALUES ('Marcos','2º','12345678J');
INSERT INTO "estudiantes" VALUES ('Marcos','1º','12345678N');
INSERT INTO "estudiantes" VALUES ('Marcos','1º','12345678V');
INSERT INTO "estudiantes" VALUES ('Pablo','1º','46273854Q');
INSERT INTO "estudiantes" VALUES ('Luis','1º','87654321Q');
INSERT INTO "estudiantes" VALUES ('Luis','2º','46273854A');
INSERT INTO "estudiantes" VALUES ('Carlos','2º','12345678B');
INSERT INTO "estudiantes" VALUES ('Marcos','2º','12345678F');
INSERT INTO "estudiantes" VALUES ('Pablo','2º','46273854C');
INSERT INTO "estudiantes" VALUES ('','','');
INSERT INTO "profesores" VALUES ('12345678R','David','i42david@uco.es','Informatica');
INSERT INTO "profesores" VALUES ('','','','');
INSERT INTO "profesores" VALUES ('46273854Q','Pablo','pablo@uco.es','Informática');
INSERT INTO "inscripciones_profesores" VALUES (8,'12345678R','Informatica','Fisica','Cuatrimestre');
INSERT INTO "grados" VALUES (1,'Informatica','Fisica,Estadistica');
INSERT INTO "inscripciones" VALUES (6,'12345678A',4,'2024-11-28',NULL);
INSERT INTO "inscripciones" VALUES (8,'12345678T',4,'2024-11-28',NULL);
INSERT INTO "inscripciones" VALUES (11,'12345678J',4,'2024-11-28 12:30:23',NULL);
INSERT INTO "inscripciones" VALUES (14,'12345678N',4,'2024-11-28 12:44:10',NULL);
INSERT INTO "inscripciones" VALUES (16,'87654321Q',5,'2024-12-18 17:10:56',NULL);
INSERT INTO "inscripciones" VALUES (17,'46273854A',6,'2024-12-18 17:31:25',NULL);
INSERT INTO "inscripciones" VALUES (18,'12345678B',6,'2024-12-19 10:41:19',NULL);
COMMIT;
