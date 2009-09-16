-- To create the database:
--   CREATE DATABASE google_group;
--   run as root db admin
--
-- To reload the tables:
--   mysql --user=root --password=root --database=google_group < schema_groups.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+5:30";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `admin_member_id` INT NOT NULL REFERENCES `members`(`id`),
    `group_visibility` ENUM('anybody','members') NOT NULL default 'members',
    `member_visibility` ENUM('members','admin') NOT NULL default 'admin',
    `joining` ENUM('invited', 'request', 'anyone') NOT NULL default 'request',
    `message_send_privileges` ENUM('members','admin') NOT NULL default 'members',
    `invitation_send_privileges` ENUM('members','admin') NOT NULL default 'admin',
    `title` VARCHAR(512) NOT NULL default 'some pagal group',
    `moderation` ENUM('all','new','no') NOT NULL default 'no',
    `description` MEDIUMTEXT NOT NULL,
    `created_at` DATETIME NOT NULL,
    `updated_at` TIMESTAMP
);

DROP TABLE IF EXISTS `discussions`;
CREATE TABLE `discussions` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `created_by` VARCHAR(100) NOT NULL,
    `reply_id` INT NOT NULL REFERENCES `reply`(`id`),
    `content` MEDIUMTEXT NOT NULL
);


DROP TABLE IF EXISTS `members`;
CREATE TABLE `members` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `nickname` VARCHAR(100) NOT NULL,
    `email_address` VARCHAR(100) NOT NULL,
    `group_id` INT NOT NULL REFERENCES `group`(`id`),
    `mail_settings` ENUM('none','email_each','digest','abridged') NOT NULL
);

DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `discussion_id` INT NOT NULL REFERENCES `discussion`(`id`),
    `secondary_reply_id` INT NOT NULL REFERENCES `reply`(`id`),
    `reply_content` MEDIUMTEXT NOT NULL
);

