-- Select the first name, last name and film title of all films an actor with the last name Cage acted in.
-- Order by the film title, descending. There should be one row for every actor/film pair.

SELECT first_name, last_name, title
FROM actor
INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id -- join film_actor to get film_id
INNER JOIN film ON film_actor.film_id = film.film_id -- join film on film_id to get title
WHERE last_name LIKE'%Cage%'
ORDER BY title DESC 


