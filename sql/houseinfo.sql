/*
Navicat MySQL Data Transfer
Source Server         : *
Source Server Version : 50173
Source Host           : *:*
Source Database       : houseinfo
Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001
Date: 2017-03-03 17:17:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `secondhand`
-- ----------------------------
DROP TABLE IF EXISTS `secondhand`;
CREATE TABLE `secondhand` (
  `GUID` varchar(200) NOT NULL,
  `CreateTime` bigint(4) NOT NULL,
  `UpdateTime` bigint(14) NOT NULL,
  `ProductID` varchar(100) NOT NULL,
  `ProductUpdateTime` varchar(50) DEFAULT NULL,
  `ProductUpdateTimeStr` varchar(50) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Community` varchar(100) NOT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `Description` varchar(200) DEFAULT NULL,
  `Tag` varchar(200) DEFAULT NULL,
  `PublisherType` varchar(100) DEFAULT NULL,
  `PublisherName` varchar(100) DEFAULT NULL,
  `ConstructorTime` int(11) DEFAULT NULL,
  `Floor` int(11) DEFAULT NULL,
  `BuildingFloors` int(11) DEFAULT NULL,
  `Orientation` varchar(20) DEFAULT NULL,
  `Layout` varchar(100) DEFAULT NULL,
  `Square` varchar(200) DEFAULT NULL,
  `Price` varchar(20) DEFAULT NULL,
  `PriceUnit` varchar(10) DEFAULT NULL,
  `UnitPrice` varchar(20) DEFAULT NULL,
  `BuildingType` varchar(50) DEFAULT NULL,
  `Decoration` varchar(200) DEFAULT NULL,
  `Tel` varchar(50) DEFAULT NULL,
  `Link` varchar(200) NOT NULL,
  `Source` varchar(50) NOT NULL,
  `Remark` varchar(200) DEFAULT NULL,
  `Pic` int(11) DEFAULT NULL,
  `SummaryText` varchar(500) NOT NULL,
  `Notify` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`GUID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='secondhand house';

-- ----------------------------
-- Add new column ScrapyCause to table secondhand
-- ----------------------------
ALTER TABLE secondhand ADD ScrapyCause varchar(100) DEFAULT NULL;

-- ----------------------------
-- Alter field SummaryText,remove ProductUpdateTime from it
-- ----------------------------
UPDATE secondhand SET SummaryText=CONCAT(productID,"-",title,"-",publisherName,"-",source,"-",square,"-",publisherType,"-",price,"-",tag,"-",layout,"-",unitPrice,"-",priceUnit,"-",location,"-",community) WHERE source="58"

UPDATE secondhand SET SummaryText=CONCAT(productID,"-",title,"-",link,"-",pic,"-",unitPrice,"-",community,"-",price,"-",decoration,"-",layout,"-",buildingType,"-",floor,"-",source,"-",square,"-",location,"-",buildingFloors) WHERE source="shoufc"