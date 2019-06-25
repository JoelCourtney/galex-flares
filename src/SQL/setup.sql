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

CREATE TABLE Lightcurves (
			SourceID VARCHAR(20) NOT NULL,
            t0 DEC(15,5),
            t1 DEC(15,5),
            t_mean DEC(15,5),
            t0_data DEC(15,5),
            t1_data DEC(15,5),
            cps_bgsub FLOAT(24),
            cps_bgsub_err FLOAT(24),
            flux_bgsub FLOAT(24),
            flux_bgsub_err FLOAT(24),
            mag_bgsub FLOAT(24),
            mag_bgsub_err_1 FLOAT(24),
            mag_bgsub_err_2 FLOAT(24),
            cps_mcatbgsub FLOAT(24),
            cps_mcatbgsub_err FLOAT(24),
            flux_mcatbgsub FLOAT(24),
            flux_mcatbgsub_err FLOAT(24),
            mag_mcatbgsub FLOAT(24),
            mag_mcatbgsub_err_1 FLOAT(24),
            mag_mcatbgsub_err_2 FLOAT(24),
            cps FLOAT(24),
            cps_err FLOAT(24),
            flux FLOAT(24),
            flux_err FLOAT(24),
            mag FLOAT(24),
            mag_err_1 FLOAT(24),
            mag_err_2 FLOAT(24),
            counts INT,
            flat_counts FLOAT(24),
            bg_counts INT,
            bg_flat_counts FLOAT(24),
            exptime FLOAT(24),
            bg FLOAT(24),
            mcat_bg FLOAT(24),
            responses FLOAT(24),
            detxs FLOAT(24),
            detys FLOAT(24),
            detrad FLOAT(24),
            racent FLOAT(24),
            deccent FLOAT(24),
            q_mean FLOAT(24),
            flags INT,
            PRIMARY KEY (SourceID, t0)
            );