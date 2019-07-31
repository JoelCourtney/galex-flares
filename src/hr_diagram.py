import query.gaia
import query.sources
import math
import matplotlib.pyplot as plt


def abs_mag(app_mag, par):
    return app_mag + 5 * (1+math.log10(par/1000.))


MS_color = [-0.037, 0.377, 0.82, 0.98,1.84,2.09,2.25,2.49,3.13,3.95,4.8]  #http://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt
MS_G = [1.09, 2.46, 4.65, 5.53,8.26,8.87,9.38,10.05,12.02,14.48,15.73]
MS_label = ['A0', 'F0', 'G2', 'K0', 'M0', 'M1', 'M2', 'M3', 'M4.5', 'M6', 'M8']


M_gj1243 = abs_mag(11.55, 83.48)
col_gj1243 = 2.83

M_yzcmi = abs_mag(9.68, 167.019)
col_yzcmi = 3.00

M_dtvir = abs_mag(8.91, 86.85)
col_dtvir = 2.16

M_aumic = abs_mag(7.84, 102.89)
col_aumic = 2.12

M_yygem = abs_mag(8.32, 66.23)
col_yygem = 1.94

M_9024 = abs_mag(5.62, 7.169)
col_9024 = 1.028

M_KIC11610797 = abs_mag(11.456, 3.5796)
col_KIC11610797 =0.773

M_KIC11551430a = abs_mag(10.713, 3.056)
col_KIC11551430a = 0.94

M_KIC11551430b = abs_mag(12.62, 2.873)
col_KIC11551430b = 0.88

pearl = abs_mag(10.71, 3.056) # KIC11551430  ... lol this is the one above!
col_pearl = 0.94

pearl2 = abs_mag(12.62, 2.873) # KIC11551430
col_pearl2 = 0.88


def create_hr_diagram():
    sources = query.sources.get_all_sources()
    ids = [source['GaiaID'] for source in sources]
    gaia_objs = query.gaia.query_ids(ids)
    colors = [obj['bp_rp'] for obj in gaia_objs]
    mags = [abs_mag(obj['phot_g_mean_mag'], obj['parallax']) for obj in gaia_objs]
    for i in reversed(range(len(mags))):
        if math.isnan(mags[i]):
            mags.pop(i)
            colors.pop(i)
    plt.rc('font', family='serif', size=14)
    fig = plt.figure(figsize=(10, 8))
    plt.scatter(colors, mags, color='#EE6677', alpha=0.9)
    plt.xlabel('Bp-Rp')
    plt.ylabel('Absolute M_G')
    plt.axis([-1,4,15,-5])
    i = 0
    while i < len(MS_color):
        plt.text(MS_color[i]-0.15, MS_G[i]+1, MS_label[i], alpha=0.5)
        i = i + 1
    plt.plot(col_gj1243, M_gj1243, marker='o', color='black')
    plt.plot(col_dtvir, M_dtvir, marker='o', color='black')
    plt.text(col_dtvir, M_dtvir, 'DT Vir')
    plt.plot(col_aumic, M_aumic, marker='o', color='black')
    plt.text(col_aumic, M_aumic, 'AU Mic')
    plt.plot(col_yygem, M_yygem, marker='o', color='black')
    plt.plot(col_yzcmi, M_yzcmi, marker='o', color='black')
    plt.plot(col_9024, M_9024, marker='o', color='black')

    plt.plot(col_KIC11610797, M_KIC11610797, marker='o', color='black')
    plt.plot(col_KIC11551430a, M_KIC11551430a, marker='o', color='blue')
    plt.plot(col_KIC11551430b, M_KIC11551430b, marker='o', color='yellow')
    plt.plot(col_pearl, pearl, marker='o', color='purple')
    plt.plot(col_pearl2, pearl2, marker='o', color='purple')
    plt.scatter(MS_color, MS_G, color='black', marker='+', alpha=0.5)
    plt.show()


if __name__ == '__main__':
    create_hr_diagram()
