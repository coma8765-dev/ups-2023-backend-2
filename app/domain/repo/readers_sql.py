CREATE = """
INSERT INTO readers 
       (name, email) 
VALUES ($1, $2)
RETURNING id
"""

UPDATE = """
UPDATE readers SET 
    name = CASE WHEN $2::VARCHAR IS NULL THEN name ELSE $2 END,
    email = CASE WHEN $3::VARCHAR IS NULL THEN email ELSE $3 END
WHERE id = $1
RETURNING id
"""

DELETE = "DELETE FROM readers WHERE id = $1 RETURNING id"

GET = "SELECT * FROM readers WHERE id = $1"

LIST = "SELECT * FROM readers"
