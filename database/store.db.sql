BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"image"	BLOB,
	"name"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"contact_num"	TEXT,
	"address"	TEXT,
	"role"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "client" (
	"id"	INTEGER,
	"image"	BLOB,
	"name"	TEXT NOT NULL,
	"lastname"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"phone"	TEXT,
	"address"	TEXT,
	"type_client"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "provider" (
	"id"	INTEGER,
	"image"	BLOB,
	"rut"	TEXT,
	"name"	TEXT,
	"email"	TEXT,
	"phone"	TEXT,
	"address"	TEXT,
	"type"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice" (
	"id"	INTEGER,
	"client_id"	INTEGER NOT NULL,
	"sent_id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"date"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"description"	TEXT,
	"total"	REAL NOT NULL,
	"code"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("client_id") REFERENCES "client"("id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE,
	FOREIGN KEY("sent_id") REFERENCES "sent"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "invoice_item" (
	"id"	INTEGER,
	"invoice_id"	INTEGER NOT NULL,
	"inventory_id"	INTEGER,
	"quantity"	INTEGER NOT NULL,
	"total_price"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "project" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"budget"	REAL NOT NULL,
	"status"	TEXT NOT NULL,
	"type_project"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "task" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"name"	TEXT,
	"description"	TEXT,
	"status"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "business_goals" (
	"id"	INTEGER,
	"business_id"	INTEGER,
	"name"	TEXT,
	"description"	TEXT,
	"status"	TEXT,
	"start_date"	DATE,
	"end_date"	DATE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("business_id") REFERENCES "business"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "inventory" (
	"id"	INTEGER,
	"image"	BLOB,
	"name"	TEXT,
	"category"	TEXT,
	"stock"	INTEGER,
	"purchase_price"	REAL,
	"sale_price"	REAL,
	"totalpurch"	REAL,
	"description"	TEXT,
	"type_product"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "investment" (
	"id"	INTEGER,
	"type"	TEXT,
	"date"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"amount"	REAL,
	"amount_end"	REAL,
	"yield"	TEXT,
	"expiration_date"	date,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sent_invoice" (
	"id"	INTEGER,
	"sent_id"	INTEGER,
	"invoice_id"	INTEGER,
	"quantity"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("sent_id") REFERENCES "sent"("id") ON DELETE CASCADE,
	FOREIGN KEY("invoice_id") REFERENCES "invoice"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "sent" (
	"id"	INTEGER,
	"address_id"	INTEGER,
	"method"	TEXT,
	"description"	TEXT,
	"price"	REAL,
	"status"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("address_id") REFERENCES "address"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "address" (
	"id"	INTEGER,
	"country"	TEXT,
	"region"	TEXT,
	"commune"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "coordinate" (
	"id"	INTEGER,
	"address_id"	INTEGER,
	"uuid"	TEXT,
	"lat"	REAL,
	"lon"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("address_id") REFERENCES "address"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "transactions" (
	"id"	INTEGER,
	"transaction_id"	INTEGER,
	"transaction_date"	DATE DEFAULT (DATE('now')),
	"amount"	REAL,
	"transaction_type"	TEXT,
	"entity"	TEXT,
	"payment_type"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "business" (
	"id"	INTEGER,
	"address_id"	INTEGER,
	"name"	TEXT,
	"image"	BLOB,
	"legal_form"	TEXT,
	"industry"	TEXT,
	"registration_number"	TEXT,
	"founding_date"	DATE,
	"gain"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("address_id") REFERENCES "address"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "employee" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"job"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "calendar" (
	"id"	INTEGER,
	"employee_id"	INTEGER,
	"start_time"	time,
	"end_time"	time,
	"horary"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("employee_id") REFERENCES "employee"("id") ON DELETE CASCADE
);
COMMIT;
