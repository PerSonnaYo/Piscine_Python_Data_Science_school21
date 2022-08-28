#bin/sh

awk 'BEGIN{FS=OFS="\",\""}
NR==1 {h=$0; next}
{f = split($2, a, "T") }
{file = a[1]".csv"}
{mas[file] += 1}
(mas[file] == 1) {print h > file}
{print >> file}' hh_positions.csv