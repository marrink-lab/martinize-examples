for dir in $(ls -d *)
do
echo ${dir}
cat ${dir}/energy_comp.dat | grep '\(SR\)'

done
