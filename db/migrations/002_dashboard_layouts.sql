-- Migration 002: Dashboard layouts

CREATE TABLE IF NOT EXISTS dashboard_layouts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle      TEXT NOT NULL,
    signal_id    TEXT NOT NULL,
    display_type TEXT NOT NULL,   -- gauge | bar | value
    grid_row     INTEGER NOT NULL,
    grid_col     INTEGER NOT NULL,
    config       TEXT             -- JSON blob for display-specific settings
);

CREATE TABLE IF NOT EXISTS coding_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    written_at REAL NOT NULL,
    vehicle    TEXT NOT NULL,
    ecu        TEXT NOT NULL,
    coding_id  TEXT NOT NULL,
    old_value  TEXT,
    new_value  TEXT NOT NULL,
    backup_raw BLOB             -- raw ECU response before write
);
