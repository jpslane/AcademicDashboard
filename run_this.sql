USE academicworld;

ALTER TABLE keyword ADD INDEX idx_keyword_name (name);

UPDATE faculty
SET name = REGEXP_REPLACE(name, "&#;", "\'")
WHERE name REGEXP "&#;";

UPDATE faculty
SET name = REGEXP_REPLACE(name, '[0-9]', '')
WHERE name REGEXP '[0-9]';

ALTER TABLE faculty
ADD CONSTRAINT check_faculty_name
CHECK (name REGEXP '^[a-zA-Z.,\\s-()&ŠćÇçÖéŠ’ğñ\'ö;:"]*$');