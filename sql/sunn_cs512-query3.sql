-- From films, select the average replacement cost and rating of all the films with that rating.
-- The first column should be the average and it should be named 'avg_cost' the second column should be the rating
-- Order by the average cost descending.

SELECT AVG(replacement_cost) as avg_cost, rating
from film
GROUP BY rating
ORDER BY avg_cost DESC;