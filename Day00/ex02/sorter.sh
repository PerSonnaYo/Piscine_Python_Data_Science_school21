#bin/sh
(cat hh.csv | head -n +1; cat hh.csv | tail -n +2 | sort -t ',' -k 2 -k 1n) > hh_sorted.csv