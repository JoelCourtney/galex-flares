drop table if exists Sources;
create table Sources (
	SourceID VARCHAR(20) NOT NULL,
    GezariRA DECIMAL(7,4) NOT NULL,
    GezariDE DECIMAL(7,4) NOT NULL,
    GalexRA DECIMAL(18,15) NOT NULL,
    GalexDE DECIMAL(18,15) NOT NULL,
    PRIMARY KEY (SourceID)
);

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

drop table if exists Stars;
create table Stars (
	GaiaID BIGINT NOT NULL,
    SourceID VARCHAR(20) NOT NULL,
    GaiaRA DECIMAL(18,15),
    GaiaDE DECIMAL(18,15),
    Parallax DECIMAL(18,15),
    PRIMARY KEY (GaiaID),
    FOREIGN KEY (SourceID) REFERENCES Sources(SourceID)
);
    