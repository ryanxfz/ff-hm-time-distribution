import pdfplumber
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import defaultdict

def extract_country_finish_times(pdf_path, start_page, end_page):
    country_times = defaultdict(list)
    with pdfplumber.open(pdf_path) as pdf_file:
        print("PDF Scanning started...")
        for i in range(start_page - 1, end_page):
            print(f"Scanning page {i + 1}...")
            page = pdf_file.pages[i]
            cropped_page = page.crop((0, 0, page.width, page.height - 50))
            text = cropped_page.extract_text()
            for line in text.split('\n'):
                match = match = re.search(r'\b([A-Z]{3})\b.*?(\d{1,2}:\d{2}:\d{2})', line)
                if match:
                    nat = match.group(1)
                    time = match.group(2)
                    country_times[nat].append(time)
                elif re.search(r'\d{1,2}:\d{2}:\d{2}', line):
                    print("No country match:", repr(line))
                # print(repr(line))
    print("PDF Scan finished.")
    return country_times

def convert_times_to_seconds(times):
    seconds_list = []
    for time in times:
        parts = time.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        seconds_list.append(total_seconds)
    return seconds_list

def plot_country_distributions(country_times):
    print("Making Histogram for each country with at least 10 runners")
    countryCount = 0
    for nat, times in country_times.items():
        countryCount += 1
        if len(times) < 10: # skip countries with less than 10 participants
            continue
        seconds_list = convert_times_to_seconds(times)
        minutes_list = [s / 60 for s in seconds_list]
        plt.figure(figsize=(16, 6))
        bins = range(60, int(max(minutes_list)) + 2, 1)
        plt.hist(minutes_list, bins=bins, color='blue', edgecolor='black', alpha=0.7)
        plt.title(f'Finish Time Distribution - {nat}')
        plt.xlabel('Finish Time (HH:MM:SS)')
        plt.ylabel('Number of Runners')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True)) # makes sure that the numb er of runner are not decimals
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        xticks = bins[::5]
        xtick_labels = [f"{int(m//60):01d}:{int(m%60):02d}:00" for m in xticks]
        plt.xticks(xticks, xtick_labels, rotation=45)

        total_runners = len(seconds_list)
        plt.savefig(f"histograms/individual-countries/2024/FF_HM_2024_{nat}.pdf")
        plt.close()
        print(f"Histogram for {nat} saved. Total runners: {total_runners}")

    print("PDFs of the histograms have been successfully generated")
    print("There are a total of " + str(countryCount) + " nationalities in this event")

if __name__ == "__main__":
    time_pdf = "results/ffhm2024.pdf"
    with pdfplumber.open(time_pdf) as pdf_file:
        total_pages = len(pdf_file.pages)
    country_times = extract_country_finish_times(time_pdf, 1, total_pages)
    plot_country_distributions(country_times)