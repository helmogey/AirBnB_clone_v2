-- Create the database hbnb_test_db if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create or update the user hbnb_test
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the database hbnb_test_db to the user hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on the database performance_schema to the user hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
