

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

--
-- Structure de la table `raw_expenses`
--

DROP TABLE IF EXISTS `raw_expenses`;
CREATE TABLE IF NOT EXISTS `raw_expenses` (
  `username` mediumtext,
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
  `username` mediumtext,
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
  `username` mediumtext,
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
  `username` mediumtext,
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


