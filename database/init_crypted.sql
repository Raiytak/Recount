SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de données :  `depenses`
--
CREATE DATABASE IF NOT EXISTS `recount` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `recount`;

-- --------------------------------------------------------


--
-- Structure de la table `raw_expenses`
--

DROP TABLE IF EXISTS `raw_expenses`;
CREATE TABLE IF NOT EXISTS `raw_expenses` (
  `username` tinytext,
  `ID` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `amount` text NOT NULL,
  `category` text,
  `theme` text,
  `trip` text,
  `company` text,
  `description` text,
  `payment_method` varchar(15) NOT NULL,
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
  `username` tinytext,
  `ID` int(11) NOT NULL,
  `date` date NOT NULL,
  `amount` text NOT NULL,
  `category` text,
  `theme` text,
  `company` text,
  `description` text,
  `trip` text,
  `payment_method` varchar(15) NOT NULL DEFAULT 'card',
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
  `username` tinytext,
  `ID` int(11) DEFAULT NULL,
  `trip` text,
  `date` date NOT NULL,
  `amount` text NOT NULL,
  `category` text,
  `theme` text,
  `company` text,
  `description` text,
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
  `username` tinytext,
  `ID` int(11) NOT NULL,
  `ID_pay_orig` int(11) NOT NULL,
  `date` date NOT NULL,
  `amount` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `reimbursement`
--


COMMIT;


