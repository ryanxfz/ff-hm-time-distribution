# Frankfurt Half Marathon — Time Distribution

A small Python program to extract finish times from Frankfurt half-marathon result PDFs and plot the finish-time distribution. The purpose of this program is to find an achievable race goal for my race in 2026 by examining finish-time percentiles.

## What it does
- Extracts finish times from a results PDF (https://www.frankfurter-halbmarathon.de/ergebnisarchiv)
- Plots these times on a cumulative grah

## The graphs
- All generated plots are saved to the `histogram` folder in the repository.
- NOTE: Each block (bins) in the histogram represents a 1-minute interval of the finish times.
