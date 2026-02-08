import sqlite3

DB_FILE = "fund.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

-- 1) گروپ
CREATE TABLE IF NOT EXISTS groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  leader_member_id INTEGER,
  created_at TEXT NOT NULL
);

-- 2) عضو
CREATE TABLE IF NOT EXISTS members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id INTEGER NOT NULL,
  full_name TEXT NOT NULL,
  phone TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  joined_at TEXT NOT NULL,
  UNIQUE(full_name),
  FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
);

-- ایندکس‌ها برای سرعت
CREATE INDEX IF NOT EXISTS idx_members_group_id ON members(group_id);
"""

def main():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"✅ Database created/updated: {DB_FILE}")

if __name__ == "__main__":
    main()
