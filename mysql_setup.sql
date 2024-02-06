-- preepares database for development
CREATE DATABASE IF NOT EXISTS OnlineBookStore;
CREATE USER IF NOT EXISTS 'storedbadmin'@'localhost' IDENTIFIED BY 'bookdb-pwd-8732';
GRANT ALL PRIVILEGES ON *.* TO 'storedbadmin'@'localhost';
GRANT SELECT ON `OnlineBookStore`.* TO 'storedbadmin'@'localhost';
FLUSH PRIVILEGES;
