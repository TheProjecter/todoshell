CREATE TABLE task (id integer primary key asc,create_time,end_time,subject,comment,status,queue_id);
CREATE TABLE queue(id integer primary key asc,name);