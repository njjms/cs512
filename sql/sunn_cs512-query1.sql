-- Select from films the title and rental duration of all films with an R
-- rating and a rental cost of greater than $1 ordered by their title descending.

SELECT title, rental_duration
FROM film
WHERE rating =  'R'
AND rental_rate > 1
ORDER BY title DESC;

