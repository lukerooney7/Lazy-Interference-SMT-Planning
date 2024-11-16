import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("graph_properties.csv")

def plot_density():
    plt.figure(figsize=(12, 6), dpi=300)
    prop_cycler = plt.rcParams['axes.prop_cycle']
    colors = prop_cycler.by_key()['color']

    ax1 = plt.gca()

    for i, (domain_name, domain_df) in enumerate(df.groupby("domain")):
        color = colors[i % len(colors)]
        ax1.plot(
            domain_df["instance"],
            domain_df["Graph density"],
            marker="o",
            linestyle="-",
            color=color,
            label=f"{domain_name} - Density"
        )

    ax1.set_title("Instance Number vs Graph Density and Number of Edges", fontsize=14, weight="bold")
    ax1.set_xlabel("Instance Number", fontsize=12)
    ax1.set_ylabel("Graph Density", fontsize=12)
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.7)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(
        lines1,
        labels1,
        loc="upper center",
        fontsize="small",
        bbox_to_anchor=(0.5, -0.15),
        ncol=2,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0.1, 1, 1])
    plt.show()


def plot_num_edges():
    plt.figure(figsize=(12, 6), dpi=300)
    prop_cycler = plt.rcParams['axes.prop_cycle']
    colors = prop_cycler.by_key()['color']

    ax1 = plt.gca()

    for i, (domain_name, domain_df) in enumerate(df.groupby("domain")):
        color = colors[i % len(colors)]
        ax1.plot(
            domain_df["instance"],
            domain_df["Number of edges"],
            marker="o",
            linestyle="-",
            color=color,
            label=f"{domain_name} - Density"
        )

    ax1.set_title("Instance Number vs Number of Edges", fontsize=14, weight="bold")
    ax1.set_xlabel("Instance Number", fontsize=12)
    ax1.set_ylabel("Number of Edges", fontsize=12)
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.7)

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(
        lines1,
        labels1,
        loc="upper center",
        fontsize="small",
        bbox_to_anchor=(0.5, -0.15),
        ncol=2,
        frameon=False
    )
    plt.yscale('log')

    plt.tight_layout(rect=[0, 0.1, 1, 1])
    plt.show()

def plot():
    plt.figure(figsize=(12, 8))
    melted_df = df.melt(id_vars=["Domain", "Instance"],
                        value_vars=["Number of nodes", "Number of edges", "Graph density", "Highest degree"],
                        var_name="Metric", value_name="Value")

    sns.barplot(data=melted_df, x="Instance", y="Value", hue="Domain", ci=None, palette="viridis")
    plt.title("Comparison of Metrics Across Domains and Instances")
    plt.xlabel("Instance Number")
    plt.ylabel("Metric Value")
    plt.yscale('log')
    plt.legend(title="Domain")
    plt.show()



# plot_density()
plot_num_edges()
# plot()
# mann_whitney()