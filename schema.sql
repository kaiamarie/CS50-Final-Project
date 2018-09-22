drop table if exists user;
create table user (
    id integer primary key autoincrement,
    username text not null,
    firstname text not null,
    lastname text not null,
    email text not null,
    pw_hash text not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists student;
create table student (
    id integer primary key autoincrement,
    firstname_s text not null,
    lastname_s text not null,
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
    teacher_id integer not null,
    req_completion_count integer default 0,
    com_percent integer,
    attendance integer default 0,
    hours_purchased integer default 100,
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
    req_count integer,
    department text,
    created_at datetime,
    updated_at datetime
);

drop table if exists min_req;
create table min_req (
    id integer primary key autoincrement,
    class_id integer not null,
    req_title text not null,
    req_description text not null,
    created_at datetime,
    updated_at datetime,
    com_tmp integer
);

drop table if exists assignment;
create table assignment (
    id integer primary key autoincrement,
    min_req_id integer not null,
    assignment_name text not null,
    assignment_info text,
    student_id integer not null,
    created_at datetime,
    updated_at datetime,
    com_tmp integer
);

drop table if exists student_com_req;
create table student_com_req (
    id integer primary key autoincrement,
    min_req_id integer not null,
    student_id integer not null,
    created_at datetime,
    updated_at datetime
);

drop table if exists announcement;
create table announcement (
    id integer primary key autoincrement,
    announcement text not null,
    created_at datetime
);

drop table if exists weighting;
create table weighting (
    id integer primary key autoincrement,
    studentClass_id integer not null,
    participation integer not null default 25,
    acquisiting integer not null default 25,
    application integer not null default 25,
    retention integer not null default 25,
    created_at datetime,
    updated_at datetime
);

drop table if exists gradebook;
create table gradebook (
    id integer primary key autoincrement,
    assignment_id integer not null,
    category text not null,
    quarter integer not null,
    max_point integer not null,
    earned_point integer not null,
    created_at datetime,
    updated_at datetime
);
