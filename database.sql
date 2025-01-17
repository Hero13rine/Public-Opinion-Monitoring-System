-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: weibo_analysis
-- ------------------------------------------------------
-- Server version	8.0.33

CREATE TABLE `weibo_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `weibo_id` varchar(64) NOT NULL,
  `text` text NOT NULL,
  `url` varchar(255) NOT NULL,
  `username` varchar(64) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `analyzed` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `analysis_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment_id` int NOT NULL,
  `sensitive_words` json NOT NULL,
  `alert_level` varchar(32) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comment` (`comment_id`),
  CONSTRAINT `fk_comment` FOREIGN KEY (`comment_id`) REFERENCES `weibo_comments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
