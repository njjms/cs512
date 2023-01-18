-- Update the bsg_people table. Set anyone named Gaius Baltar to be from Caprica. This should use a subquery.

UPDATE bsg_people
SET homeworld = (SELECT id FROM bsg_planets WHERE name = 'Caprica')
WHERE fname = 'Gaius' AND lname = 'Baltar'

