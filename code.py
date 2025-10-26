import pdfplumber
import numpy as np
import re
import matplotlib.pyplot as plt

# 1 PDF Point = 1/72 inchj
# to avoid reading unwanted values in the header/footer

# use this one if you wanna see a range of pages
def extract_finish_times(pdf_path, start_page, end_page):
    finish_times = []
    with pdfplumber.open(pdf_path) as pdf_file:
        print("PDF Scanning started...")
        for i in range(start_page - 1, end_page):
            print(f"Scanning page { i +1 }...")
            page = pdf_file.pages[i]
            cropped_page = page.crop((0, 0, page.width, page.height - 50))
            text = cropped_page.extract_text()
            times = re.findall(r'(?<!\+)\b\d{1,2}:\d{2}:\d{2}\b', text)
            finish_times.extend(times)
    print("PDF Scan finished.")
    return finish_times


# def extract_finish_times(pdf_path):
#     finish_times = []
#     with pdfplumber.open(pdf_path) as pdf_file:
#         print("Scanning the pdf...")
#         page = pdf_file.pages[3]
#         cropped_page = page.crop((0, 0, page.width, page.height - 50))
#         text = cropped_page.extract_text()
#         times = re.findall(r'(?<!\+)\b\d{1,2}:\d{2}:\d{2}\b', text)
#         finish_times.extend(times)
#     print("PDF Scan finished.")
#     return finish_times

def convert_times_to_seconds(times):
    print("Processing the data...")
    seconds_list = []
    for time in times:
        parts = time.split(':')
        if len(parts) == 3:  # HH:MM:SS format
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # MM:SS format
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        seconds_list.append(total_seconds)
    return seconds_list


def plot_finish_time_distribution(seconds_list):
    print("Plotting the data...")
    minutes_list = [s / 60 for s in seconds_list]
    
    plt.figure(figsize=(16, 6))
    bins = range(60, int(max(minutes_list)) + 2, 1)
    plt.hist(minutes_list, bins=bins, color='blue', edgecolor='black', alpha=0.7)
    plt.title('Finish Time Distribution')
    plt.xlabel('Finish Time (HH:MM:SS)')
    plt.ylabel('Number of Runners')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    xticks = bins[::5]
    xtick_labels = [f"{int(m//60):01d}:{int(m%60):02d}:00" for m in xticks]
    plt.xticks(xticks, xtick_labels, rotation=45)
    
    # standout values
    total_runners = len(seconds_list)
    fastest = min(seconds_list)
    slowest = max(seconds_list)
    percentiles = [1, 10, 25, 50, 75]
    percentile_values = [int(np.percentile(seconds_list, p)) for p in percentiles]
    
    def sec_to_str(s):
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h}:{m:02d}:{sec:02d}"
    
    # plot the lines for the standout values on the graph
    plt.axvline(fastest/60, color='green', linestyle='--', label=f"Fastest: {sec_to_str(fastest)}")
    for p, val in zip(percentiles, percentile_values):
        plt.axvline(val/60, linestyle=':', label=f"Top {p}%: {sec_to_str(val)}")
    
    plt.legend(loc='upper right')
   
    print(f"Total runners: {total_runners}")
    print(f"Fastest: {sec_to_str(fastest)}")
    print(f"Most time: {sec_to_str(slowest)}")
    for p, val in zip(percentiles, percentile_values):
        print(f"Top {p}%: {sec_to_str(val)}")
    plt.text(0.01, 0.95, f"Total runners: {total_runners}", ha='left', va='top',
             transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    plt.tight_layout()
    plt.savefig("graphs/FF_HM_2025.pdf")
    print("Distribution graph pdf successfully created!")

if __name__ == "__main__":
    time_pdf = "results/ffhm2025.pdf"
    with pdfplumber.open(time_pdf) as pdf_file:
        total_pages = len(pdf_file.pages)
    finish_times = extract_finish_times(time_pdf, 1, total_pages)
    seconds_list = convert_times_to_seconds(finish_times)
    plot_finish_time_distribution(seconds_list)