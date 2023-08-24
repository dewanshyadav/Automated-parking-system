mysql> create database parking_system;
mysql> use parking_system;

mysql> SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
mysql> SET AUTOCOMMIT = 0;
mysql> START TRANSACTION;
mysql> SET time_zone = "+00:00";

mysql> DROP TABLE IF EXISTS `login`;
mysql> CREATE TABLE IF NOT EXISTS `login` (`id` int(11) NOT NULL AUTO_INCREMENT,`name` char(30) DEFAULT NULL, `pwd` char(30) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
mysql> INSERT INTO `login` (`id`, `name`, `pwd`) VALUES (1, 'dewansh', '12345'),(2, 'admin', '0000');

mysql> DROP TABLE IF EXISTS `parking_space`;
mysql> CREATE TABLE IF NOT EXISTS `parking_space` (`slot` int(11) NOT NULL AUTO_INCREMENT,`type_id` int(11) DEFAULT NULL,`status` char(20) DEFAULT NULL,PRIMARY KEY (`slot`)) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
mysql> INSERT INTO `parking_space` (`slot`, `type_id`, `status`) VALUES (1, 1, 'full'), (2, 2, 'full'), (3, 3, 'open'), (4, 4, 'open'), (5, 5, 'open'), (6, 1, 'open'), (7, 1, 'open'), (8, 1, 'open'), (9, 1, 'open'), (10, 1, 'open'), (11, 1, 'open'), (12, 1, 'open'), (13, 2, 'open'), (14, 2, 'open'), (15, 2, 'open'), (16, 2, 'open'), (17, 2, 'open'), (18, 2, 'open'), (19, 2, 'open'), (20, 3, 'open'), (21, 3, 'open'), (22, 3, 'open'), (23, 3, 'open'), (24, 3, 'open'), (25, 4, 'open'), (26, 4, 'open'), (27, 5, 'open'), (28, 5, 'open');

mysql> DROP TABLE IF EXISTS `parking_type`;
mysql> CREATE TABLE IF NOT EXISTS `parking_type` (`type_id` int(11) NOT NULL AUTO_INCREMENT,`name` char(20) DEFAULT NULL,`price` float(7,2) DEFAULT NULL, PRIMARY KEY (`type_id`)) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
mysql> INSERT INTO `parking_type` (`type_id`, `name`, `price`) VALUES (1, 'two Wheelar', 30.00), (2, 'car', 50.00), (3, 'bus', 250.00), (4, 'truck', 350.00), (5, 'trolly', 450.00);

mysql> DROP TABLE IF EXISTS `transaction`;
mysql> CREATE TABLE IF NOT EXISTS `transaction` (`id` int(11) NOT NULL AUTO_INCREMENT,`vehicle_id` char(20) DEFAULT NULL,`parking_id` int(11) DEFAULT NULL,`entry_date` date DEFAULT NULL,`exit_date` date DEFAULT NULL,`amount` float(10,2) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
mysql> INSERT INTO `transaction` (`id`, `vehicle_id`, `parking_id`, `entry_date`, `exit_date`, `amount`) VALUES(1, 'DL14CB 1087', 1, '2021-03-08', '2021-03-08', 30.00),(2, 'DL13CB 1090', 29, '2021-03-09', '2021-03-09', 35.00),(3, 'dlcb 1090', 1, '2021-03-09', NULL, NULL),(4, 'dl13cd 1020', 2, '2021-03-09', NULL, NULL);

mysql> commit;
