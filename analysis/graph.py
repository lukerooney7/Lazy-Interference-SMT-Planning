import os
import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

# folder_path = '/Users/lukeroooney/developer/pyPMTEvalToolkit/sandbox-dir/dump_results'
folder_path = '/Users/lukeroooney/Desktop/saved-data/solve-data/numeric-comparison.csv'
classical_domains = {"rovers", "tpp-numeric", "tsp", "trucks", "depot", "tpp", "satellite", "parcprinter", "airport"}
numerical_domains = {"zenotravel", "satellites", "tpp-numeric-numeric", "markettrader", "counters"}
color_map = {
    'Eager ∀-Step Encoding': '#00b5e2',   # Bright Blue
    'Lazy ∀-Step Encoding (': '#ff7f0e',    # Orange
    'Eager ∃-Step Encoding': '#2ca02c',   # Green
    'Lazy ∃-Step Encoding': '#d62728',    # Red
    'Lazy Incremental Cycle ∃-Step': '#9467bd', # Purple
    'Lazy Optimised Code ∀-Step': '#17becf' # Brown
}

total_instances = {
    "ext-plant-watering": 20,
    "mprime": 30,
    "satellite": 20,
    "block-grouping": 192,
    "farmland": 50,
    "pathwaysmetric": 30,
    "sec_clearance": 40,
    "counters": 55,
    "fo-counters": 20,
    "petrobras": 10,
    "delivery": 20,
    "fo-farmland": 25,
    "plant-watering": 51,
    "sugar": 20,
    "depots": 20,
    "fo-sailing": 20,
    "rover": 20,
    "tpp": 40,
    "drone": 20,
    "hydropower": 30,
    "rover-linear": 10,
    "tpp-metric": 10,
    "expedition": 20,
    "markettrader": 20,
    "sailing": 40,
    "zenotravel": 23
}


def cactus_plot(df, domain, encoding, log, max_instance, timeout, par):
    df = df[df['domain'] == domain]
    timeout_penalty = timeout * 60 * par
    # df = df[df['planner_tag'].str.contains(encoding, na=False)]
    df = df[df['status'] == "SOLVED_SATISFICING"]
    plt.figure(figsize=(12, 8))
    plt.hlines(timeout_penalty, xmin=0, xmax=max_instance, colors='red', linestyles='--', label='Timeout Threshold', linewidth=2)

    if log:
        plt.yscale('log')

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        times = []
        times += list(planner_data['planning_time'])
        for i in range(len(planner_data), max_instance + 1):
            times.append(timeout_penalty)
        times.sort()
        x_values = list(range(1, len(times) + 1))
        plt.plot(x_values, times, label=planner_tag, marker='o', markersize=6, linestyle='-', linewidth=2)

    plt.title(f'Camparing Planning Times of Approaches for {domain.upper()} Domain', fontsize=18)
    plt.xlabel('Number of Instances Solved', fontsize=14)
    plt.ylabel('Planning Time (minutes)', fontsize=14)
    plt.legend(title='Approach', loc='upper left', fontsize=12)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('auto')
    plt.tight_layout()
    plt.show()

def scatter_plot(df, log, x, y, min_instance, max_instance, timeout):
    df_filtered = df[(df['planner_tag'].isin([x, y])) &
                     (df['instance'] >= min_instance) &
                     (df['instance'] <= max_instance)]
    timeout_penalty = timeout * 60
    unique_domains = df_filtered['domain'].unique()
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'X']  #
    domain_marker_map = {domain: markers[i % len(markers)] for i, domain in enumerate(unique_domains)}
    plt.figure(figsize=(12, 8))
    plt.axhline(y=timeout_penalty, color='red', linestyle='--', linewidth=1.5, label='Timeout Limit', zorder=0)
    plt.axvline(x=timeout_penalty, color='red', linestyle='--', linewidth=1.5, zorder=0)
    if log:
        plt.yscale('log')
        plt.xscale('log')
    plt.plot([0, timeout_penalty], [0, timeout_penalty], 'k-', linewidth=2, label='Equal Planning Time')
    for domain in unique_domains:
        domain_data = df_filtered[df_filtered['domain'] == domain]

        X = domain_data[domain_data['planner_tag'] == x][['instance', 'planning_time']]
        Y = domain_data[domain_data['planner_tag'] == y][['instance', 'planning_time']]

        merged_data = X.merge(Y, on='instance', how='outer', suffixes=('_x', '_y'))

        graph_data = pd.DataFrame()
        graph_data['x'] = merged_data['planning_time_x']
        graph_data['y'] = merged_data['planning_time_y']
        graph_data['c'] = merged_data['instance']
        graph_data = graph_data.fillna(timeout_penalty)
        cmap = 'Blues' if domain in classical_domains else 'Reds' if domain in numerical_domains else 'Greys'
        # print(graph_data)
        plt.scatter(
            graph_data['x'], graph_data['y'],
            s=100, marker=domain_marker_map[domain], c=graph_data['c'], cmap=cmap,
            edgecolor='black', alpha=0.7, label=domain
        )
    plt.title(f'Comparison of {x} and {y} Planning Times', fontsize=16)
    plt.xlabel(f'{x} Planning Time (s)', fontsize=14)
    plt.ylabel(f'{y} Planning Time (s)', fontsize=14)

    plt.gca().set_aspect('equal', adjustable='box')
    custom_legend = []
    for domain in unique_domains:
        color = 'blue' if domain in classical_domains else 'red' if domain in numerical_domains else 'grey'
        marker = domain_marker_map[domain]
        custom_legend.append(Line2D([0], [0], marker=marker, color='w', markerfacecolor=color,
                                    markeredgecolor='black', markersize=10, label=domain))

    plt.legend(custom_legend, unique_domains, title='Domain', fontsize=12)
    sm_blue = plt.cm.ScalarMappable(cmap='Blues', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                                 vmax=df_filtered['instance'].max()))
    sm_red = plt.cm.ScalarMappable(cmap='Reds', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                               vmax=df_filtered['instance'].max()))
    sm_blue._A = []
    sm_red._A = []
    fig = plt.gcf()
    plt.colorbar(sm_blue, ax=fig.gca(),label='Instance Number (Classical Domains)')
    plt.colorbar(sm_red, ax=fig.gca(),label='Instance Number (Numerical Domains)')

    plt.tight_layout()
    plt.show()


def compare_pars(df, domain, min_instance, max_instance, timeout, par):
    # df = df[df['domain'] == domain]
    timeout_penalty = timeout * par * 60
    total_times = {}

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        total_time = 0

        for instance in range(1, max_instance + 1):
            instance_time = planner_data[planner_data['instance'] == instance]['planning_time']

            if not instance_time.empty:
                total_time += instance_time.iloc[0]
            else:
                total_time += timeout_penalty

        total_times[planner_tag] = total_time

    total_times_series = pd.Series(total_times).sort_values()

    plt.figure(figsize=(10, 6))
    ax = total_times_series.plot(kind='barh', color='steelblue', edgecolor='black')

    ax.set_title(f'{domain} Par {par} comparison for {timeout}m Time Limit', fontsize=16, fontweight='bold',
                 pad=20)
    ax.set_xlabel('Total Planning Time (seconds)', fontsize=14, labelpad=10)
    ax.set_ylabel('Planner Tag', fontsize=14, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for i, (value, label) in enumerate(zip(total_times_series, total_times_series.index)):
        ax.text(value + max(total_times_series) * 0.01, i, f'{value:.2f}', ha='left', va='center', fontsize=10,
                color='black')

    plt.grid(visible=True, which='both', axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


def cactus_all(df, log, total_instances, timeout, par):
    timeout_penalty = timeout * par
    # df = df[df['status'] == "SOLVED_SATISFICING"]
    plt.figure(figsize=(12, 8))
    plt.hlines(timeout_penalty, xmin=0, xmax=total_instances, colors='red', linestyles='--', label='Timeout Threshold', linewidth=2)

    if log:
        plt.yscale('log')

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        times = []
        times += list(planner_data['planning_time'])
        for i in range(len(planner_data), total_instances + 1):
            times.append(timeout_penalty)
        times.sort()
        x_values = list(range(1, len(times) + 1))
        plt.plot(x_values, times, label=planner_tag, marker='o', markersize=6, linestyle='-', linewidth=2)

    plt.title(f'Planning Time Comparison for All Domain Encodings', fontsize=18)
    plt.xlabel('Number of Instances Solved', fontsize=14)
    plt.ylabel('Planning Time (minutes)', fontsize=14)
    plt.legend(title='Approach', loc='upper left', fontsize=12)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('auto')
    plt.tight_layout()
    plt.show()

def par_all(df, total_instances, timeout, par):
    timeout_penalty = timeout * par
    total_times = {}

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        total_time = 0
        for time in planner_data['planning_time']:
            total_time += time
        for i in range(len(planner_data), total_instances + 1):
            total_time += timeout_penalty

        total_times[planner_tag] = total_time

    total_times_series = pd.Series(total_times).sort_values()

    plt.figure(figsize=(10, 6))
    ax = total_times_series.plot(kind='barh', color='steelblue', edgecolor='black')

    ax.set_title(f'Par {par} comparison for {timeout}m Time Limit on {total_instances} Instances', fontsize=16, fontweight='bold',
                 pad=20)
    ax.set_xlabel('Total Planning Time (seconds)', fontsize=14, labelpad=10)
    ax.set_ylabel('Planner Tag', fontsize=14, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for i, (value, label) in enumerate(zip(total_times_series, total_times_series.index)):
        ax.text(value + max(total_times_series) * 0.01, i, f'{value:.2f}', ha='left', va='center', fontsize=10,
                color='black')
    ax.set_xlim([0, max(total_times_series) * 1.1])

    plt.grid(visible=True, which='both', axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


def compare_domains(df, p1, p2, timeout, par):
    timeout_penalty = timeout * par
    df = df[df['planner_tag'].isin([p1, p2])]
    df['domain'] = df['domain'].str.replace(r'sec_clear_\d+_\d+-linear', 'sec_clearance', regex=True)
    domain_ratios = {}
    for domain in df['domain'].unique():
        domain_data = df[df['domain'] == domain]
        data_1 = domain_data[domain_data['planner_tag'] == p1]
        data_2 = domain_data[domain_data['planner_tag'] == p2]
        t1 = sum(data_1['planning_time']) + timeout_penalty * (total_instances[domain] - len(data_1))
        t2 = sum(data_2['planning_time']) + timeout_penalty * (total_instances[domain] - len(data_2))
        ratio = t1 / t2 if t2 > 0 else float('inf')
        domain_ratios[domain] = ratio
    sorted_domains = sorted(domain_ratios.items(), key=lambda x: x[1])
    domains, ratios = zip(*sorted_domains)
    # Plotting the horizontal bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(domains, ratios, color='skyblue', edgecolor='black')
    plt.axvline(1, color='red', linestyle='--', label='Equal Performance (Ratio = 1)')
    plt.xlabel(f'Time Ratio ({p1}/{p2})')
    plt.ylabel('Domains')
    plt.title(f'Comparison of {p1} and {p2} Across Domains')
    plt.legend()
    plt.tight_layout()
    plt.show()








def display_data(df):
    # df = df[df['planner_tag'].str.contains("forall", na=False)]
    # df['planner_tag'] = df['planner_tag'].replace('forall', 'Eager ∀-Step Encoding')
    # df['planner_tag'] = df['planner_tag'].replace('forall-lazy', 'Lazy ∀-Step Encoding')
    # df['planner_tag'] = df['planner_tag'].replace('forall-lazy', 'Lazy ∀ (No Propagation)')
    # df['planner_tag'] = df['planner_tag'].replace('forall-code', 'Lazy ∀-Step Encoding\n(Optimised Code)')
    # df['planner_tag'] = df['planner_tag'].replace('exists', 'Eager ∃-Step Encoding')
    # # df['planner_tag'] = df['planner_tag'].replace('exists-lazy', 'Lazy ∃-Step Encoding')
    # df['planner_tag'] = df['planner_tag'].replace('exists-lazy', 'Lazy ∃ (No Propagation)')
    # df['planner_tag'] = df['planner_tag'].replace('exists-cycle', 'Lazy Incremental Cycle ∃-Step')
    # df['planner_tag'] = df['planner_tag'].replace('forall-prop-id', 'Lazy ∀ (e=Not(B) ids=[A, A])')
    # df['planner_tag'] = df['planner_tag'].replace('exists-prop-id', 'Lazy ∃ (e=Not(B) ids=[A, A])')
    # df['planner_tag'] = df['planner_tag'].replace('exists-prop-clause', 'Lazy ∃ (e=Not(B) or Not(A))')
    # df['planner_tag'] = df['planner_tag'].replace('forall-prop-clause', 'Lazy ∀ (e=Not(B) or Not(A))')
    # df['planner_tag'] = df['planner_tag'].replace('exists-cycle', 'Lazy Incremental Cycle ∃-Step')
    # df['planner_tag'] = df['planner_tag'].replace('exists-cycle', 'Lazy Incremental Cycle ∃-Step')
    df['planning_time'] = df['planning_time'] / 60
    # df = df
    # [(df['planner_tag'] == 'forall-lazy') | (df['planner_tag'] == 'forall-code')]
    # scatter_plot(df, True, "exists","exists-lazy", 1,30, 30)
    # cactus_plot(df, "fo-counters", "tsp", False,  total_instances['petrobras'], 30/60, 1)
    # compare_pars(df, "rovers",0, 10, 30, 2)
    # cactus_all(df, False, 200, 30, 1)
    # par_all(df, 200, 30, 2)
    compare_domains(df, "exists-lazy", "exists", 30, 2)




# df = pd.concat([get_data(folder_path), get_data("/Users/lukeroooney/Desktop/saved-data/dump_results2")], ignore_index=True)
# df = df.drop_duplicates(subset=['instance', 'domain', 'planner_tag'], keep='first')
df =  pd.read_csv(folder_path)

df = df[df['domain'] != 'counters']

# df = df[(df['planner_tag'] != "forall-lazy-optimal") & (df['planner_tag'] != "exists-lazy-optimal")& (df['planner_tag'] != "exists-noprop")& (df['planner_tag'] != "forall-noprop")]
display_data(df)