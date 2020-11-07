CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(25) NOT NULL DEFAULT '',
  `last_name` varchar(25) NOT NULL DEFAULT '',
  `is_professor` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `schools` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `school` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `classes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `school_id` int(11) unsigned NOT NULL,
  `class` varchar(25) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `fk_school_id` (`school_id`),
  CONSTRAINT `fk_school_id` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `office_hours` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `meeting_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_office_hours_user_id` (`user_id`),
  CONSTRAINT `fk_office_hours_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `log_events` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `event` varchar(25) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

CREATE TABLE `attendees` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `office_hours_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `lobby_join` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_office_hours_id` (`office_hours_id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_office_hours_id` FOREIGN KEY (`office_hours_id`) REFERENCES `office_hours` (`id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `attendee_queue_positions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `attendee_id` int(10) unsigned NOT NULL,
  `position` int(11) NOT NULL,
  `estimated_wait_time_seconds` int(11) DEFAULT NULL,
  `actual_wait_time_seconds` int(11) DEFAULT NULL,
  `event_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_attendee_id` (`attendee_id`),
  CONSTRAINT `fk_attendee_id` FOREIGN KEY (`attendee_id`) REFERENCES `attendees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `attendee_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `attendee_id` int(10) unsigned NOT NULL,
  `event_id` int(10) unsigned NOT NULL,
  `event_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_event_id` (`event_id`),
  KEY `fk_attendee_log_attendee_id` (`attendee_id`),
  CONSTRAINT `fk_attendee_log_attendee_id` FOREIGN KEY (`attendee_id`) REFERENCES `attendees` (`id`),
  CONSTRAINT `fk_event_id` FOREIGN KEY (`event_id`) REFERENCES `log_events` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

