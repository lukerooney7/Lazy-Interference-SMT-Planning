import json
import os

import pandas as pd

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

folder = "/Users/lukeroooney/Desktop/saved-data/raw-results/numeric-comparison"
df = get_data(folder)

df.to_csv("/Users/lukeroooney/Desktop/saved-data/solve-data/numeric-comparison.csv", index=False)