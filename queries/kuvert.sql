-- :name fetch_open_kuvert :many
SELECT * FROM kuvert WHERE opening_date <= date('now');

-- :name fetch_recent_open_kuvert :many
SELECT * FROM kuvert WHERE opening_date <= date('now') ORDER BY opening_date DESC LIMIT 5;

-- :name fetch_open_kuvert_by_id :one
SELECT * FROM kuvert WHERE id = :id AND opening_date <= date('now');

-- :name fetch_kuvert_by_id :one
SELECT title, created_at, tag, opening_date from kuvert WHERE id = :id;

-- :name fetch_open_tag_kuvert :many
SELECT * FROM kuvert WHERE opening_date <= date('now') AND tag = :tag;

-- :name store_kuvert :insert
INSERT INTO kuvert (content, opening_date, tag, title) VALUES (:content, :opening_date, :tag, :title) RETURNING id;

-- :name fetch_all_kuvert :many
SELECT * FROM kuvert;

-- :name force_fetch_kuvert :one
SELECT * FROM kuvert WHERE id = :id;
