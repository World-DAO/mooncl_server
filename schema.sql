-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: mooncl_db
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `nft_transactions`
--

DROP TABLE IF EXISTS `nft_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nft_transactions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nft_id` bigint NOT NULL,
  `from_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `to_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `transaction_type` enum('mint','transfer','sale') COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(20,8) DEFAULT NULL,
  `transaction_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` bigint DEFAULT NULL,
  `gas_fee` decimal(20,8) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_nft_id` (`nft_id`),
  KEY `idx_from_address` (`from_address`),
  KEY `idx_to_address` (`to_address`),
  KEY `idx_transaction_type` (`transaction_type`),
  KEY `idx_transaction_hash` (`transaction_hash`),
  CONSTRAINT `nft_transactions_ibfk_1` FOREIGN KEY (`nft_id`) REFERENCES `nfts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='NFT交易记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nfts`
--

DROP TABLE IF EXISTS `nfts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nfts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `opinion_id` bigint NOT NULL,
  `token_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `creator_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `image_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `metadata` json DEFAULT NULL,
  `mint_transaction_hash` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mint_price` decimal(20,8) NOT NULL,
  `current_price` decimal(20,8) DEFAULT NULL,
  `is_for_sale` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  KEY `idx_opinion_id` (`opinion_id`),
  KEY `idx_token_id` (`token_id`),
  KEY `idx_owner_address` (`owner_address`),
  KEY `idx_creator_address` (`creator_address`),
  KEY `idx_is_for_sale` (`is_for_sale`),
  CONSTRAINT `nfts_ibfk_1` FOREIGN KEY (`opinion_id`) REFERENCES `opinions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='NFT表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `opinions`
--

DROP TABLE IF EXISTS `opinions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opinions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tags` json DEFAULT NULL,
  `is_minted` tinyint(1) DEFAULT '0',
  `mint_price` decimal(20,8) DEFAULT '0.00000000',
  `view_count` int DEFAULT '0',
  `like_count` int DEFAULT '0',
  `comment_count` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_category` (`category`),
  KEY `idx_is_minted` (`is_minted`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `opinions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='观点表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address` (`address`),
  KEY `idx_address` (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-05 19:40:51
