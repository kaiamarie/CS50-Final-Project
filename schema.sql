drop table if exists user;
create table user (
    user_id integer primary key autoincrement,
    username text not null,
    email text not null,
    pw_hash text not null,
    created_at datetime,
    upadeted_at datetime
);
