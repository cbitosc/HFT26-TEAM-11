CREATE TABLE IF NOT EXISTS cameras (camera_id TEXT PRIMARY KEY, lat REAL, lon REAL, clock_flag INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS images (image_id TEXT PRIMARY KEY, camera_id TEXT, taken_at TEXT, seq_id TEXT, is_empty INTEGER);
CREATE TABLE IF NOT EXISTS detections (det_id INTEGER PRIMARY KEY AUTOINCREMENT, image_id TEXT, category TEXT, conf REAL, x REAL, y REAL, w REAL, h REAL);
CREATE TABLE IF NOT EXISTS sightings (sighting_id TEXT PRIMARY KEY, camera_id TEXT, start_time TEXT, end_time TEXT, species TEXT, confidence REAL, n_frames INTEGER, rep_image TEXT);
