CREATE TABLE `opinions` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '观点ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '观点内容',
  `is_minted` tinyint(1) DEFAULT '0' COMMENT '是否已铸造NFT',
  `evaluate_price` decimal(20,8) DEFAULT '0.00000000' COMMENT '评估价格',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_opinions_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='观点表';