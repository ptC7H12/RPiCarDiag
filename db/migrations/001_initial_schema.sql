-- Migration 001: Initial schema

CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle     TEXT NOT NULL,
    started_at  REAL NOT NULL,
    ended_at    REAL,
    frame_count INTEGER DEFAULT 0,
    notes       TEXT
);

CREATE TABLE IF NOT EXISTS can_frames (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id     INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    timestamp      REAL NOT NULL,
    arbitration_id INTEGER NOT NULL,
    dlc            INTEGER NOT NULL,
    data           BLOB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_can_frames_session ON can_frames(session_id);

CREATE TABLE IF NOT EXISTS dtcs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
    scanned_at REAL NOT NULL,
    vehicle    TEXT NOT NULL,
    ecu        TEXT,
    code       TEXT NOT NULL,
    description TEXT,
    status     TEXT NOT NULL,   -- active | stored | pending
    freeze_frame TEXT            -- JSON blob
);

CREATE TABLE IF NOT EXISTS dtc_clear_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    cleared_at REAL NOT NULL,
    vehicle    TEXT NOT NULL,
    ecu        TEXT,
    dtc_count  INTEGER
);
