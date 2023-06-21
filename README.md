# SSS-Invoices

This is a database project written by Mahmud Ghdamsi for the company Smart System Solutions situated in Tripoli, Libya. 
Please refer to Mahmud for any changes to be made to the source code.

## Date of the first release:
21/6/2023

## Version:
1.0

## DOWNLOAD:
To download this app, [click here.](https://github.com/MTstriker10/SSS-Invoices/archive/refs/heads/main.zip)

## INSTALLING:
To run this app, extract the ZIP file to a folder. Next, run SSS Invoices.exe to begin the program.

## REQUIREMENTS:
***APP CANNOT RUN WITHOUT A MYSQL DATABASE.***
The app assumes you have a mysql server database called sssinvoices running with **3** tables: **invoices, products, categories.**
If for some reason some tables or columns are missing or edited, create a backup of all your current table data and then import the files found in **[SQL Dump.rar](https://github.com/MTstriker10/SSS-Invoices/blob/main/SQL%20Dump.rar)**

invoices should contain columns:
```
CREATE TABLE `invoices` (
  `InvoiceNo` varchar(50) NOT NULL,
  `CustomerName` varchar(50) NOT NULL,
  `PhoneNo` varchar(15) NOT NULL,
  `InvoiceDate` date NOT NULL,
  `InstallationTeam` varchar(200) NOT NULL,
  `InstallationDate` date NOT NULL,
  `InvoiceProductCategories` varchar(200) NOT NULL,
  `InvoiceProductIDs` varchar(255) NOT NULL,
  `WarrantyLastDate` date NOT NULL,
  `IsReplaced` tinyint NOT NULL DEFAULT '0',
  `ReplacedProductIDs` text,
  `ReplacedDate` date DEFAULT NULL,
  `Comments` text,
  `QrCode` blob NOT NULL,
  PRIMARY KEY (`InvoiceNo`),
  UNIQUE KEY `InvoiceNo_UNIQUE` (`InvoiceNo`)
```
  
categories should contain columns:
```
CREATE TABLE `categories` (
  `CategoryID` int unsigned NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(45) NOT NULL,
  PRIMARY KEY (`CategoryID`),
  UNIQUE KEY `CategoryID_UNIQUE` (`CategoryID`),
  UNIQUE KEY `CategoryName_UNIQUE` (`CategoryName`)
```
  
 products should contain categories:
```
 CREATE TABLE `products` (
  `ProductID` varchar(50) NOT NULL,
  `ProductCategoryID` int NOT NULL,
  PRIMARY KEY (`ProductID`),
  UNIQUE KEY `ProductID_UNIQUE` (`ProductID`)
```

## Future Features:

1. Edit records section
2. Search box for View Records
3. Dynamic Checkbox for is_replaced
4. mobile support(? unlikely)
5. In-app documentation
