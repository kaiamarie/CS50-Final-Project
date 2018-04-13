drop table if exists user;
create table user (
    id integer primary key autoincrement,
    username text not null,
    email text not null,
    pw_hash text not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists student;
create table student (
    id integer primary key autoincrement,
    firstname text not null,
    lastname text not null,
    grade integer,
    enrollment_date date,
    created_at datetime,
    updated_at datetime
);

drop table if exists studentClass;
create table studentClass (
    id integer primary key autoincrement,
    student_id integer not null,
    class_id integer not null,
    hours_purchased integer,
    start_date date,
    end_date date,
    created_at datetime,
    updated_at datetime
);

drop table if exists adviser;
create table adviser (
    id integer primary key autoincrement,
    user_id integer not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists teacher;
create table teacher (
    id integer primary key autoincrement,
    user_id integer not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists class;
create table class (
    id integer primary key autoincrement,
    class_title text not null,
    credits number,
    created_at datetime,
    updated_at datetime
);

drop table if exists min_req;
create table min_req (
    id integer primary key autoincrement,
    class_id integer not null,
    requirement text not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists assignment;
create table assignment (
    id integer primary key autoincrement,
    min_req_id integer not null,
    assinment_name text not null,
    created_at datetime,
    updated_at datetime
);
