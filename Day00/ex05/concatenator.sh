#bin/sh
echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > hh_positions_1.csv
cat 20*.csv | grep -v "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" >> hh_positions_1.csv