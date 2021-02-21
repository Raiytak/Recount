-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  jeu. 17 déc. 2020 à 18:34
-- Version du serveur :  5.7.26
-- Version de PHP :  7.2.18


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `depenses`
--
CREATE DATABASE IF NOT EXISTS `expenses` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `expenses`;

-- --------------------------------------------------------




-- My modifications (the rest was automatically generated)
-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
-- -- GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost';
-- GRANT INSERT, SELECT, DELETE, UPDATE ON `depenses`.* TO 'newsuser'@'localhost' IDENTIFIED BY 'password';
-- End my modif



--
-- Structure de la table `raw_expenses`
--

DROP TABLE IF EXISTS `raw_expenses`;
CREATE TABLE IF NOT EXISTS `raw_expenses` (
  `ID` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `amount` float NOT NULL,
  `category` text,
  `theme` text,
  `trip` text,
  `company` text,
  `description` mediumtext,
  `payment_method` varchar(15) NOT NULL DEFAULT 'card',
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=88030 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `raw_expenses`
--

-- --------------------------------------------------------

--
-- Structure de la table `clean_expenses`
--

DROP TABLE IF EXISTS `clean_expenses`;
CREATE TABLE IF NOT EXISTS `clean_expenses` (
  `ID` int(11) NOT NULL,
  `date` date NOT NULL,
  `amount` float NOT NULL,
  `category` mediumtext,
  `theme` text,
  `company` text,
  `description` text,
  `trip` text,
  `payment_method` text NOT NULL,
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=88030 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `clean_expenses`
--

-- --------------------------------------------------------

--
-- Structure de la table `trip_expenses`
--

DROP TABLE IF EXISTS `trip_expenses`;
CREATE TABLE IF NOT EXISTS `trip_expenses` (
  `ID` int(11) DEFAULT NULL,
  `trip` text,
  `date` date NOT NULL,
  `amount` float NOT NULL,
  `category` mediumtext,
  `theme` text,
  `company` text,
  `description` mediumtext,
  `payment_method` varchar(15) NOT NULL DEFAULT 'card',
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`date`,`_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `trip_expenses`
--

-- --------------------------------------------------------

--
-- Structure de la table `reimbursement`
--

DROP TABLE IF EXISTS `reimbursement`;
CREATE TABLE IF NOT EXISTS `reimbursement` (
  `ID` int(11) NOT NULL,
  `ID_pay_orig` int(11) NOT NULL,
  `date` date NOT NULL,
  `amount` float NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `reimbursement`
--


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


