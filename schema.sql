drop table if exists quotes;
create table quotes (
  id integer primary key autoincrement,
  title text not null,
  quote text not null,
  isbn integer not null,
  page_no integer not null
);
drop table if exists tags;
create table tags (
  quote_id integer,
  tag text not null
);