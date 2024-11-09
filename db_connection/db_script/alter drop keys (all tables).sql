-- State table'dan primary key kald?rma
ALTER TABLE state_table
DROP CONSTRAINT PK_state_table;

-- City table'dan primary key kald?rma
ALTER TABLE city_table
DROP CONSTRAINT PK__city_tab__031385F023909FFF;

-- ZIP code table'dan primary key ve foreign keyleri kald?rma
ALTER TABLE ZIP_code_table
DROP CONSTRAINT PK__ZIP_code__7927D44911E121E3;

ALTER TABLE ZIP_code_table
DROP CONSTRAINT FK__ZIP_code___city___3B75D760;

ALTER TABLE ZIP_code_table
DROP CONSTRAINT FK__ZIP_code___state__3C69FB99;

-- Advertisement table'dan primary key ve foreign key kald?rma
ALTER TABLE ad_table
DROP CONSTRAINT FK__ad_table__ZIP_co__45F365D3;

ALTER TABLE ad_table
DROP CONSTRAINT FK__ad_table__ZIP_co__45F365D3;
