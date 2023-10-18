CREATE TABLE member (
		member_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(100) NOT NULL,
		pw VARCHAR(100) NOT NULL
);

CREATE TABLE member (
		member_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		email VARCHAR(100) NOT NULL,
		pw VARCHAR(100) NOT NULL
);

CREATE TABLE script (
    script_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT NOT NULL,
    background VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    town VARCHAR(50) NULL,
    town_detail VARCHAR(500) NULL,
    final_goal VARCHAR(300) NULL,
    goal_1 VARCHAR(300) NULL,
    goal_2 VARCHAR(300) NULL,
    goal_3 VARCHAR(300) NULL
);

CREATE TABLE member_player (
    member_id BIGINT NOT NULL,
    player_id BIGINT NOT NULL
);

CREATE TABLE item (
    item_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    detail VARCHAR(300) NULL,
    type INT NOT NULL
);

CREATE TABLE skill (
    skill_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    detail VARCHAR(300) NULL,
    type INT NOT NULL,
    effect INT NOT NULL
);

CREATE TABLE player_skill (
    player_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL
);

CREATE TABLE inventory (
    player_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    amount INT NOT NULL
);

CREATE TABLE option (
    option_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    script_id BIGINT NOT NULL,
    player_id BIGINT NOT NULL,
    options VARCHAR(300) NOT NULL,
    choice VARCHAR(100) NOT NULL
);

ALTER TABLE script ADD CONSTRAINT FK_player_TO_script_1 FOREIGN KEY (
    player_id
)
REFERENCES player (
    player_id
);

ALTER TABLE member_player ADD CONSTRAINT FK_member_TO_member_player_1 FOREIGN KEY (
	member_id
)
REFERENCES member (
	member_id
);

ALTER TABLE member_player ADD CONSTRAINT FK_player_TO_member_player_1 FOREIGN KEY (
	player_id
)
REFERENCES player (
	player_id
);

ALTER TABLE player_skill ADD CONSTRAINT FK_player_TO_player_skill_1 FOREIGN KEY (
	player_id
)
REFERENCES player (
	player_id
);

ALTER TABLE player_skill ADD CONSTRAINT FK_skill_TO_player_skill_1 FOREIGN KEY (
	skill_id
)
REFERENCES skill (
	skill_id
);

ALTER TABLE inventory ADD CONSTRAINT FK_player_TO_inventory_1 FOREIGN KEY (
	player_id
)
REFERENCES player (
	player_id
);

ALTER TABLE inventory ADD CONSTRAINT FK_item_TO_inventory_1 FOREIGN KEY (
	item_id
)
REFERENCES item (
	item_id
);

ALTER TABLE option ADD CONSTRAINT FK_script_TO_option_1 FOREIGN KEY (
	script_id
)
REFERENCES script (
	script_id
);

ALTER TABLE option ADD CONSTRAINT FK_script_TO_option_2 FOREIGN KEY (
	player_id
)
REFERENCES script (
	player_id
);
