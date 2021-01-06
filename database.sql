


CREATE TABLE `sendRequestMaster` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `userId` varchar(255) DEFAULT NULL,
  `senduserId` varchar(255) DEFAULT NULL,
  `requestTime` varchar(255) DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT '0',
  `usercreate` varchar(255) DEFAULT NULL,
  `DateCreate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UserUpdate` varchar(255) DEFAULT NULL,
  `DateUpdate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;



CREATE TABLE `messages` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `userId` varchar(255) DEFAULT NULL,
  `senduserId` varchar(255) DEFAULT NULL,
  `messageTime` varchar(255) DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT '0',
  `usercreate` varchar(255) DEFAULT NULL,
  `DateCreate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UserUpdate` varchar(255) DEFAULT NULL,
  `DateUpdate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


CREATE TABLE `userMaster` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `userId` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profilePic` text(512) DEFAULT NULL,
  `status` int(1) NOT NULL DEFAULT '0',
  `usercreate` varchar(255) DEFAULT NULL,
  `DateCreate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UserUpdate` varchar(255) DEFAULT NULL,
  `DateUpdate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;














