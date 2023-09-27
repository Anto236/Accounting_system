-- Create the 'account_system' database
CREATE DATABASE IF NOT EXISTS account_system;

-- Create the 'account_dev' user with the password 'account_pwd'
CREATE USER IF NOT EXISTS 'account_dev'@'localhost' IDENTIFIED BY 'account_pwd';

-- Grant all privileges on the 'account_system' database to the 'account_dev' user
GRANT ALL PRIVILEGES ON `account_system`.* TO 'account_dev'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
