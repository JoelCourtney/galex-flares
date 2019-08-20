set @n = 55;
set @id = (SELECT SourceID FROM Sources WHERE RowNum = @n);
UPDATE Lightcurves SET SourceNum = @n WHERE SourceID = @id;
UPDATE Flares SET SourceNum = @n WHERE SourceID = @id;
UPDATE SDSS SET SourceNum = @n WHERE SourceID = @id;