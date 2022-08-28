#bin/sh
echo '"name","count"' > hh_uniq_positions.csv;
tail -n +2 hh_positions.csv | cut -f 3 -d ',' | sort | uniq -ci | 
awk  'FS=" " {print $2, "," $1}' | tr -d ' ' >> hh_uniq_positions.csv