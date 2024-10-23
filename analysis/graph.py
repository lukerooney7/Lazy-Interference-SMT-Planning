import os
import json
import pandas as pd
from matplotlib import pyplot as plt

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


def cactus_plot(df, domain, encoding, log, min_instance, max_instance):
    df = df[df['domain'] == domain]
    # df = df[df['planner_tag'].str.contains(encoding, na=False)]
    df = df[df['status'] == "SOLVED_SATISFICING"]

    # Filter the instances between min_instance and max_instance
    df = df[(df['instance'] >= min_instance) & (df['instance'] <= max_instance)]

    plt.figure(figsize=(12, 8))

    if log:
        plt.yscale('log')

    for planner_tag in df['planner_tag'].unique():
        planner_data = df[df['planner_tag'] == planner_tag]
        plt.plot(planner_data['instance'], planner_data['planning_time'],
                 label=planner_tag, marker='o', markersize=8, linestyle='-', linewidth=2)

    plt.title(f'Planning Time Comparison for {domain} Domain Encodings', fontsize=18)
    plt.xlabel('Instance', fontsize=14)
    plt.ylabel('Planning Time (s)', fontsize=14)
    plt.legend(title='Planner Tag', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('auto')
    plt.tight_layout()
    plt.show()


def scatter_plot(df, domain, x, y):
    df = df[df['domain'] == domain]
    df_filtered = df[df['planner_tag'].isin([x, y])]

    df_pivot = df_filtered.pivot(index='instance', columns='planner_tag', values='planning_time').reset_index()

    plt.figure(figsize=(12, 8))
    plt.yscale('log')
    plt.xscale('log')
    plt.scatter(df_pivot[x], df_pivot[y], s=100, color='blue', edgecolor='black', alpha=0.7, marker='o')

    plt.title(f'Comparison of {x} and {y} Planning Times', fontsize=16)
    plt.xlabel(f'{x} Planning Time (s)', fontsize=14)
    plt.ylabel(f'{y} Planning Time (s)', fontsize=14)

    min_val = min(df_pivot[x].min(), df_pivot[y].min())
    max_val = max(df_pivot[x].max(), df_pivot[y].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k-', linewidth=2, label='Equal Planning Time')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend(fontsize=12)

    plt.tight_layout()
    plt.show()


df = get_data()
# scatter_plot(df, "rovers", "ForallSMT-tag", "LazyForallSMT-tag")
cactus_plot(df, "rovers", "exists", True, 0, 100)

