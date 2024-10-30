CREATE DATABASE IF NOT EXISTS predictions_db;

USE predictions_db;

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    features TEXT,
    prediction INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
