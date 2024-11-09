-- State table'a primary key ekle
ALTER TABLE state_table
ADD CONSTRAINT PK_state_table PRIMARY KEY (state_id);

-- City table'a primary key ekle
ALTER TABLE city_table
ADD CONSTRAINT PK_city_table PRIMARY KEY (city_ID);

-- ZIP code table'a primary key ve foreign key ekle
ALTER TABLE ZIP_code_table
ADD CONSTRAINT PK_ZIP_code_table PRIMARY KEY (ZIP_code);

ALTER TABLE ZIP_code_table
ADD CONSTRAINT FK_ZIP_code_city_ID FOREIGN KEY (city_ID) REFERENCES city_table(city_ID);

-- Advertisement table'a primary key ve foreign key ekle
ALTER TABLE ad_table
ADD CONSTRAINT PK_ad_table PRIMARY KEY (AD_ID);

ALTER TABLE ad_table
ADD CONSTRAINT FK_ad_table_ZIP_code FOREIGN KEY (ZIP_code) REFERENCES ZIP_code_table(ZIP_code);
