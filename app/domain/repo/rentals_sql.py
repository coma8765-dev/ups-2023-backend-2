CREATE = """
INSERT INTO rentals 
       (book_id, reader_id, fine_amount) 
VALUES ($1, $2, $3)
RETURNING id
"""

UPDATE = """
UPDATE rentals SET 
    "end" = CASE WHEN $2::TIMESTAMP IS NULL THEN "end" ELSE $2 END
WHERE id = $1
RETURNING id
"""

GET_BY_BOOK_AND_READER = """
SELECT * 
FROM rentals 
WHERE reader_id = $1 AND book_id = $2
"""

LIST = """
SELECT *, 
       (SELECT rental_limit 
        FROM books b 
        WHERE b.id = r.book_id) AS rental_limit
FROM rentals r
WHERE CASE WHEN $1::INTEGER IS NULL THEN TRUE ELSE book_id = $1 END 
  AND CASE WHEN $2::INTEGER IS NULL THEN TRUE ELSE reader_id = $2 END 
  AND CASE WHEN $3::BOOLEAN IS NULL THEN TRUE 
           ELSE CASE WHEN $3 THEN "end" IS NOT NULL ELSE "end" IS NULL END END
"""
