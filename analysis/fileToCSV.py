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



def file_to_csv():
    folder = "/Users/lukeroooney/Desktop/Dissertation/data/dump_files/stepshare2"
    df = get_data(folder)

    df.to_csv("/Users/lukeroooney/Desktop/Dissertation/data/csvs/stepshare2.csv", index=False)
    print('created CSV')


def combine_csvs():
    folder_path = "/Users/lukeroooney/Desktop/Dissertation/data/csvs"
    dfs = []

    for file_name in os.listdir(folder_path):
        if file_name == "stepshare.csv":
            continue
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)

            # if 'classical' in file_name:
            #     suffix = '_cls'
            # elif 'numeric' in file_name:
            #     suffix = '_num'
            # else:
            #     continue
            # df['domain'] = df['domain'] + suffix
            dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv("/Users/lukeroooney/Desktop/Dissertation/data/csvs/all.csv", index=False)

# file_to_csv()
combine_csvs()