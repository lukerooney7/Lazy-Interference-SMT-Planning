import pandas as pd
import matplotlib.pyplot as plt

csv_file = "/cs/home/lr225/Documents/Lazy-Interference-SMT-Planning/stats.csv"
df = pd.read_csv(csv_file)





def show_propagations():
    # Filter data for a specific domain
    domain = "tpp"
    domain_data = df[df['domain'] == domain]

    # Convert instance numbers to integers for sorting
    domain_data['instance'] = domain_data['instance'].astype(int)
    domain_data = domain_data.sort_values('instance')
    plt.figure(figsize=(10, 6))
    for propagator, group_data in domain_data.groupby('propagator'):
        if "forall" in propagator:
            # Plot propagations against instance numbers
            plt.plot(group_data['instance'], group_data['propagations'], marker='o', label=f"{propagator} Propagations")
            # plt.plot(group_data['instance'], group_data['conflicts'], marker='o', label=f"{propagator} Conflicts")

            # plt.plot(group_data['instance'], group_data['decisions'], marker='o', label=f"{propagator} Decisions")

            # plt.plot(domain_data['instance'], domain_data['conflicts'], marker='o', label='Conflicts')
            # plt.plot(domain_data['instance'], domain_data['decisions'], marker='o', label='Decisions')

    # Adding labels and title
    plt.xlabel("Instance Number", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    # plt.yscale('log')
    plt.title(f"Number of Propagations of Domain '{domain}'", fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def show_mutexes(df):
    df['mutexes'] = pd.to_numeric(df['mutexes'])
    df_forall = df[df['propagator'] == 'forall']
    df_lazy_optimal = df[df['propagator'] == 'forall-lazy']

    merged_df = pd.merge(df_forall, df_lazy_optimal, on='instance', suffixes=('_forall', '_lazy'))
    merged_df = merged_df.sort_values(by='instance')
    # Calculate the ratio
    merged_df['mutex_ratio'] = merged_df['mutexes_lazy'] / merged_df['mutexes_forall']

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(merged_df['instance'], merged_df['mutex_ratio'], marker='o', label='Lazy Approach')
    plt.axhline(y=1, color='r', linestyle='--', label='Eager Approach')
    plt.xlabel('Instance')
    plt.ylabel('Ratio of Total Mutexes Used')
    plt.title('Ratio of Total Mutexes used Instance')
    plt.legend()
    plt.grid(True)
    plt.show()

def num_steps(df):
    grouped = df.groupby(['instance', 'propagator'])['steps'].sum().reset_index()
    pivoted = grouped.pivot(index='instance', columns='propagator', values='steps')
    pivoted.plot(kind='bar', figsize=(12, 6), width=0.8)

    # Customize the plot
    plt.title('Number of Steps for Each Propagator by Instance')
    plt.xlabel('Instance')
    plt.ylabel('Steps')
    plt.legend(title='Propagator')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def parallelism(df):
    df['length_to_steps_ratio'] = df['length'] / df['steps']

    # Group by instance and propagator
    grouped = df.groupby(['instance', 'propagator'])['length_to_steps_ratio'].mean().reset_index()

    # Pivot the table to have propagators as columns for easier plotting
    pivoted = grouped.pivot(index='instance', columns='propagator', values='length_to_steps_ratio')

    # Plot the data as a grouped bar chart
    pivoted.plot(kind='bar', figsize=(12, 6), width=0.8)

    # Customize the plot
    plt.title('Parallelism of Propagators for Rovers Domain')
    plt.xlabel('Instance')
    plt.ylabel('Actions per Step')
    plt.legend(title='Propagator')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot
    plt.show()



# num_steps(df)
# show_mutexes(df)
# parallelism(df)
show_propagations()
