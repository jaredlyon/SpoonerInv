CREATE TABLE IF NOT EXISTS mytable(
   region_id INTEGER  NOT NULL PRIMARY KEY 
  ,name      VARCHAR(20) NOT NULL
  ,manager   INTEGER  NOT NULL
);
INSERT INTO mytable(region_id,name,manager) VALUES (1,'Colorado',49);
INSERT INTO mytable(region_id,name,manager) VALUES (2,'District of Columbia',48);
INSERT INTO mytable(region_id,name,manager) VALUES (3,'California',93);
INSERT INTO mytable(region_id,name,manager) VALUES (4,'California',92);
INSERT INTO mytable(region_id,name,manager) VALUES (5,'Oklahoma',43);
