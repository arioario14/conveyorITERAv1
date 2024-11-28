BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Conveyor" (
	"ConveyorID"	INTEGER,
	"SpeedID"	INTEGER UNIQUE,
	"TempID"	INTEGER UNIQUE,
	"Execute"	TEXT,
	PRIMARY KEY("ConveyorID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Speed" (
	"SpeedID"	INTEGER UNIQUE,
	"Direction"	TEXT,
	"Speed"	INTEGER,
	PRIMARY KEY("SpeedID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Temperature" (
	"TempID"	INTEGER,
	"MaxTemp"	INTEGER,
	"MinTemp"	INTEGER,
	PRIMARY KEY("TempID" AUTOINCREMENT)
);

INSERT INTO "Speed" ("Direction", "Speed") VALUES ('CW', 45);
INSERT INTO "Speed" ("Direction", "Speed") VALUES ('CCW', 30);

INSERT INTO "Temperature" ("MaxTemp", "MinTemp") VALUES (100, 10);
INSERT INTO "Temperature" ("MaxTemp", "MinTemp") VALUES (120, 15);

INSERT INTO "Conveyor" ("SpeedID", "TempID", "Execute") VALUES (1, 1, 'ON');
INSERT INTO "Conveyor" ("SpeedID", "TempID", "Execute") VALUES (2, 2, 'OFF');
COMMIT;
