USE user_accounts_schema;

-- Create a table to store user information
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Use the PASSWORD() function to hash the password
INSERT INTO users (first_name, last_name, username, password_hash)
VALUES ('John', 'Doe', 'john.doe@example.com', PASSWORD('user_password'));