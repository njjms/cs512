-- Delete all rows from bsg_people where the person has no homeword

DELETE FROM bsg_people
WHERE homeworld IS NULL

