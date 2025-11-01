from FinishTimes import extract_finish_times
from FinishTimes import convert_times_to_seconds
from FinishTimes import plot_finish_time_distribution
import pdfplumber

if __name__ == "__main__":
    # 2024
    time_pdf_2024 = "results/ffhm2024.pdf"
    with pdfplumber.open(time_pdf_2024) as pdf_file:
        total_pages_2024 = len(pdf_file.pages)
    finish_times_2024 = extract_finish_times(time_pdf_2024, 1, total_pages_2024)

    # 2025
    time_pdf_2025 = "results/ffhm2025.pdf"
    with pdfplumber.open(time_pdf_2025) as pdf_file:
        total_pages_2025 = len(pdf_file.pages)
    finish_times_2025 = extract_finish_times(time_pdf_2025, 1, total_pages_2025)
    all_finish_times = finish_times_2024 + finish_times_2025
    seconds_list = convert_times_to_seconds(all_finish_times)
    plot_finish_time_distribution(seconds_list)