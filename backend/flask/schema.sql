-- SQLite schema for starter
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'student'
);

CREATE TABLE scholarship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    eligibility TEXT,
    amount TEXT,
    status TEXT DEFAULT 'active'
);

CREATE TABLE application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    scholarship_id INTEGER NOT NULL,
    status TEXT DEFAULT 'submitted',
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    documents TEXT,
    FOREIGN KEY(student_id) REFERENCES user(id),
    FOREIGN KEY(scholarship_id) REFERENCES scholarship(id)
);

-- Example inserts (run after creating app.db if desired)
-- INSERT INTO user (name,email,password_hash,role) VALUES ('Admin','admin@example.com','<hash>','admin');
