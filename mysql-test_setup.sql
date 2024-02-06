-- preepares database for development
CREATE DATABASE IF NOT EXISTS OnlineBookStoretest;
CREATE USER IF NOT EXISTS 'storedbadmintest'@'localhost' IDENTIFIED BY 'bookdb-test-pwd-8732';
GRANT ALL PRIVILEGES ON `OnlineBookStoretest`.* TO 'storedbadmintest'@'localhost';
GRANT SELECT ON `OnlineBookStoretest`.* TO 'storedbadmintest'@'localhost';
FLUSH PRIVILEGES;
