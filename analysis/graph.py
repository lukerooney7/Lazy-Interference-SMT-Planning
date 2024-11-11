import os
import json
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

# folder_path = '/Users/lukeroooney/Desktop/Dissertation/parallelSAT/dump_results'
folder_path = '/Users/lukeroooney/developer/pyPMTEvalToolkit/sandbox-dir/dump_results'

def get_data():
    data_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as f:
                json_data = json.load(f)

                task_info = json_data.get('task-info', {})
                planner_info = json_data.get('planner-info', {})
                task_result = json_data.get('task-result', {})
                domain = task_info.get('domain')
                instance = task_info.get('instance')
                planner_tag = planner_info.get('planner-tag')


                timings = task_result.get('timings', {})
                pddl_parse_time = timings.get('pddl-parse-time')
                planning_time = timings.get('planning-time')

                summary = task_result.get('summary', {})
                status = summary.get('status')

                data_list.append({
                    'domain': domain,
                    'instance': instance,
                    'planner_tag': planner_tag,
                    'pddl_parse_time': pddl_parse_time,
                    'planning_time': planning_time,
                    'status': status,
                })

    df = pd.DataFrame(data_list)
    df.sort_values(by='instance', inplace=True)
    return df


def cactus_plot(df, domain, encoding, log, min_instance, max_instance, timeout, par):
    df = df[df['domain'] == domain]
    timeout_penalty = timeout * 60 * par
    # df = df[df['planner_tag'].str.contains(encoding, na=False)]
    df = df[df['status'] == "SOLVED_SATISFICING"]
    df = df[(df['instance'] >= min_instance) & (df['instance'] <= max_instance)]


    plt.figure(figsize=(12, 8))
    plt.hlines(timeout_penalty, xmin=1, xmax=max_instance, colors='red', linestyles='--', label='Timeout Threshold', linewidth=2)

    if log:
        plt.yscale('log')

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        instances = []
        times = []
        for instance in range(1, max_instance + 1):
            if instance in planner_data['instance'].values:
                time = planner_data.loc[planner_data['instance'] == instance, 'planning_time'].values[0]
            else:
                time = timeout_penalty

            instances.append(instance)
            times.append(time)
        plt.plot(instances, times, label=planner_tag, marker='o', markersize=8, linestyle='-', linewidth=2)

    plt.title(f'Planning Time Comparison for {domain} Domain Encodings', fontsize=18)
    plt.xlabel('Instance', fontsize=14)
    plt.ylabel('Planning Time (s)', fontsize=14)
    plt.legend(title='Planner Tag', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
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
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'X']  # Extend if needed
    domain_marker_map = {domain: markers[i % len(markers)] for i, domain in enumerate(unique_domains)}
    plt.figure(figsize=(12, 8))
    if log:
        plt.yscale('log')
        plt.xscale('log')
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
        # print(graph_data)
        plt.scatter(
            graph_data['x'], graph_data['y'],
            s=100, marker=domain_marker_map[domain], c=graph_data['c'],
            edgecolor='black', alpha=0.7, label=domain
        )
    plt.title(f'Comparison of {x} and {y} Planning Times', fontsize=16)
    plt.xlabel(f'{x} Planning Time (s)', fontsize=14)
    plt.ylabel(f'{y} Planning Time (s)', fontsize=14)
    plt.plot([0, timeout_penalty], [0, timeout_penalty], 'k-', linewidth=2, label='Equal Planning Time')
    plt.gca().set_aspect('equal', adjustable='box')
    custom_legend = [Line2D([0], [0], marker=marker, color='w', markerfacecolor='none',
                            markeredgecolor='black', markersize=10) for marker in markers]
    plt.legend(custom_legend, unique_domains, title='Domain', fontsize=12)
    plt.colorbar(label='Instance Number')
    plt.tight_layout()
    plt.show()


def compare_pars(df, domain, min_instance, max_instance, timeout, par):
    df = df[df['domain'] == domain]
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

    sns.set_theme(style="whitegrid")
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




def display_data(df):
    # scatter_plot(df, False,"forall-lazy-optimal", "test", 1,8, 3.5)
    cactus_plot(df, "rovers", "tsp", True, 0, 10, 2, 1)
    # compare_pars(df, "tsp",0, 10, 10, 2)

df = get_data()
display_data(df)