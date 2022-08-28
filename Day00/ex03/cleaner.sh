#bin/sh
(cat hh_sorted.csv | head -n +1;
cat hh_sorted.csv | tail -n +2 |
awk 'BEGIN{FS=OFS=","} 
    { jun = match($3, /[Jj]unior/)}
    { mid = match($3, /[Mm]iddle/)}
    { sir = match($3, /[Ss]enior/)}
    {if (jun > 0  && mid > 0 && sir > 0) 
        $3 = "\"Junior/Middle/Senior\""
    else if (jun > 0  && mid > 0)
        $3 = "\"Junior/Middle\""
    else if (jun > 0  && sir > 0)
        $3 = "\"Junior/Senior\""
    else if (mid > 0  && sir > 0)
        $3 = "\"Middle/Senior\""
    else if (jun > 0)
        $3 = "\"Junior\""
    else if (mid > 0)
        $3 = "\"Middle\""
    else if (sir > 0)
        $3 = "\"Senior\""
    else
        $3 = "\"-\""
     }1' $1 ) > hh_positions.csv