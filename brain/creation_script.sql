-- Create a brain with few emotions like as nature :)
-- Brain
CREATE TABLE `brains` (
	`uniquebrain`	NVARCHAR NOT NULL UNIQUE,
	`uniquehuman`	nvarchar ( 8000 ) NOT NULL UNIQUE,
	`ownerof`	NVARCHAR NOT NULL,
	`bornon`	DATETIME NOT NULL,
	`destroyedon`	DATETIME,
	`aliasname`	nvarchar (30) NOT NULL,
	description nvarchar (8000) NOT NULL,
	`isactive`	boolean NOT NULL DEFAULT (1),
	`createdon`	DATETIME,
	FOREIGN KEY(`ownerof`) REFERENCES `humans`(`uniquehuman`)
);

-- People
CREATE TABLE IF NOT EXISTS people(
	rowid integer primary key AUTOINCREMENT,
  Firstname nvarchar(50) NULL,
  Lastname nvarchar(50) NULL,
  Aliasname nvarchar(20) NULL,
  portrait nvarchar(1500) NULL,
  DOB datetime NULL,
  DOD datetime NULL,
  bornplace nvarchar(1000) null,
  diedplace nvarchar(1000) null,
  description nvarchar(80000) null,
);

-- educations
CREATE TABLE IF NOT EXISTS educations(
rowid integer primary key AUTOINCREMENT,
  relatesto int not null,
  subject nvarchar(1000) NULL,
  institute nvarchar(8000) NULL,
  instituteaddress nvarchar(8000) NULL,  
  orderid int null,
  FOREIGN KEY (relatesto) references people(ROWID)
);

-- relationship types
CREATE TABLE `relationshiptypes` (
	`name`	nvarchar ( 30 ) NOT NULL,
	`rowid`	INTEGER PRIMARY KEY AUTOINCREMENT
);

-- relationship with people
CREATE TABLE IF NOT EXISTS relationship(
rowid integer primary key AUTOINCREMENT,
  peopleid int not null,
  relatedto int not null,
  relationshiptype int not null,
  foreign key (peopleid) references people(rowid),
  foreign key (relatedto) references people(rowid),
  foreign key (relationshiptype) references relationshiptypes(rowid)
);
-- humans
CREATE TABLE IF NOT EXISTS `humans` (
	`uniquehuman`	nvarchar ( 8000 ) NOT NULL UNIQUE,
	`aliasname`	nvarchar ( 30 ) NOT NULL,
	`isactive`	boolean NOT NULL DEFAULT (1),
	description nvarchar (8000) NULL,
	`createdon`	DATETIME,
	PRIMARY KEY(`uniquehuman`)
);

--memory
CREATE TABLE IF NOT EXISTS memory(
	rowid integer primary key AUTOINCREMENT,
	convuniqueid	NVARCHAR NOT NULL UNIQUE,
	conversations nvarchar,
	conversationby varchar(10),
	conversationdateon datetime	default current_timestamp
);
