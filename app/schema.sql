DROP TABLE IF EXISTS task;

CREATE TABLE task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);