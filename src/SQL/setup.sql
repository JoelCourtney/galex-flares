drop table if exists Sources;
create table Sources (
	RowNum INT NOT NULL AUTO_INCREMENT,
	SourceID VARCHAR(20) NOT NULL,
    GezariRA DECIMAL(7,4) NOT NULL,
    GezariDE DECIMAL(7,4) NOT NULL,
    GalexRA DECIMAL(18,15) NOT NULL,
    GalexDE DECIMAL(18,15) NOT NULL,
    GaiaID BIGINT NOT NULL,
    GaiaRA DECIMAL(18,15) NOT NULL,
    GaiaDE DECIMAL(18,15) NOT NULL,
    Parallax DECIMAL(18,15),
    PRIMARY KEY (RowNum)
);
alter table Sources add RowNum INT AUTO_INCREMENT;

drop table if exists Flares;
create table Flares (
	FlareID INT NOT NULL AUTO_INCREMENT,
	SourceID VARCHAR(20) NOT NULL,
    FlareStart INT NOT NULL,
    FlareEnd INT NOT NULL,
    QuiesentStart INT NOT NULL,
    QuiesentEnd INT NOT NULL,
	PRIMARY KEY (FlareID),
    FOREIGN KEY (SourceID) REFERENCES Sources(SourceID)
);

create table Locks (
	SourceID VARCHAR(20) NOT NULL,
    Attribute VARCHAR(15) NOT NULL,
    PRIMARY KEY (SourceID, Attribute)
    
);
ALTER TABLE Locks ADD Status VARCHAR(10) NOT NULL;

drop table Parameters;
create table Parameters (
	Parameter VARCHAR(30) NOT NULL,
    Val DECIMAL(15,8) NOT NULL,
    PRIMARY KEY (Parameter)
);
INSERT INTO Parameters (Parameter, Val) VALUES ('ApertureRadius', 0.0045);
INSERT INTO Parameters (Parameter, Val) VALUES ('AnnulusInnerRadius', 0.005);
INSERT INTO Parameters (Parameter, Val) VALUES ('AnnulusOuterRadius', 0.006);