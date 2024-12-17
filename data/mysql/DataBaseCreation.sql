CREATE DATABASE IF NOT EXISTS GamesVoyantDB;

USE GamesVoyantDB;


CREATE TABLE Users
(
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(20)  NOT NULL UNIQUE,
    name           VARCHAR(20)  NOT NULL,
    surname        VARCHAR(20)  NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    nationality    VARCHAR(30)  NOT NULL,
    date_of_birth  DATE         NOT NULL,
    friends        JSON,
    saved_games    JSON,
    games_liked    JSON,
    games_disliked JSON
);

DELIMITER $$

CREATE PROCEDURE CreateUser(
    IN p_username VARCHAR(20),
    IN p_password_hash VARCHAR(255),
    IN p_name VARCHAR(20),
    IN p_surname VARCHAR(20),
    IN p_nationality VARCHAR(30),
    IN p_date_of_birth DATE
)
BEGIN
    INSERT INTO Users (username,
                       password_hash,
                       name,
                       surname,
                       nationality,
                       date_of_birth,
                       friends,
                       saved_games,
                       games_liked,
                       games_disliked)
    VALUES (p_username,
            p_password_hash,
            p_name,
            p_surname,
            p_nationality,
            p_date_of_birth,
            '[]', '[]', '[]', '[]');
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE DeleteUser(
    IN p_user_id INT
)
BEGIN
    DELETE FROM Users WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE ModifyUsername(
    IN p_user_id INT,
    IN p_new_username VARCHAR(20)
)
BEGIN
    UPDATE Users
    SET username = p_new_username
    WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddFriend(
    IN p_user_id INT,
    IN p_friend_id INT
)
BEGIN
    SET @new_friends = JSON_ARRAY_APPEND(
            (SELECT friends FROM Users WHERE user_id = p_user_id),
            '$',
            p_friend_id
        );
    UPDATE Users
    SET friends = @new_friends
    WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE RemoveFriend(
    IN p_user_id INT,
    IN p_friend_id INT
)
BEGIN
    SET @friend_index = JSON_UNQUOTE(
            JSON_SEARCH(
                    (SELECT friends FROM Users WHERE user_id = p_user_id),
                    'one',
                    p_friend_id
                )
        );

    IF @friend_index IS NOT NULL THEN
        SET @updated_friends = JSON_REMOVE(
                (SELECT friends FROM Users WHERE user_id = p_user_id),
                @friend_index
            );
        UPDATE Users
        SET friends = @updated_friends
        WHERE user_id = p_user_id;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddLikedGame(
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @updated_games_liked = JSON_ARRAY_APPEND(
            (SELECT games_liked FROM Users WHERE user_id = p_user_id),
            '$',
            p_game_id
        );
    UPDATE Users
    SET games_liked = @updated_games_liked
    WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE RemoveLikedGame (
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @game_index = JSON_UNQUOTE(
        JSON_SEARCH(
            (SELECT games_liked FROM Users WHERE user_id = p_user_id),
            'one',
            p_game_id
        )
    );

    IF @game_index IS NOT NULL THEN
        SET @updated_games_liked = JSON_REMOVE(
            (SELECT games_liked FROM Users WHERE user_id = p_user_id),
            @game_index
        );
        UPDATE Users
        SET games_liked = @updated_games_liked
        WHERE user_id = p_user_id;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddDislikedGame(
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @updated_games_liked = JSON_ARRAY_APPEND(
            (SELECT games_disliked FROM Users WHERE user_id = p_user_id),
            '$',
            p_game_id
        );
    UPDATE Users
    SET games_disliked = @updated_games_liked
    WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE RemoveDislikedGame (
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @game_index = JSON_UNQUOTE(
        JSON_SEARCH(
            (SELECT games_disliked FROM Users WHERE user_id = p_user_id),
            'one',
            p_game_id
        )
    );

    IF @game_index IS NOT NULL THEN
        SET @updated_games_liked = JSON_REMOVE(
            (SELECT games_disliked FROM Users WHERE user_id = p_user_id),
            @game_index
        );
        UPDATE Users
        SET games_disliked = @updated_games_liked
        WHERE user_id = p_user_id;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddSavedGame(
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @updated_games_liked = JSON_ARRAY_APPEND(
            (SELECT saved_games FROM Users WHERE user_id = p_user_id),
            '$',
            p_game_id
        );
    UPDATE Users
    SET saved_games = @updated_games_liked
    WHERE user_id = p_user_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE RemoveSavedGame (
    IN p_user_id INT,
    IN p_game_id INT
)
BEGIN
    SET @game_index = JSON_UNQUOTE(
        JSON_SEARCH(
            (SELECT saved_games FROM Users WHERE user_id = p_user_id),
            'one',
            p_game_id
        )
    );

    IF @game_index IS NOT NULL THEN
        SET @updated_games_liked = JSON_REMOVE(
            (SELECT saved_games FROM Users WHERE user_id = p_user_id),
            @game_index
        );
        UPDATE Users
        SET saved_games = @updated_games_liked
        WHERE user_id = p_user_id;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE SearchUser(
    IN p_search_query VARCHAR(20)
)
BEGIN
    SELECT user_id, username, name, surname, nationality, date_of_birth
    FROM Users
    WHERE username LIKE CONCAT('%', p_search_query, '%')
       OR name LIKE CONCAT('%', p_search_query, '%')
       OR surname LIKE CONCAT('%', p_search_query, '%');
END$$

DELIMITER ;

