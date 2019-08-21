from query.db import *
import query.sources


def clear_spectra():
    execute('DELETE FROM Spectra;')


def insert_spectra(sourceID, frameID, wavelengths, fluxes):
    str = 'INSERT INTO Spectra (SourceID, FrameID, CCDColumn, Wavelength, Flux) VALUES '
    for i in range(len(fluxes)):
        str += '(%i, %i, %i, %.30f, %.30f),' % (sourceID, frameID, i, wavelengths[i], fluxes[i])
    execute(str[:-1] + ';')


def get_h_alpha(sourceID):
    h_alpha = 6562.8
    width = 5
    lower = h_alpha - width
    upper = h_alpha + width
    df = fetch_panda('SELECT * FROM Spectra WHERE SourceID = %i AND Wavelength > %.30f AND Wavelength < %.30f;' %
                    (sourceID, lower, upper))
    return df.max()['Flux']
