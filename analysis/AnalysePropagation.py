import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a DataFrame
csv_file = "/Users/lukeroooney/Desktop/Dissertation/parallelSAT/analysis/stats.csv"  # Replace with your CSV file name
df = pd.read_csv(csv_file)





def show_propagations():
    # Filter data for a specific domain (e.g., 'rovers')
    domain = "rovers"
    domain_data = df[df['domain'] == domain]

    # Convert instance numbers to integers for sorting
    domain_data['instance'] = domain_data['instance'].astype(int)
    domain_data = domain_data.sort_values('instance')

    # Plot propagations against instance numbers
    plt.figure(figsize=(10, 6))
    plt.plot(domain_data['instance'], domain_data['propagations'], marker='o', label='Propagations')
    plt.plot(domain_data['instance'], domain_data['conflicts'], marker='o', label='Conflicts')
    plt.plot(domain_data['instance'], domain_data['decisions'], marker='o', label='Decisions')

    # Adding labels and title
    plt.xlabel("Instance Number", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.yscale('log')
    plt.title(f"Analysis of Domain '{domain}'", fontsize=14)
    plt.legend()
    plt.grid(True)

    # Save or display the plot
    plt.tight_layout()
    plt.show()

def show_mutexes(df):
    df['mutexes'] = pd.to_numeric(df['mutexes'])
    df_forall = df[df['propagator'] == 'forall']
    df_lazy_optimal = df[df['propagator'] == 'forall-lazy']

    # Merge the two DataFrames on 'instance'
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



show_mutexes(df)

