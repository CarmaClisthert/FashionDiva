DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wardrobe;
DROP TABLE IF EXISTS clothing_items;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE clothing_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    image_path TEXT NOT NULL,
    --item_type TEXT,
    --attributes TEXT,
    --embedding BLOB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
