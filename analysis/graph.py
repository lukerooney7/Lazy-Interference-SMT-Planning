import os
import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

# folder_path = '/Users/lukeroooney/developer/pyPMTEvalToolkit/sandbox-dir/dump_results'
folder_path = '/Users/lukeroooney/Desktop/Dissertation/parallelSAT/dump_results'
classical_domains = {"rovers", "tpp-numeric", "tsp", "trucks", "depot", "tpp", "satellite"}
numerical_domains = {"zenotravel", "satellites", "tpp-numeric-numeric", "markettrader", "counters"}

def get_data(folder_path):
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
    plt.hlines(timeout_penalty, xmin=min_instance, xmax=max_instance, colors='red', linestyles='--', label='Timeout Threshold', linewidth=2)

    if log:
        plt.yscale('log')

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        instances = []
        times = []
        for instance in range(min_instance, max_instance + 1):
            if instance in planner_data['instance'].values:
                time = planner_data.loc[planner_data['instance'] == instance, 'planning_time'].values[0]
            else:
                time = timeout_penalty

            instances.append(instance)
            times.append(time)
        times.sort()
        x_values = list(range(1, len(times) + 1))
        plt.plot(x_values, times, label=planner_tag, marker='o', markersize=6, linestyle='-', linewidth=2)

    plt.title(f'Planning Time Comparison for {domain} Domain Encodings', fontsize=18)
    plt.xlabel('Number of Instances Solved', fontsize=14)
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
    sm_blue._A = []  # Dummy array for colorbar
    sm_red._A = []  # Dummy array for colorbar
    fig = plt.gcf()
    plt.colorbar(sm_blue, ax=fig.gca(),label='Instance Number (Classical Domains)')
    # plt.colorbar(sm_red, ax=fig.gca(),label='Instance Number (Numerical Domains)')

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
    timeout_penalty = timeout * 60 * par
    df = df[df['status'] == "SOLVED_SATISFICING"]
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
    plt.ylabel('Planning Time (s)', fontsize=14)
    plt.legend(title='Planner Tag', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('auto')
    plt.tight_layout()
    plt.show()


def display_data(df):
    # scatter_plot(df, True, "forall-lazy-optimal","test", 1,10, 5)
    # cactus_plot(df, "tpp", "tsp", True, 1, 20, 30, 1)
    # compare_pars(df, "rovers",0, 20, 30, 2)
    cactus_all(df, True, 85, 30, 1)


df = get_data(folder_path)
df = df[(df['planner_tag'] != "exists-noprop") & (df['planner_tag'] != "exists")]
display_data(df)