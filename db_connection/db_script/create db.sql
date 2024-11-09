-- Veritabanını oluştur
CREATE DATABASE immo_welt;
GO

-- Yeni veritabanını kullan
USE immo_welt;
GO

-- State table
CREATE TABLE state_table (
    state_id INT PRIMARY KEY,
    state_name VARCHAR(255) NOT NULL
);

-- City table
CREATE TABLE city_table (
    city_ID INT PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL,
	city_population INT
);

-- ZIP code table
CREATE TABLE ZIP_code_table (
    ZIP_code INT PRIMARY KEY,
    city_ID INT NOT NULL,
    url VARCHAR(500),
    FOREIGN KEY (city_ID) REFERENCES city_table(city_ID)
);

-- Advertisement table
CREATE TABLE ad_table (
    AD_ID INT PRIMARY KEY,
    ZIP_code INT NOT NULL,
    price DECIMAL(10, 2),
    number_of_room INT,
    house_size DECIMAL(10, 2),
    property_size DECIMAL(10, 2),
    City_score DECIMAL(5, 2),
    geo_score DECIMAL(5, 2),
    ad_URL VARCHAR(500),
    FOREIGN KEY (ZIP_code) REFERENCES ZIP_code_table(ZIP_code)
);
