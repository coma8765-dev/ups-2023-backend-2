CREATE = """
INSERT INTO books 
       (title, rental_limit, image_link, author_id) 
VALUES ($1, $2, $3, $4)
RETURNING id
"""

UPDATE = """
UPDATE books SET 
    title = CASE WHEN $2::VARCHAR IS NULL THEN title ELSE $2 END,
    rental_limit = CASE WHEN $3::INTERVAL IS NULL 
                   THEN rental_limit ELSE $3 END,
    image_link = CASE WHEN $4::VARCHAR IS NULL 
                 THEN image_link ELSE $4 END,
    author_id = CASE WHEN $5::INTEGER IS NULL THEN author_id ELSE $5 END
WHERE id = $1
RETURNING id
"""

DELETE = "DELETE FROM books WHERE id = $1 RETURNING id"

GET = """
SELECT *,
       EXISTS (SELECT id 
               FROM rentals 
               WHERE book_id = b.id AND "end" IS NULL) AS is_busy
FROM books b
WHERE id = $1
"""

LIST = """
SELECT b.*,
       EXISTS (SELECT id 
        FROM rentals 
        WHERE book_id = b.id AND "end" IS NOT NULL) AS is_busy
FROM books b
WHERE CASE WHEN $1::INTEGER IS NULL THEN TRUE ELSE author_id = $1 END 
  AND CASE WHEN $2::VARCHAR IS NULL THEN TRUE 
           ELSE LOWER (title) LIKE CONCAT('%', LOWER ($2), '%') END 
  AND CASE WHEN $3::BOOLEAN IS NULL THEN TRUE 
           ELSE NOT EXISTS (SELECT id 
                            FROM rentals 
                            WHERE book_id = b.id) END 
"""
