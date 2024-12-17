use GamesVoyantDB;

CALL CreateUser(
    'alice',
    'hashedpassword1',
    'Alice',
    'Smith',
    'American',
    '1995-05-15'
);

CALL CreateUser(
    'bob',
    'hashedpassword2',
    'Bob',
    'Brown',
    'Canadian',
    '1992-11-20'
);

CALL CreateUser(
    'charlie',
    'hashedpassword3',
    'Charlie',
    'Davis',
    'British',
    '1990-03-10'
);

CALL CreateUser(
    'diana',
    'hashedpassword4',
    'Diana',
    'Evans',
    'Australian',
    '1998-09-25'
);

CALL CreateUser(
    'Lollo',
    'eheh',
    'Lorenzo Martin',
    'Diaz Avalos',
    'Peruvian',
    '2002-04-20'
);

CALL CreateUser(
    'Dan',
    'segreto',
    'Daniele',
    'Maijnelli',
    'Italian',
    '2002-04-11'
);

CALL CreateUser(
    'Ceci',
    'aiuto',
    'Cecilia',
    'Comar',
    'Italian',
    '2001-04-09'
);

CALL CreateUser(
    'Teo',
    'nonono',
    'Matteo',
    'Fumis',
    'Italian',
    '2001-12-02'
);

select * from users;