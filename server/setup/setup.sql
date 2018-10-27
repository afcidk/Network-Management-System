create database NMS;
use NMS;

# table used to record traffic
create table flows (
	src VARCHAR(20),
	dst VARCHAR(20),
	len INT,
	type VARCHAR(7)
);

# table used to record agent status
create table agent (
	agent VARCHAR(20),
	time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	isup BOOLEAN
);
