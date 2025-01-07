import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def extract_data(file_path):
    """Extracts domain, planner tag, and plan length from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)


    domain = data.get("task-info", {}).get("domain", "")
    instance = data.get("task-info", {}).get("instance", 0)
    if "sec" not in domain and instance < 20:
        plan_length = len(data.get("task-result", {}).get("plan", []))

        return domain, plan_length


def create_bar_chart(data):
    """Creates a bar chart of average plan length per domain."""
    # Compute average plan length for each domain
    domain_totals = defaultdict(int)
    domain_counts = defaultdict(int)

    for domain, plan_length in data:
        domain_totals[domain] += plan_length
        domain_counts[domain] += 1

    average_plan_lengths = {domain: domain_totals[domain] / domain_counts[domain] for domain in domain_totals}

    # Sort domains alphabetically
    sorted_domains = sorted(average_plan_lengths.keys(), key=lambda d: average_plan_lengths[d], reverse=True)
    sorted_averages = [average_plan_lengths[domain] for domain in sorted_domains]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_domains, sorted_averages, color='skyblue')
    plt.xlabel("Domain")
    plt.ylabel("Average Plan Length")
    plt.title("Average Plan Length by Domain")
    plt.xticks(rotation=45, ha="right")  # Rotate domain names for readability
    plt.tight_layout()
    plt.show()


def main(folder_path):
    """Main function to process all files and create the bar chart."""
    all_data = []

    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            extracted_data = extract_data(file_path)
            if extracted_data:
                all_data.append(extracted_data)

    if all_data:
        create_bar_chart(all_data)
    else:
        print("No valid data found.")


folder_path = "/Users/lukeroooney/Desktop/Dissertation/data/dump_files/eager"
main(folder_path)