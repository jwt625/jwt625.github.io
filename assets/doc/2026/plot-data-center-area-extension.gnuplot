set terminal pngcairo size 1400,900 enhanced font "Arial,18"
set output "assets/images/2026/data-center-area-observed-through-2025.png"

set datafile separator "\t"
set datafile missing "NaN"
set logscale y 2
set xrange [2005:2026]
set yrange [0.5:512]
set xtics 5
set ytics ("0.5" 0.5, "1" 1, "2" 2, "4" 4, "8" 8, "16" 16, "32" 32, "64" 64, "128" 128, "256" 256, "512" 512)
set grid ytics lc rgb "#d9d9d9" lw 1
set border 3 lw 1.5
set tics nomirror
set key left top spacing 1.15 font ",15"

set xlabel "Year"
set ylabel "Area / operating Net IT space (million sq ft)"

original_fit(x) = 22.0 * (1.37 ** (x - 2017.0))

plot \
  "assets/doc/2026/data-center-area-extension-2025.tsv" using 1:2 every ::1 with linespoints \
    lw 2 pt 7 ps 1.35 lc rgb "#f3b61f" title "Original data", \
  [2006:2017] original_fit(x) with lines lw 2 lc rgb "#333333" title "37%/year fit", \
  [2017:2025] original_fit(x) with lines lw 2 dt 2 lc rgb "#b94a3a" title "Fit extrapolation", \
  "assets/doc/2026/data-center-area-extension-2025.tsv" using 1:3 every ::1 with linespoints \
    lw 3 pt 7 ps 1.25 lc rgb "#168a45" title "Observed hyperscale data"
