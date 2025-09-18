CREATE TABLE `nft` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'NFT ID',
  `opinion_id` bigint NOT NULL COMMENT '观点ID',
  `token_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '链上Token ID',
  `owner_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '当前拥有者地址',
  `mint_price` decimal(20,8) NOT NULL COMMENT '铸造价格',
  `current_price` decimal(20,8) DEFAULT NULL COMMENT '当前价格',
  `is_for_sale` tinyint(1) DEFAULT '0' COMMENT '是否在售',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_token_id` (`token_id`),
  KEY `idx_opinion_id` (`opinion_id`),
  KEY `idx_owner_address` (`owner_address`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_nfts_opinion_id` FOREIGN KEY (`opinion_id`) REFERENCES `opinions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='NFT表';