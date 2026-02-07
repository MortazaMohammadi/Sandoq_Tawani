import sqlite3

DB_FILE = "fund.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

-- 1) گروپ
CREATE TABLE IF NOT EXISTS groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  leader_member_id INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 2) عضو
CREATE TABLE IF NOT EXISTS members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id INTEGER NOT NULL,
  full_name TEXT NOT NULL,
  phone TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  joined_at TEXT NOT NULL DEFAULT (date('now')),
  UNIQUE(full_name),
  FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
);

-- 3) پول معینه ماهانه
CREATE TABLE IF NOT EXISTS monthly_fee_rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amount REAL NOT NULL CHECK(amount >= 0),
  effective_from TEXT NOT NULL,  -- YYYY-MM-DD
  note TEXT
);

-- 4) پول جمع‌آوری شده
CREATE TABLE IF NOT EXISTS collected_money (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER NOT NULL,
  period TEXT NOT NULL, -- YYYY-MM
  amount REAL NOT NULL CHECK(amount >= 0),
  collected_by_member_id INTEGER,
  note TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(member_id, period),
  FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE,
  FOREIGN KEY(collected_by_member_id) REFERENCES members(id)
);

-- 5) مصرف عمومی
CREATE TABLE IF NOT EXISTS general_expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0),
  expense_date TEXT NOT NULL DEFAULT (date('now')),
  note TEXT
);

-- 6) مصرف فوتی
CREATE TABLE IF NOT EXISTS death_expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0),
  expense_date TEXT NOT NULL DEFAULT (date('now')),
  note TEXT,
  FOREIGN KEY(member_id) REFERENCES members(id)
);

-- 7) قرضه
CREATE TABLE IF NOT EXISTS loans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER NOT NULL,
  loan_type TEXT NOT NULL,
  principal REAL NOT NULL CHECK(principal > 0),
  start_date TEXT NOT NULL DEFAULT (date('now')),
  status TEXT NOT NULL CHECK(status IN ('requested','approved','rejected','active','closed')) DEFAULT 'requested',
  note TEXT,
  FOREIGN KEY(member_id) REFERENCES members(id)
);

-- ایندکس‌ها برای سرعت
CREATE INDEX IF NOT EXISTS idx_members_group_id ON members(group_id);
CREATE INDEX IF NOT EXISTS idx_collected_member_id ON collected_money(member_id);
CREATE INDEX IF NOT EXISTS idx_collected_period ON collected_money(period);
CREATE INDEX IF NOT EXISTS idx_death_member_id ON death_expenses(member_id);
CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans(member_id);
"""

def main():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"✅ Database created/updated: {DB_FILE}")

if __name__ == "__main__":
    main()
