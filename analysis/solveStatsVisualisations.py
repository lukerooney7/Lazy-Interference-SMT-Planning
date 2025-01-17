import pandas as pd
from matplotlib import pyplot as plt

csv_file = "../pypmt/stats.csv"
csv_df = pd.read_csv(csv_file)

domains = ['briefcase', 'truck', 'mprime', 'ztravel', 'dlog', 'pathways', 'rover', 'tsp', 'pegsolitaire', 'movie', 'psr', 'gripper']

color_map = {
    'Eager ∀ (No Propagator)': 'grey',
    'Eager ∀': 'orange',
    'Naive Lazy ∀': 'purple',
    'Code-Optimised Lazy ∀': 'purple',
    'Generate & Test ∀': 'brown',
    'Stepsharing ∀': 'red',
    'Neighbours ∀': 'red',
    'Lazy ∀': 'red',
    'Decide ∀': 'red',
    'Eager ∃ (No Propagator)': 'black',
    'Eager ∃': 'blue',
    'Naive Lazy ∃': 'gold',
    'Code-Optimised Lazy ∃': 'gold',
    'Lazy ∃': 'green',
    'Generate & Test ∃': 'green',
    'Stepsharing ∃': 'purple',
    'Ghost Node ∃': 'purple',
    'Decide ∃': 'purple',
}


def replace_names(df):
    df = df.copy()  # To ensure we are working with a copy, not a view.

    df.loc[df['planner_tag'] == 'forall-noprop', 'planner_tag'] = 'Eager ∀ (No Propagator)'
    df.loc[df['planner_tag'] == 'forall', 'planner_tag'] = 'Eager ∀'
    df.loc[df['planner_tag'] == 'forall-lazy', 'planner_tag'] = 'Naive Lazy ∀'
    df.loc[df['planner_tag'] == 'forall-code', 'planner_tag'] = 'Code-Optimised Lazy ∀'
    df.loc[df['planner_tag'] == 'forall-final', 'planner_tag'] = 'Generate & Test ∀'
    df.loc[df['planner_tag'] == 'forall-stepshare', 'planner_tag'] = 'Stepsharing ∀'
    df.loc[df['planner_tag'] == 'forall-prop', 'planner_tag'] = 'Neighbours ∀'
    # df.loc[df['planner_tag'] == 'forall-prop', 'planner_tag'] = 'Lazy ∀'
    df.loc[df['planner_tag'] == 'forall-decide', 'planner_tag'] = 'Decide ∀'

    df.loc[df['planner_tag'] == 'exists-noprop', 'planner_tag'] = 'Eager ∃ (No Propagator)'
    df.loc[df['planner_tag'] == 'exists', 'planner_tag'] = 'Eager ∃'
    df.loc[df['planner_tag'] == 'exists-lazy', 'planner_tag'] = 'Naive Lazy ∃'
    df.loc[df['planner_tag'] == 'exists-code', 'planner_tag'] = 'Code-Optimised Lazy ∃'
    # df.loc[df['planner_tag'] == 'exists-code', 'planner_tag'] = 'Lazy ∃'
    df.loc[df['planner_tag'] == 'exists-final', 'planner_tag'] = 'Generate & Test ∃'
    df.loc[df['planner_tag'] == 'exists-stepshare', 'planner_tag'] = 'Stepsharing ∃'
    df.loc[df['planner_tag'] == 'exists-prop', 'planner_tag'] = 'Ghost Node ∃'
    df.loc[df['planner_tag'] == 'exists-decide', 'planner_tag'] = 'Decide ∃'

    return df

def domain_names(df):
    for d in domains:
        df['problem'] = df['problem'].apply(lambda x: d if d in x else x)

    return df

def filter_complete_propagator_entries(df):
    all_propagators = df['planner_tag'].unique()
    valid_problems = (
        df.groupby('problem')['planner_tag']
        .apply(lambda x: set(all_propagators).issubset(set(x)))
    )
    valid_problem_names = valid_problems[valid_problems].index

    filtered_df = df[df['problem'].isin(valid_problem_names)]

    return filtered_df

def total_bar(df, property):
    result = df.groupby('planner_tag')[property].sum().sort_values(ascending=False)
    print(result)
    result.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f'Total number of  {property} by approach')
    plt.xlabel('Approach')
    plt.ylabel(f'Total {property}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def compare_bar(df, property_name, propagator_1, propagator_2, log_scale=False):

    df = domain_names(df)
    df_filtered = df[df['planner_tag'].isin([propagator_1, propagator_2])]
    aggregated_data = df_filtered.groupby(['problem', 'planner_tag'], as_index=False)[property_name].sum()
    pivot_data = aggregated_data.pivot(index='problem', columns='planner_tag', values=property_name)
    planner_colors = [color_map[propagator_1], color_map[propagator_2]]
    plt.figure(figsize=(12, 6))
    pivot_data.plot(kind='bar', stacked=False, color=planner_colors, width=0.8)

    # log if neeeded
    if log_scale:
        plt.yscale('log')
    plt.title(f'Comparison of {property_name.capitalize()} Between Propagators', fontsize=14, fontweight='bold')
    plt.xlabel('Sample Domain', fontsize=12)
    plt.ylabel(f'Total {property_name.capitalize()}', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.legend(title='Approach', loc='upper left', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def include_data(df, planner):
    return df[df['planner_tag'].isin(planner)]


csv_df.rename(columns={'propagator': 'planner_tag'}, inplace=True)

# csv_df = csv_df[csv_df['problem']]
filtered_df = csv_df[~csv_df['problem'].str.contains("gripper-x-1", na=False)]
csv_df = csv_df[csv_df['problem'].str.contains('|'.join(domains))]
df_filtered = filter_complete_propagator_entries(csv_df)

df_filtered = replace_names(df_filtered)
# df_filtered = include_data(df_filtered, ['Decide ∀', 'Code-Optimised Lazy ∀', 'Decide ∃', 'Code-Optimised Lazy ∃'])
total_bar(df_filtered, 'conflicts')

compare_bar(df_filtered, 'conflicts',   'Ghost Node ∃','Code-Optimised Lazy ∃', True)
