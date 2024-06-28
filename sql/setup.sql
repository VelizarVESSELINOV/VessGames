CREATE DATABASE vgame_store;
CREATE USER app_service WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE vgame_store TO app_service;
