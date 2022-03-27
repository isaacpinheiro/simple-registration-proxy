create database simple_registration_proxy;
use simple_registration_proxy;

create table device(
    id serial,
    dev_eui varchar(255) not null unique,
    access_token varchar(255) not null unique,
    app_id varchar(255) not null unique,
    primary key(id)
);

