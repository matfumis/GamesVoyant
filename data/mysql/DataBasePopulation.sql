USE GamesVoyantDB;

CALL CreateUser(
        'alice',
        '$2b$12$uX0y.NjI9Wxg8XXu4wY.V.kLEH1Bqqfo5bbf1n26pD0vY5TGe9V6e',  -- bcrypt hash for 'hashedpassword1'
        'Alice',
        'Smith',
        'American',
        '1995-05-15'
     );

CALL CreateUser(
        'bob',
        '$2b$12$X0y.Zx9JSsJlZov9/jOFSCHTZpl5n3TejpfC1ggvINbH4MnFeP3Jm',  -- bcrypt hash for 'hashedpassword2'
        'Bob',
        'Brown',
        'Canadian',
        '1992-11-20'
     );

CALL CreateUser(
        'charlie',
        '$2b$12$KjX1zdo8xW0GnqA3ZVvL6dVpvn5z3Qbgt7t7qjK31TwI8fpzO7vu',  -- bcrypt hash for 'hashedpassword3'
        'Charlie',
        'Davis',
        'British',
        '1990-03-10'
     );

CALL CreateUser(
        'diana',
        '$2b$12$8f9h.6aYq9WqAKYGV8mhLO9itCmTQ4bCoVsVeVq7fqS/q68U/fiSa',  -- bcrypt hash for 'hashedpassword4'
        'Diana',
        'Evans',
        'Australian',
        '1998-09-25'
     );

CALL CreateUser(
        'Lollo',
        '$2b$12$1gZQxg4lLm9/Z8IqZo4TRGHrk5KN1lwAKDbe5PT76zyI8mm2XsP7a',  -- bcrypt hash for 'eheh'
        'Lorenzo Martin',
        'Diaz Avalos',
        'Peruvian',
        '2002-04-20'
     );

CALL CreateUser(
        'Dan',
        '$2b$12$CZcU5vM1W06ya.qJgZzHTQS2bsJ0DbhpfVuY91JH8X8bxQ0wQDAUa',  -- bcrypt hash for 'segreto'
        'Daniele',
        'Maijnelli',
        'Italian',
        '2002-04-11'
     );

CALL CreateUser(
        'Ceci',
        '$2b$12$4lOS0pYPsg.Yy3Y9LrUp9u2GTiFkaVoDeA2eRurFFYZZROo5A2Ge2',  -- bcrypt hash for 'aiuto'
        'Cecilia',
        'Comar',
        'Italian',
        '2001-04-09'
     );

CALL CreateUser(
        'Teo',
        '$2b$12$7BdFc7dVwCgIom0sZgHg7o3lNOwI4tX/jzB3MqqswkIzDPs7Jf2ja',  -- bcrypt hash for 'nonono'
        'Matteo',
        'Fumis',
        'Italian',
        '2001-12-02'
     );

SELECT * FROM users;
