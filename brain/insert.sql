BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `humans` (
	`uniquehuman`	nvarchar ( 8000 ) NOT NULL,
	`aliasname`	nvarchar ( 30 ) NOT NULL,
	`isactive`	boolean NOT NULL DEFAULT (1),
	PRIMARY KEY(`uniquehuman`)
);
INSERT INTO `humans` (uniquehuman,aliasname,description,isactive) VALUES ('1','',1),
 ('abcd12345','anbu','you have relationship with me since',1) 
COMMIT;

INSERT INTO `brains` (uniquebrain,ownerof,bornon,aliasname,description,isactive) VALUES
 ('abcd123456789','abcd12345','07/06/2018','sweety','I have relationship with you',1) 
COMMIT;
