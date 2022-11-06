CREATE = """
INSERT INTO authors
       (name, image_link, birthdate, death_date) 
VALUES ($1, $2, $3, $4)
RETURNING id
"""

UPDATE = """
UPDATE authors SET
    name = CASE WHEN $2::VARCHAR IS NULL THEN name ELSE $2 END, 
    image_link = CASE WHEN $3::VARCHAR IS NULL THEN image_link ELSE $3 END, 
    birthdate = CASE WHEN $4::TIMESTAMP IS NULL THEN birthdate ELSE $4 END, 
    death_date = CASE WHEN $5::TIMESTAMP IS NULL THEN death_date ELSE $5 END
WHERE id = $1
RETURNING id
"""

DELETE = "DELETE FROM authors WHERE id = $1 RETURNING id"

GET = "SELECT * FROM authors WHERE id = $1"

LIST = "SELECT * FROM authors"
