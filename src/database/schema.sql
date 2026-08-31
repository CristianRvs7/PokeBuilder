CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE teams (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    format VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_teams_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE team_members (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_id INTEGER NOT NULL,
    pokemon_id INTEGER NOT NULL,
    pokemon_name VARCHAR(100) NOT NULL,
    slot SMALLINT NOT NULL,
    ability VARCHAR(100),
    item VARCHAR(100),
    nature VARCHAR(50),
    tera_type VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_team_members_team
        FOREIGN KEY (team_id)
        REFERENCES teams(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_team_member_slot 
        CHECK (slot BETWEEN 1 AND 6),

    CONSTRAINT uq_team_member_slot
        UNIQUE (team_id, slot),

    CONSTRAINT uq_team_pokemon
        UNIQUE (team_id, pokemon_id)
);


CREATE TABLE pokemon_moves (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_member_id INTEGER NOT NULL,
    move_name VARCHAR(100) NOT NULL,
    slot SMALLINT NOT NULL,

    CONSTRAINT fk_pokemon_moves_member
        FOREIGN KEY (team_member_id)
        REFERENCES team_members(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_move_slot
        CHECK (slot BETWEEN 1 AND 4),

    CONSTRAINT uq_pokemon_move_slot
        UNIQUE (team_member_id, slot)
);


CREATE TABLE pokemon_evs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_member_id INTEGER NOT NULL UNIQUE,

    hp SMALLINT NOT NULL DEFAULT 0,
    attack SMALLINT NOT NULL DEFAULT 0,
    defense SMALLINT NOT NULL DEFAULT 0,
    special_attack SMALLINT NOT NULL DEFAULT 0,
    special_defense SMALLINT NOT NULL DEFAULT 0,
    speed SMALLINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_pokemon_evs_member
        FOREIGN KEY (team_member_id)
        REFERENCES team_members(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_ev_hp
        CHECK (hp BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_attack
        CHECK (attack BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_defense
        CHECK (defense BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_special_attack
        CHECK (special_attack BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_special_defense
        CHECK (special_defense BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_speed
        CHECK (speed BETWEEN 0 AND 252),

    CONSTRAINT chk_ev_total
        CHECK (
            hp +
            attack +
            defense +
            special_attack +
            special_defense +
            speed <= 510
        )
);


CREATE TABLE pokemon_ivs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    team_member_id INTEGER NOT NULL UNIQUE,

    hp SMALLINT NOT NULL DEFAULT 31,
    attack SMALLINT NOT NULL DEFAULT 31,
    defense SMALLINT NOT NULL DEFAULT 31,
    special_attack SMALLINT NOT NULL DEFAULT 31,
    special_defense SMALLINT NOT NULL DEFAULT 31,
    speed SMALLINT NOT NULL DEFAULT 31,

    CONSTRAINT fk_pokemon_ivs_member
        FOREIGN KEY (team_member_id)
        REFERENCES team_members(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_iv_hp
        CHECK (hp BETWEEN 0 AND 31),

    CONSTRAINT chk_iv_attack
        CHECK (attack BETWEEN 0 AND 31),

    CONSTRAINT chk_iv_defense
        CHECK (defense BETWEEN 0 AND 31),

    CONSTRAINT chk_iv_special_attack
        CHECK (special_attack BETWEEN 0 AND 31),

    CONSTRAINT chk_iv_special_defense
        CHECK (special_defense BETWEEN 0 AND 31),

    CONSTRAINT chk_iv_speed
        CHECK (speed BETWEEN 0 AND 31)
);

drop table if exists pokemon_ivs cascade;
drop table if exists pokemon_evs cascade;

drop table if exists pokemon_moves cascade;
drop table if exists team_members cascade;

drop table if exists teams cascade;
drop table if exists users cascade;