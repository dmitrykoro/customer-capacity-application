DROP TABLE IF EXISTS facility CASCADE;
DROP TABLE IF EXISTS account CASCADE;
DROP TABLE IF EXISTS customer_visit CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;


CREATE TABLE facility(
    uuid VARCHAR PRIMARY KEY,
    name VARCHAR(64),
    city VARCHAR(64),
    max_capacity INT,
    notes VARCHAR(64),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE account(
    uuid VARCHAR PRIMARY KEY,
    name VARCHAR(64),
    role VARCHAR(64),
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(512) DEFAULT NULL,
    facility_id VARCHAR REFERENCES facility(uuid) ON DELETE CASCADE,
    session_key VARCHAR(64) DEFAULT NULL,
    session_expires_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE customer_visit(
    uuid VARCHAR PRIMARY KEY,
    name VARCHAR(64),
    document_id VARCHAR(64),
    age INT,
    facility_id VARCHAR REFERENCES facility(uuid),
    checked_in_at TIMESTAMP DEFAULT now(),
    checked_out_at TIMESTAMP DEFAULT NULL,
    charge FLOAT DEFAULT NULL
);

CREATE TABLE notifications(
    uuid VARCHAR PRIMARY KEY,
    facility_id VARCHAR REFERENCES facility(uuid),
    age INT,
    phone VARCHAR(64)
);
