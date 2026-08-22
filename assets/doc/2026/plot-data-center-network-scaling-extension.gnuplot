set terminal pngcairo size 1400,1000 enhanced font "Arial,20"
set output "assets/images/2026/data-center-network-scaling-observed-through-2025.png"

set datafile separator "\t"
set datafile missing "NaN"
set logscale y 10
set xrange [1997:2027]
set yrange [0.0001:1000]
set xtics 5
set ytics ("0.0001" 0.0001, "0.001" 0.001, "0.01" 0.01, "0.1" 0.1, "1" 1, "10" 10, "100" 100, "1000" 1000)
set grid ytics lc rgb "#d9d9d9" lw 1
set grid xtics lc rgb "#e6e6e6" lw 1
set border lw 1.8
set tics nomirror
set key right bottom opaque box lw 1 spacing 1.2 font ",17"

set xlabel "Year"
set ylabel "Capacity (Tb/s)"

switch_fit(x) = 12.8 * (1.41 ** (x - 2018.0))
lane_fit(x) = 0.05 * (1.22 ** (x - 2018.0))

set label 1 "73%/year" at 2010.0,70 tc rgb "#2e7d26" font ",18"
set label 2 "41%/year" at 2014.5,2.0 tc rgb "#1756b3" font ",18"
set label 3 "22%/year" at 2015.0,0.055 tc rgb "#c41212" font ",18"

plot \
  "assets/doc/2026/data-center-network-scaling-extension-2025.tsv" using 1:2 every ::1 with lines \
    lw 3 lc rgb "#2e7d26" title "Data center traffic (AU)", \
  [1999:2025.42] switch_fit(x) with lines lw 2.5 lc rgb "#18a9e6" notitle, \
  "assets/doc/2026/data-center-network-scaling-extension-2025.tsv" using 1:3 every ::1 with points \
    pt 5 ps 1.65 lc rgb "#1756b3" notitle, \
  "assets/doc/2026/data-center-network-scaling-extension-2025.tsv" using 1:3 every ::1 with points \
    pt 5 ps 1.05 lc rgb "#18a9e6" title "Switch chip capacity", \
  [1999:2025.42] lane_fit(x) with lines lw 2.5 lc rgb "#c41212" notitle, \
  "assets/doc/2026/data-center-network-scaling-extension-2025.tsv" using 1:4 every ::1 with points \
    pt 7 ps 1.55 lc rgb "#c41212" notitle, \
  "assets/doc/2026/data-center-network-scaling-extension-2025.tsv" using 1:4 every ::1 with points \
    pt 7 ps 0.95 lc rgb "#ffc21a" \
    title "Per-lane interface rate"
