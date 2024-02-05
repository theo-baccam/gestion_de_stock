/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
DROP TABLE IF EXISTS category;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS product;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `quantity` int NOT NULL,
  `id_category` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO category(id,name) VALUES('1','\'Potions\''),('2','\'Wands\''),('3','\'Gems\''),('4','\'Parchments\'');
INSERT INTO product(id,name,description,price,quantity,id_category) VALUES('1','\'Minor Health Potion\'','\'A small flask containing liquid that restores HP\'','50','20','1'),('2','\'Health Potion\'','\'A medium-sized flask containing liquid that restores HP\'','95','15','1'),('3','\'Large Health Potion\'','\'A large flask containing liquid that restores HP\'','140','10','1'),('4','\'Air Wand\'','\'A wand that can manipulate wind and air\'','190','5','2'),('5','\'Illusionist\'s Wand\'','\'A wand that can conjure illusions\'','240','4','2'),('6','\'Empty Gem\'','\'A gem that has yet to be infused with magic\'','110','30','3'),('7','\'Fire Gem\'','\'A gem that has been infused with fire magic\'','230','10','3'),('8','\'Automate The Boring Stuff With Necromancy\'','\'By Ah\'l Sw\'hgart\'','80','10','4');