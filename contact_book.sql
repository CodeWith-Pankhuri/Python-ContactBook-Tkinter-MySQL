CREATE DATABASE IF NOT EXISTS contact_db;

USE contact_db;

CREATE TABLE IF NOT EXISTS contacts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      phone Varchar(20) UNIQUE NOT NULL,
 	  email VARCHAR(100) UNIQUE,
      address TEXT
  );


