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
    """
    Creates a bar chart of average plan length per domain, formatted for academic presentation.

    Parameters:
        data (list of tuples): A list where each tuple contains a domain (str)
                               and a plan length (int/float).
    """
    # Validate input data
    if not data:
        raise ValueError("The input data is empty. Please provide a non-empty dataset.")

    # Compute average plan length for each domain
    domain_totals = defaultdict(int)
    domain_counts = defaultdict(int)

    for domain, plan_length in data:
        domain_totals[domain] += plan_length
        domain_counts[domain] += 1

    # Calculate average plan lengths
    average_plan_lengths = {domain: domain_totals[domain] / domain_counts[domain] for domain in domain_totals}

    # Sort domains by average plan length in descending order
    sorted_domains = sorted(average_plan_lengths.keys(), key=lambda d: average_plan_lengths[d], reverse=True)
    sorted_averages = [average_plan_lengths[domain] for domain in sorted_domains]

    # Plot configuration
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_domains, sorted_averages, color='#4C72B0', edgecolor='black', alpha=0.8)


    # Enhancing the visualization
    plt.xlabel("Domain", fontsize=16, labelpad=10)
    plt.ylabel("Average Plan Length", fontsize=16, labelpad=10)
    plt.title("Average Plan Length by Domain", fontsize=18, pad=15)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=13)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Display the chart
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


folder_path = ""
main(folder_path)