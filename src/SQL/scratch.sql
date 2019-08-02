SELECT * FROM Sources;

SELECT * FROM Flares;


ALTER TABLE Flares ADD (
    TPeak DEC(15,5)
);

ALTER TABLE Flares
    MODIFY Quality INT NOT NULL;