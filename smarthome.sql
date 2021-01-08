CREATE TABLE  "Δευτερεύον_προφίλ" (
	"username_de"	varchar(30) NOT NULL,
	PRIMARY KEY("username_de"),
	FOREIGN KEY("username_de") REFERENCES "Προφίλ_χρήστη"("username") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE  "Ελέγχει" (
	"command_id_ελέγχει"	integer NOT NULL,
	"device_id_ελέγχει"	varchar(30) NOT NULL,
	PRIMARY KEY("command_id_ελέγχει"),
	FOREIGN KEY("command_id_ελέγχει") REFERENCES "Εντολή"("command_id") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("device_id_ελέγχει") REFERENCES "Συσκευή"("device_id")  ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE TABLE  "Εντολή" (
	"command_id"	integer,
	"εντολή_id"	varchar(30) NOT NULL,
	PRIMARY KEY("command_id" AUTOINCREMENT)
);
CREATE TABLE  "Έχει_πρόσβαση" (
	"username_πρόσβασης"	varchar(30) NOT NULL,
	"device_id_πρόσβασης"	varchar(30) NOT NULL,
	PRIMARY KEY("username_πρόσβασης","device_id_πρόσβασης"),
	FOREIGN KEY("username_πρόσβασης") REFERENCES "Δευτερεύον_προφίλ"("username_de") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("device_id_πρόσβασης") REFERENCES "Συσκευή"("device_id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE  "Παρέχει_δικαιώματα" (
	"primary_username"	varchar(30) ,
	"secondary_username"	varchar(30) NOT NULL,
	PRIMARY KEY("primary_username","secondary_username"),
	FOREIGN KEY("primary_username") REFERENCES "Πρωτεύον_προφίλ"("username_pro") ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY("secondary_username") REFERENCES "Δευτερεύον_προφίλ"("username_de") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE  "Προφίλ_χρήστη" (
	"username"	VARCHAR(30) NOT NULL,
	"password"	varchar(30) NOT NULL,
	"alternative_password"	varchar(30),
	"δημόσιο"	boolean,
	"πολλαπλών_χρηστών"	boolean,
	PRIMARY KEY("username")
);
CREATE TABLE  "Πρωτεύον_προφίλ" (
	"username_pro"	varchar(30) NOT NULL,
	PRIMARY KEY("username_pro"),
	FOREIGN KEY("username_pro") REFERENCES "Προφίλ_χρήστη"("username") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE  "Συσκευή" (
	"device_id"	varchar(30) NOT NULL,
	"είδος"	varchar(30) NOT NULL,
	"δωμάτιο"	varchar(30) NOT NULL,
	"ενεργή"	boolean NOT NULL,
	"KWh"	real NOT NULL,
	PRIMARY KEY("device_id")
);
CREATE TABLE "Πραγματοποιεί" (
	"username_πραγματοποιεί"	varchar(30),
	"command_id_πραγματοποιεί"	int NOT NULL,
	"όνομα_συσκευής_control"	varchar(30),
	"ημερομηνία_ώρα"	datetime NOT NULL,
	"IP_Address"	varchar(15),
	PRIMARY KEY("command_id_πραγματοποιεί"),
	FOREIGN KEY("command_id_πραγματοποιεί") REFERENCES "Εντολή"("command_id") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("username_πραγματοποιεί") REFERENCES "Προφίλ_χρήστη"("username") ON DELETE SET NULL ON UPDATE CASCADE
);


