CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    -- Otros atributos para un usuario
);

CREATE TABLE Property (
    property_id INT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(100),
    price DECIMAL(10, 2),
    description TEXT,
    -- Otros atributos de la propiedad
);

CREATE TABLE Likes (
    user_id INT,
    property_id INT,
    active BOOLEAN DEFAULT TRUE,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (property_id) REFERENCES Property(property_id),
    PRIMARY KEY (user_id, property_id)
);
