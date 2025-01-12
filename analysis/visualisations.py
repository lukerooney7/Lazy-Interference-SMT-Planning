import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

folder_path = '/Users/lukeroooney/Desktop/Dissertation/data/csvs/all.csv'

cls_domains = {
    "airport", "airport-adl", "assembly", "blocks", "blocks-3op", "briefcaseworld",
    "cavediving", "cybersec", "depot", "driverlog", "elevators-00-adl", "elevators-00-full",
    "elevators-00-strips", "ferry", "freecell", "fridge", "grid", "gripper", "hanoi",
    "logistics", "miconic", "miconic-fulladl", "miconic-simpleadl",
    "movie", "mystery", "no-mprime", "no-mystery", "openstacks", "openstacks-strips",
    "parcprinter-08-strips", "pathways", "pathways-noneg", "pegsol", "pipesworld-06",
    "pipesworld-notankage", "pipesworld-tankage", "psr-small", "rovers", "rovers-02",
    "scanalyzer", "schedule", "tpp", "trucks", "trucks-strips", "tsp", "elevators", "parcprinter"
}

num_domains = {
    "block-grouping", "counters", "delivery", "depots", "drone", "expedition",
    "ext-plant-watering", "farmland", "fo-counters", "fo-farmland", "fo-sailing",
    "hydropower", "markettrader", "mprime", "pathwaysmetric", "petrobras",
    "plant-watering", "rover", "rover-linear", "sailing", "satellite", "sec_clearance",
    "settlers", "sugar", "tpp", "tpp-metric", "zenotravel"
}

color_map = {
    'Eager ∀ (No Propagator)': 'grey',
    'Eager ∀': 'orange',
    'Naive Lazy ∀': 'red',
    'Code-Optimised Lazy ∀': 'brown',
    'Final Conflict ∀': 'brown',
    'Stepsharing ∀': 'red',
    'Neighbours ∀': 'red',
    'Lazy ∀': 'red',
    'Decide ∀': 'red',
    'Eager ∃ (No Propagator)': 'black',
    'Eager ∃': 'blue',
    'Naive Lazy ∃': 'purple',
    'Code-Optimised Lazy ∃': 'green',
    'Lazy ∃': 'green',
    'Final Conflict ∃': 'green',
    'Stepsharing ∃': 'purple',
    'Ghost Node ∃': 'purple',
    'Decide ∃': 'purple',
}

total_instances = {
    "airport": 50,
    "block-grouping": 25,
    "blocks": 15,
    "blocks-3op": 12,
    "briefcaseworld": 1,
    "counters": 54,
    "cybersec":10,
    "delivery": 1,
    "depot": 8,
    "depots": 10,
    "driverlog": 12,
    "drone": 3,
    "elevators": 33,
    "expedition": 2,
    "ferry": 26,
    "fo-counters": 3,
    "fo-farmland": 6,
    "fo-sailing": 1,
    "gripper": 4,
    "hanoi": 4,
    "hydropower": 2,
    "miconic": 33,
    "movie": 30,
    "mprime": 30,
    "openstacks": 5,
    "parcprinter": 28,
    "pathways": 4,
    "pathways-noneg": 4,
    "logistics":10,
    "pathwaysmetric": 1,
    "pegsol": 8,
    "petrobras": 15,
    "pipesworld-notankage": 11,
    "plant-watering": 1,
    "psr-small": 49,
    "rover": 15,
    "rover-linear": 9,
    "rovers": 15,
    "satellite": 7,
    "scanalyzer": 3,
    "schedule": 1,
    "sugar": 19,
    "sec_clearance": 40,
    "tpp":20,
    "tpp-metric": 5,
    "trucks": 10,
    "tsp": 9,
    "zenotravel": 15
}


'''
    Cactus plot of all planners for a specific domain
'''
def cactus_plot(df, domain, log, max_instance, timeout, par):
    df = df[df['domain'] == domain]
    timeout_penalty = timeout * par
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


'''
    Displays an NxN grid of cactus plots for a specific domain as above  
'''
def cactus_grid(df, domains, log, timeout, par):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12), sharey='row')
    handles, labels = [], []  # To collect handles and labels for the single legend

    for ax, domain in zip(axs.flat, domains):
        domain_df = df[df['domain'] == domain]
        timeout_penalty = timeout * par
        domain_df = domain_df[domain_df['status'] == "SOLVED_SATISFICING"]
        threshold_line = ax.hlines(timeout_penalty, xmin=0, xmax=total_instances[domain], colors='red',
                                   linestyles='--', label='Timeout Threshold', linewidth=2)
        if log:
            ax.set_yscale('log')
        for planner_tag in domain_df['planner_tag'].unique():
            planner_data = domain_df[domain_df['planner_tag'] == planner_tag]
            times = list(planner_data['planning_time'])
            for i in range(len(planner_data), total_instances[domain] + 1):
                times.append(timeout_penalty)
            times.sort()
            x_values = list(range(1, len(times) + 1))
            line, = ax.plot(x_values, times, label=planner_tag, color=color_map.get(planner_tag, 'blue'),
                            marker='o', markersize=6, linestyle='-', linewidth=3)
            handles.append(line)
            labels.append(planner_tag)
        ax.set_title(f'{domain.upper()} Domain', fontsize=16, fontweight="bold")
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.grid(which='both', linestyle='--', linewidth=0.5)

    # Shared labels
    fig.text(0.07, 0.5, 'Planning Time (minutes)', va='center', ha='center', rotation='vertical', fontsize=16)
    fig.text(0.54, 0.07, 'Number of Instances Solved', va='center', ha='center', fontsize=16)

    unique_handles_labels = {label: handle for handle, label in zip(handles, labels)}
    handles, labels = list(unique_handles_labels.values()), list(unique_handles_labels.keys())
    handles.append(threshold_line)
    labels.append('Timeout Threshold')

    fig.legend(handles, labels, fontsize=16, loc='upper center', bbox_to_anchor=(0.54, 0.95), ncol=5)
    plt.tight_layout(rect=[0.08, 0.08, 1, 0.9])
    plt.show()


'''
    Scatter plot which allows two approaches to be compared, plotting the times of one on the x-axis
    and the other on the y-axis.
'''
def scatter_plot(df, log, x, y, timeout_penalty):
    df_filtered = df[(df['planner_tag'].isin([x, y]))]
    unique_domains = df_filtered['domain'].unique()
    # Markers symbols gathered from https://matplotlib.org/stable/api/markers_api.html
    markers = [
        'o', 's', '^', 'D', 'v', 'p', '*', 'X',
        'H', 'h', '8', 'P', 'd',
        '>', '<', '1', '2', '3', '4',
        '8', 'p', 'H', 'h', 'v',
                ]
    domain_marker_map = {domain: markers[i % len(markers)] for i, domain in enumerate(unique_domains)}
    plt.figure(figsize=(16, 8))
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
        cmap = 'Blues' if domain in cls_domains else 'Reds' if domain in num_domains else 'Greys'
        plt.scatter(
            graph_data['x'], graph_data['y'],
            s=100, marker=domain_marker_map[domain], c=graph_data['c'], cmap=cmap,
            edgecolor='black', alpha=0.7, label=domain
        )
    plt.title(f'Comparison of {x} and {y} Planning Times', fontsize=16)
    plt.xlabel(f'{x} Planning Time (s)', fontsize=14)
    plt.ylabel(f'{y} Planning Time (s)', fontsize=14)
    plt.gca().set_aspect('equal', adjustable='box')
    blue_legend = []
    red_legend = []
    grey_legend = []

    # Custom legend
    for domain in unique_domains:
        color = 'blue' if domain in cls_domains else 'red' if domain in num_domains else 'grey'
        marker = domain_marker_map[domain]

        if color == 'blue':
            blue_legend.append(Line2D([0], [0], marker=marker, color='w', markerfacecolor=color,
                                      markeredgecolor='black', markersize=10, label=domain))
        elif color == 'red':
            red_legend.append(Line2D([0], [0], marker=marker, color='w', markerfacecolor=color,
                                     markeredgecolor='black', markersize=10, label=domain))

    custom_legend = blue_legend + red_legend
    plt.legend(custom_legend, [line.get_label() for line in blue_legend + red_legend + grey_legend],
               title='Domain', fontsize=12, loc='upper right', bbox_to_anchor=(-0.1, 1), ncol=2)

    sm_blue = plt.cm.ScalarMappable(cmap='Blues', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                                 vmax=df_filtered['instance'].max()))
    sm_red = plt.cm.ScalarMappable(cmap='Reds', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                               vmax=df_filtered['instance'].max()))
    sm_blue._A = []
    sm_red._A = []
    fig = plt.gcf()
    cax1 = fig.add_axes([0.8, 0.1, 0.03, 0.8])
    sm_blue = plt.cm.ScalarMappable(cmap='Blues', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                                 vmax=df_filtered['instance'].max()))
    sm_blue._A = []
    plt.colorbar(sm_blue, cax=cax1, label='Instance Number (Classical Domains)')
    cax2 = fig.add_axes([0.87, 0.1, 0.03, 0.8])
    sm_red = plt.cm.ScalarMappable(cmap='Reds', norm=Normalize(vmin=df_filtered['instance'].min(),
                                                               vmax=df_filtered['instance'].max()))
    sm_red._A = []
    plt.colorbar(sm_red, cax=cax2, label='Instance Number (Numerical Domains)')

    plt.tight_layout()
    plt.show()


'''
    Compares the PAR-N times in a bar chart for a specified domain (Where N*timeout is added for each instance not 
    solved)
'''
def compare_pars(df, domain, max_instance, timeout, par):
    df = df[df['domain'] == domain]
    timeout_penalty = timeout * par
    total_times = {}

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        total_time = 0
        for time in planner_data['planning_time']:
            total_time += time
        for i in range(len(planner_data), max_instance):
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

'''
    Cactus plot of every instance for all domains for overall comparison
'''
def cactus_all(df, log, total_instances, timeout, par):
    timeout_penalty = timeout * par
    plt.figure(figsize=(16, 8))
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
        plt.plot(x_values, times, label=planner_tag, c=color_map[planner_tag],  marker='o', markersize=6, linestyle='-', linewidth=2)

    plt.title(f'Time to Solve Instances for All Domains', fontsize=20)
    plt.xlabel('Number of Instances Solved', fontsize=18)
    plt.ylabel('Planning Time (minutes)', fontsize=18)
    plt.legend(loc='upper left', fontsize=16)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)
    plt.gca().set_aspect('auto')

    plt.tight_layout()
    plt.show()


'''
    PAR-N bar chart for all instances for final comparison and evaluation
'''
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
    colors = total_times_series.index.map(
        lambda x: 'orange' if '∀' in x else ('blue' if '∃' in x else 'steelblue')
    )
    plt.figure(figsize=(10, 8))
    ax = total_times_series.plot(kind='barh', color=colors, edgecolor='black')
    ax.set_title(f'Par {par} comparison for {timeout}m Time Limit on {total_instances} Instances', fontsize=16, fontweight='bold',
                 pad=20)
    ax.set_xlabel('Total Planning Time (minutes)', fontsize=14, labelpad=10)
    ax.set_ylabel('Approach', fontsize=14, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for i, (value, label) in enumerate(zip(total_times_series, total_times_series.index)):
        ax.text(value + max(total_times_series) * 0.01, i, f'{value:.2f}', ha='left', va='center', fontsize=10,
                color='black')
    ax.set_xlim([0, max(total_times_series) * 1.1])
    legend_handles = [
        mpatches.Patch(color='orange', label='∀-Step'),
        mpatches.Patch(color='blue', label='∃-Step'),
    ]
    plt.legend(handles=legend_handles, fontsize=12)
    plt.grid(visible=True, which='both', axis='x', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


'''
    Bar chart showing the ratio of PAR-N times of two instances, including a dotted line to show where the bar should
     be if the times are even
'''
def compare_domains(df, p1, p2, timeout, par):
    df = df[~df['domain'].str.contains("sailing", na=False)]
    timeout_penalty = timeout * par
    df = df[df['planner_tag'].isin([p1, p2])]
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
    colors = ['blue' if domain in cls_domains else 'red' for domain in domains]
    plt.figure(figsize=(12, 8))
    plt.barh(domains, ratios, color=colors, edgecolor='black')
    plt.axvline(1, color='red', linestyle='--', label='Equal Performance (Ratio = 1)')
    plt.xlabel(f'PAR-2 Time Ratio ({p1}/{p2})', fontsize=14)
    plt.ylabel('Domain', fontsize=14)
    plt.title(f'Comparison of {p1} and {p2} Across Domains', fontsize=16)
    legend_handles = [
        mpatches.Patch(color='blue', label='Classical Domain'),
        mpatches.Patch(color='red', label='Numeric Domain'),
        Line2D([0], [0], color='red', linestyle='--', label='Equal Performance (Ratio = 1)')
    ]
    plt.legend(handles=legend_handles, fontsize=12)
    plt.tight_layout()
    plt.show()


'''
    Helper function that only includes relevant approaches to allow for fine-grained comparison images in the report
'''
def include_data(df, planner):
    return df[df['planner_tag'].isin(planner)]


'''
    Helper function that replaces the shortened planner tag string with a name matching the section in the report for easy
    comparison
'''
def replace_names(df):
    df['planner_tag'] = df['planner_tag'].replace('forall-noprop', 'Eager ∀ (No Propagator)')
    df['planner_tag'] = df['planner_tag'].replace('forall', 'Eager ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-lazy', 'Naive Lazy ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-code', 'Code-Optimised Lazy ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-final', 'Generate & Test ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-stepshare', 'Stepsharing ∀')
    # df['planner_tag'] = df['planner_tag'].replace('forall-prop', 'Neighbours ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-prop', 'Lazy ∀')
    df['planner_tag'] = df['planner_tag'].replace('forall-decide', 'Decide ∀')

    df['planner_tag'] = df['planner_tag'].replace('exists-noprop', 'Eager ∃ (No Propagator)')
    df['planner_tag'] = df['planner_tag'].replace('exists', 'Eager ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-lazy', 'Naive Lazy ∃')
    # df['planner_tag'] = df['planner_tag'].replace('exists-code', 'Code-Optimised Lazy ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-code', 'Lazy ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-final', 'Generate & Test ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-stepshare', 'Stepsharing ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-prop', 'Ghost Node ∃')
    df['planner_tag'] = df['planner_tag'].replace('exists-decide', 'Decide ∃')
    return df


'''
    Helper funciton to find the total number of instances solvable (set union of all approaches). This gives us a 
    value for total instances in PAR-N calculations
'''
def number_of_instances(df):
    unique_instances_count = df.groupby(['domain', 'instance']).ngroups
    print("No. unique instances:", unique_instances_count)
    return unique_instances_count


def display_data(df):
    df = include_data(df, ['forall-decide', 'exists-decide', 'exists-code', 'forall-code'])
    df = replace_names(df)
    total_instances_count = number_of_instances(df)
    df['planning_time'] = df['planning_time'] / 60 # Convert time to minutes from seconds
    # scatter_plot(df, True, "Lazy ∃-Step","Eager ∃-Step", 30)
    # scatter_plot(df, True, "Lazy ∀-Step","Eager ∀-Step", 30)
    # cactus_plot(df, "rovers", False,  18, 30, 1)
    # cactus_grid(df, ["elevators", "miconic", "sugar", "tsp"], False,   30, 1)
    # compare_pars(df, "rovers", 20, 30, 2)
    cactus_all(df, False, total_instances_count, 30, 1)
    # par_all(df, 649, 30, 2)
    # compare_domains(df,  "Eager ∀", "Eager ∃",30, 2)




df =  pd.read_csv(folder_path)
df['domain'] = df['domain'].str.replace(r'sec_clear_\d+_\d+-linear', 'sec_clearance', regex=True)

display_data(df)



