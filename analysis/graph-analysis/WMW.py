import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import mannwhitneyu

from analysis.graph import get_data

df = pd.read_csv("graph_properties.csv")
plt.figure(figsize=(10, 6))

graph_properties = [
    "Number of edges",
    "Graph density",
]

folder_path = '/Users/lukeroooney/developer/pyPMTEvalToolkit/sandbox-dir/dump_results'

X = df[graph_properties].copy()

kmeans = KMeans(n_clusters=2)
df['Cluster'] = kmeans.fit_predict(X)
df['Cluster'] = df['planner-tag']

times_df = get_data(folder_path)
times_df = times_df.pivot_table(index=["instance", "domain"], columns="planner_tag", values="planning_time").reset_index()
times_df["delta"] = times_df["forall"] - times_df["forall-lazy-optimal"]
times_df = times_df[["instance", "domain", "delta"]]
merged_df = pd.merge(df, times_df, on=["instance", "domain"], how="inner")

results = []

for cluster_a in merged_df['Cluster'].unique():
    for cluster_b in merged_df['Cluster'].unique():
        if cluster_a < cluster_b:
            group_a = merged_df[merged_df['Cluster'] == cluster_a]['delta']
            group_b = merged_df[merged_df['Cluster'] == cluster_b]['delta']

            # Wilcoxon-Mann-Whitney test
            stat, p_value = mannwhitneyu(group_a, group_b, alternative='two-sided')
            results.append({
                'Cluster A': cluster_a,
                'Cluster B': cluster_b,
                'Statistic': stat,
                'P-Value': p_value
            })

results_df = pd.DataFrame(results)
print(results_df)
significant_results = results_df[results_df['P-Value'] < 0.05]
print("\nSignificant Results (p < 0.05):")
print(significant_results)
