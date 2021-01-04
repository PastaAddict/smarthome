CREATE TABLE  "deutereuon_profil" (
	"username_de"	varchar(30) NOT NULL,
	PRIMARY KEY("username_de"),
	FOREIGN KEY("username_de") REFERENCES "profil_xristi"("username") ON DELETE CASCADE
);
CREATE TABLE  "elegxei" (
	"command_id_ele"	varchar(255) NOT NULL,
	"device_id_ele"	varchar(255) NOT NULL,
	PRIMARY KEY("command_id_ele"),
	FOREIGN KEY("command_id_ele") REFERENCES "entoli"("command_id") ON DELETE CASCADE,
	FOREIGN KEY("device_id_ele") REFERENCES "syskeyi"("device_id")
);
CREATE TABLE  "entoli" (
	"command_id"	integer,
	"command"	varchar(255) NOT NULL,
	PRIMARY KEY("command_id" AUTOINCREMENT)
);
CREATE TABLE  "exei_prosvasi" (
	"username_prosvasis"	varchar(30) NOT NULL,
	"device_id"	varchar(30) NOT NULL,
	PRIMARY KEY("username_prosvasis","device_id"),
	FOREIGN KEY("username_prosvasis") REFERENCES "deutereuon_profil"("username_de") ON DELETE CASCADE,
	FOREIGN KEY("device_id") REFERENCES "syskeyi"("device_id")
);
CREATE TABLE  "parexei_dikaiwmata" (
	"primary_username"	varchar(30) NOT NULL,
	"secondary_username"	varchar(30) NOT NULL,
	PRIMARY KEY("primary_username","secondary_username"),
	FOREIGN KEY("primary_username") REFERENCES "proteuon_profil"("username_pro") ON DELETE CASCADE,
	FOREIGN KEY("secondary_username") REFERENCES "deutereuon_profil"("username_de") ON DELETE CASCADE
);
CREATE TABLE  "profil_xristi" (
	"username"	VARCHAR(30) NOT NULL,
	"kwdikos"	varchar(30) NOT NULL,
	"alternative_password"	varchar(30),
	"dimosio"	boolean,
	"pollaplwn_xriston"	boolean,
	PRIMARY KEY("username")
);
CREATE TABLE  "proteuon_profil" (
	"username_pro"	varchar(30) NOT NULL,
	PRIMARY KEY("username_pro"),
	FOREIGN KEY("username_pro") REFERENCES "profil_xristi"("username") ON DELETE CASCADE
);
CREATE TABLE  "syskeyi" (
	"device_id"	varchar(50) NOT NULL,
	"eidos"	varchar(50) NOT NULL,
	"dwmatio"	varchar(30),
	"energi"	boolean,
	"kwh"	real,
	PRIMARY KEY("device_id")
);
CREATE TABLE  "pragmatopoiei" (
	"username_pragma"	varchar(30),
	"command_id_pragma"	varchar(255) NOT NULL,
	"smart_name"	varchar(30),
	"date_time"	datetime NOT NULL,
	"IP_Address"	varchar(15),
	PRIMARY KEY("command_id_pragma"),
	FOREIGN KEY("command_id_pragma") REFERENCES "entoli"("command_id") ON DELETE CASCADE,
	FOREIGN KEY("username_pragma") REFERENCES "profil_xristi"("username") ON DELETE SET NULL
);


