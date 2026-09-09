PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS prospects (
  id TEXT PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  email_normalized TEXT NOT NULL UNIQUE,
  source TEXT NOT NULL DEFAULT 'simulation_site_orfab',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_prospects_email_normalized
ON prospects(email_normalized);

CREATE TABLE IF NOT EXISTS simulations (
  id TEXT PRIMARY KEY,
  client_submission_id TEXT NOT NULL UNIQUE,
  prospect_id TEXT NOT NULL,
  simulation_json TEXT NOT NULL,
  result_json TEXT,
  selected_optimizations_json TEXT NOT NULL DEFAULT '[]',
  estimate_label TEXT,
  page_url TEXT,
  privacy_notice_version TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  synced_at TEXT,
  FOREIGN KEY (prospect_id) REFERENCES prospects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_simulations_prospect_id
ON simulations(prospect_id);

CREATE INDEX IF NOT EXISTS idx_simulations_synced_at
ON simulations(synced_at, created_at);
