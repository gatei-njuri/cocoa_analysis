import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def process_countries_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    country_df = df[df["Area"] == country]
    country_df = country_df[["Year","Element","Value"]]
    pivot_df = country_df.pivot_table(
        index="Year",
        columns="Element",
        values="Value",
        aggfunc="first"
    ).reset_index()

    pivot_df = pivot_df.rename(columns={
        "Area harvested": "Area harvested",
        "Yield": "Yield",
        "Production": "Production"
    })

    cols = ["Year", "Area harvested", "Yield", "Production"]
    existing = [c for c in cols if c in pivot_df.columns]
    return pivot_df[existing]

def save_table(df: pd.DataFrame, output_dir: str, filename: str):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False)

def clean_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)

    for col in ['Area harvested', 'Yield', 'Production']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.sort_values('Year').reset_index(drop=True)
    return df

def plot_scatter(df: pd.DataFrame, country_name: str, output_dir: str, filename: str,
                 color: str = 'tab:green', marker_size: int = 40):
    os.makedirs(output_dir, exist_ok=True)
    if 'Yield' not in df.columns:
        print(f"Warning: 'Yield' column not found for {country_name}. Skipping scatter plot.")
        return

    df_plot = df.dropna(subset=['Yield'])
    if df_plot.empty:
        print(f"Warning: No valid Yield values for {country_name}. Skipping scatter plot.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df_plot['Year'], df_plot['Yield'], s=marker_size, color=color, edgecolor='k', alpha=0.8)
    ax.set_title(f"{country_name} — Yield by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Yield")
    ax.grid(True, linestyle='--', alpha=0.4)

    out_path = os.path.join(output_dir, filename)
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved scatter plot for {country_name}: {out_path}")

def plot_bar(df: pd.DataFrame, country_name: str, output_dir: str, filename: str,
             color: str = 'tab:blue'):
    os.makedirs(output_dir, exist_ok=True)
    if 'Area harvested' not in df.columns:
        print(f"Warning: 'Area harvested' column not found for {country_name}. Skipping bar chart.")
        return

    df_plot = df.dropna(subset=['Area harvested'])
    if df_plot.empty:
        print(f"Warning: No valid Area harvested values for {country_name}. Skipping bar chart.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df_plot['Year'], df_plot['Area harvested'], color=color, alpha=0.7, edgecolor='k')
    ax.set_title(f"{country_name} — Area harvested by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Area harvested")
    ax.grid(True, linestyle='--', axis='y', alpha=0.4)

    out_path = os.path.join(output_dir, filename)
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved bar chart for {country_name}: {out_path}")

def plot_combined(ghana_df: pd.DataFrame, coast_df: pd.DataFrame, output_dir: str, filename: str):
    
    os.makedirs(output_dir, exist_ok=True)

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Ghana scatter
    g_scatter = ghana_df.dropna(subset=['Yield'])
    axs[0, 0].scatter(g_scatter['Year'], g_scatter['Yield'],
                      color='seagreen', edgecolor='black', alpha=0.8, s=60)
    axs[0, 0].set_title("Ghana — Yield by Year", fontsize=12, fontweight="bold")
    axs[0, 0].set_xlabel("Year", fontsize=10)
    axs[0, 0].set_ylabel("Yield (hg/ha)", fontsize=10)
    axs[0, 0].grid(True, linestyle='--', alpha=0.4)

    # Côte d'Ivoire scatter
    c_scatter = coast_df.dropna(subset=['Yield'])
    axs[0, 1].scatter(c_scatter['Year'], c_scatter['Yield'],
                      color='darkorange', edgecolor='black', alpha=0.8, s=60)
    axs[0, 1].set_title("Côte d'Ivoire — Yield by Year", fontsize=12, fontweight="bold")
    axs[0, 1].set_xlabel("Year", fontsize=10)
    axs[0, 1].set_ylabel("Yield (hg/ha)", fontsize=10)
    axs[0, 1].grid(True, linestyle='--', alpha=0.4)

    # Ghana bar
    g_bar = ghana_df.dropna(subset=['Area harvested'])
    axs[1, 0].bar(g_bar['Year'], g_bar['Area harvested'],
                  color='royalblue', alpha=0.7, edgecolor='black')
    axs[1, 0].set_title("Ghana — Area harvested by Year", fontsize=12, fontweight="bold")
    axs[1, 0].set_xlabel("Year", fontsize=10)
    axs[1, 0].set_ylabel("Area harvested (ha)", fontsize=10)
    axs[1, 0].grid(True, linestyle='--', axis='y', alpha=0.4)

    # Côte d'Ivoire bar
    c_bar = coast_df.dropna(subset=['Area harvested'])
    axs[1, 1].bar(c_bar['Year'], c_bar['Area harvested'],
                  color='firebrick', alpha=0.7, edgecolor='black')
    axs[1, 1].set_title("Côte d'Ivoire — Area harvested by Year", fontsize=12, fontweight="bold")
    axs[1, 1].set_xlabel("Year", fontsize=10)
    axs[1, 1].set_ylabel("Area harvested (ha)", fontsize=10)
    axs[1, 1].grid(True, linestyle='--', axis='y', alpha=0.4)

    # Overall title
    fig.suptitle("Cocoa Production in Ghana and Côte d'Ivoire (1961–2022)",
                 fontsize=16, fontweight='bold')

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = os.path.join(output_dir, filename)
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved combined plot with annotations: {out_path}")


def main():
    parser = argparse.ArgumentParser(description ="Cocoa production data processor")
    parser.add_argument("file", help ="Path to csv file")
    parser.add_argument("-o", "--output", default="output", help ="Output directory for results")
    args = parser.parse_args()

    df = load_data(args.file)

    # Ghana
    ghana_table = process_countries_data(df, "Ghana")
    ghana_table = clean_and_sort(ghana_table)
    save_table(ghana_table, args.output, "ghana_table.csv")
    plot_scatter(ghana_table, "Ghana", args.output, "ghana_yield_scatter.png", color='tab:green')
    plot_bar(ghana_table, "Ghana", args.output, "ghana_area_bar.png", color='tab:blue')

    # Côte d'Ivoire
    coast_table = process_countries_data(df, "Côte d'Ivoire")
    coast_table = clean_and_sort(coast_table)
    save_table(coast_table, args.output, "coast_table.csv")
    plot_scatter(coast_table, "Côte d'Ivoire", args.output, "coast_yield_scatter.png", color='tab:orange')
    plot_bar(coast_table, "Côte d'Ivoire", args.output, "coast_area_bar.png", color='tab:red')

    # Combined multi-panel PDF
    plot_combined(ghana_table, coast_table, args.output, "combined_plots.pdf")

    print("All outputs saved in:", args.output)

if __name__ == "__main__":
    main()
