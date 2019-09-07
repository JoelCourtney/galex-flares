#! /bin/bash

rm -rf lists
mkdir lists

ls original/Bias*r.fits > lists/red_zero.list
ls original/Bias*b.fits > lists/blue_zero.list

ls original/*r.fits | grep -v 'Bias' > lists/red_zero_comp.list
ls original/*b.fits | grep -v 'Bias' > lists/blue_zero_comp.list

sed 's/original/zero_corrected/' lists/red_zero_comp.list > lists/red_zero_corrected.list
sed 's/original/zero_corrected/' lists/blue_zero_comp.list > lists/blue_zero_corrected.list



grep 'FlatR' lists/red_zero_corrected.list > lists/red_flat.list
grep 'FlatB' lists/blue_zero_corrected.list > lists/blue_flat.list

grep -v 'Flat' lists/red_zero_corrected.list > lists/red_flat_comp.list
grep -v 'Flat' lists/blue_zero_corrected.list > lists/blue_flat_comp.list

sed 's/zero_corrected/flat_zero_corrected/' lists/red_flat_comp.list > lists/red_flat_zero_corrected.list
sed 's/zero_corrected/flat_zero_corrected/' lists/blue_flat_comp.list > lists/blue_flat_zero_corrected.list



grep -i -v 'henear' lists/blue_flat_zero_corrected.list > lists/blue_stars.list
grep -i -v 'henear' lists/red_flat_zero_corrected.list > lists/red_stars.list

sed 's/flat_zero_corrected/extracted/' lists/blue_stars.list > lists/blue_stars_extracted.list
sed 's/flat_zero_corrected/extracted/' lists/red_stars.list > lists/red_stars_extracted.list



sed 's/extracted/wavecal/' lists/blue_stars_extracted.list > lists/blue_stars_wavecal.list
sed 's/extracted/wavecal/' lists/red_stars_extracted.list > lists/red_stars_wavecal.list

sed 's/wavecal/fluxcal/' lists/blue_stars_wavecal.list > lists/blue_stars_fluxcal.list
sed 's/wavecal/fluxcal/' lists/red_stars_wavecal.list > lists/red_stars_fluxcal.list

sed 's/wavecal/final/' lists/blue_stars_wavecal.list > lists/blue_stars_final.list
sed 's/wavecal/final/' lists/red_stars_wavecal.list > lists/red_stars_final.list

sed 's/wavecal/printed/g;s/fits/csv csv/g' lists/blue_stars_wavecal.list > lists/blue_stars_printed.list
sed 's/wavecal/printed/g;s/fits/csv csv/g' lists/red_stars_wavecal.list > lists/red_stars_printed.list

