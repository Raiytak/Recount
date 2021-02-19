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
CREATE DATABASE IF NOT EXISTS `depenses` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `depenses`;

-- --------------------------------------------------------




-- My modifications (the rest was automatically generated)
-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
-- -- GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost';
-- GRANT INSERT, SELECT, DELETE, UPDATE ON `depenses`.* TO 'newsuser'@'localhost' IDENTIFIED BY 'password';
-- End my modif



--
-- Structure de la table `depenses_brutes`
--

DROP TABLE IF EXISTS `depenses_brutes`;
CREATE TABLE IF NOT EXISTS `depenses_brutes` (
  `ID` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `montant` float NOT NULL,
  `theme` text,
  `soustheme` text,
  `voyage` text,
  `entreprise` text,
  `description` mediumtext,
  `methode_payement` varchar(15) NOT NULL DEFAULT 'carte',
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=88030 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `depenses_brutes`
--

-- --------------------------------------------------------

--
-- Structure de la table `depenses_propres`
--

DROP TABLE IF EXISTS `depenses_propres`;
CREATE TABLE IF NOT EXISTS `depenses_propres` (
  `ID` int(11) NOT NULL,
  `date` date NOT NULL,
  `montant` float NOT NULL,
  `theme` mediumtext,
  `soustheme` text,
  `entreprise` text,
  `description` text,
  `voyage` text,
  `methode_payement` text NOT NULL,
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`_id`)
) ENGINE=MyISAM AUTO_INCREMENT=88030 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `depenses_propres`
--

-- --------------------------------------------------------

--
-- Structure de la table `depenses_voyages`
--

DROP TABLE IF EXISTS `depenses_voyages`;
CREATE TABLE IF NOT EXISTS `depenses_voyages` (
  `ID` int(11) DEFAULT NULL,
  `voyage` text,
  `date` date NOT NULL,
  `montant` float NOT NULL,
  `theme` mediumtext,
  `soustheme` text,
  `entreprise` text,
  `description` mediumtext,
  `methode_payement` varchar(15) NOT NULL DEFAULT 'carte',
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`date`,`_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `depenses_voyages`
--

-- --------------------------------------------------------

--
-- Structure de la table `remboursements`
--

DROP TABLE IF EXISTS `remboursements`;
CREATE TABLE IF NOT EXISTS `remboursements` (
  `ID` int(11) NOT NULL,
  `ID_pay_orig` int(11) NOT NULL,
  `date` date NOT NULL,
  `montant` float NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `remboursements`
--


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


