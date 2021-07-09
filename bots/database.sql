/*A file to visualise what the database looks like*/

CREATE TABLE IF NOT EXIST Exp(
    userId INT PRIMARY KEY,
    exp INT DEFAULT 0,
    level INT DEFAULT 0,
);

CREATE TABLE IF NOT EXIST Guilds(
    guild_id INT PRIMARY KEY,
    prefix text DEFAULT '69!'
);
