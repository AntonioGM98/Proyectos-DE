DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS vuelos;

CREATE TABLE IF NOT EXISTS cities (
	city_code VARCHAR(3),
	airport_code VARCHAR(3),
	ctry_code VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS clients(
	name VARCHAR(50),
	surname VARCHAR(50),
	email VARCHAR(50),
	pnr VARCHAR(5),
	mkt_permission INT4
);

CREATE TABLE IF NOT EXISTS tickets(
	carrier VARCHAR(2),
	op_code INT4,
	ticket INT4,
	pnr VARCHAR(5),
	seat VARCHAR(3)
);

CREATE TABLE IF NOT EXISTS vuelos(
	carrier VARCHAR(2),
	op_code INT4,
	reg_code VARCHAR(3),
	origin VARCHAR(3),
	destination VARCHAR(3),
	flight_status VARCHAR(50),
	capacity INT4,
	departure_time VARCHAR(50),
	arrival_time VARCHAR(50),
	delayed VARCHAR(3)
);
