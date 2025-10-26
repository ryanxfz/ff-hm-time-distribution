# Frankfurt Half Marathon: Time Distribution

A small Python script to extract finish times from Frankfurt half-marathon result PDFs and plot the finish-time distribution. The purpose of this script is to find an achievable race goal for my race in 2026 by examining finish-time percentiles. It's also a nice little project to practice some python.

## What it does
- Extracts finish times from a results PDF (https://www.frankfurter-halbmarathon.de/ergebnisarchiv)
- Plots these times on a histogram

## The histogram
- The generated plots for the year 2024 and 2025 are saved to the `histograms` folder in the repository. The file names are `FF_HM_2024.pdf` and `FF_HM_2025.pdf` respectively.
- NOTE: Each block (bins) in the histogram represents a 1-minute interval of the finish times.
- ## Extension:
    - I've also added the histograms of each countries with at least 10 runners... cuz why not.
    - These histograms can be found in `histograms/individual-countries`. You can then select the year you want to see.

## The highlights:
### 2025:
- Total runners: 8501
- Fastest time: 1:02:35
- Percentiles:
    - 1%: 1:17:55
    - 10%: 1:33:29
    - 25%: 1:44:24
    - 50%: 1:57:01
    - 75%: 2:10:53

### 2024:
- Total runners: 7505
- Fastest time: 1:02:46
- Percentiles:
    - 1%: 1:17:51
    - 10%: 1:33:27
    - 25%: 1:44:12
    - 50%: 1:56:25
    - 75%: 2:09:23