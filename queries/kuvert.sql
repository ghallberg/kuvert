-- :name fetch_open_kuvert :many
SELECT * FROM kuvert WHERE opening_date <= date('now')

-- :name fetch_kuvert :one
SELECT * FROM kuvert WHERE id = :id AND opening_date <= date('now')

-- :name fetch_open_user_kuvert :many
SELECT * FROM kuvert WHERE opening_date <= date('now') AND owner = :owner

-- :name store_kuvert :insert
INSERT INTO kuvert (content, opening_date, owner) VALUES (:content, :opening_date, :owner)
