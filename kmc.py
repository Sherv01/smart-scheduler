import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator

# Load data
csv_file = "C:/Users/Sherv/Desktop/Coding Portfolio/Calendar Project/V2/scheduled_activities.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file)


def filter_data_by_category(data, category):
    """Filter data for a specific category."""
    filtered_data = data[data['Category'] == category]
    return filtered_data


def generate_elbow_plot(data, category):
    """Generate an elbow plot and category plot as subplots."""
    times = data['Start_Time'].values.reshape(-1, 1)
    distortions = []

    # Calculate distortions for k = 1 to 9
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(times)
        distortions.append(kmeans.inertia_)

    # Use the kneed library to find the elbow point
    kneedle = KneeLocator(range(1, 10), distortions, curve='convex', direction='decreasing')
    suggested_k = kneedle.knee

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [3, 1]})  # Adjust height ratios

    # Elbow plot (top)
    ax1.plot(range(1, 10), distortions, marker='o')
    ax1.set_title("Elbow Plot")
    ax1.set_xlabel("Number of Clusters (k)")
    ax1.set_ylabel("Distortion (Inertia)")
    ax1.axvline(x=suggested_k, color='red', linestyle='--', label=f"Suggested k: {suggested_k}")
    ax1.legend()

    # Category plot (bottom)
    ax2.scatter(data['Start_Time'], [category] * len(data), c='black', label='Raw Data', zorder=2)
    ax2.set_title(f"Raw Data for {category}")
    ax2.set_xlabel("Start Time")
    ax2.set_ylabel("Category")
    ax2.legend()
    ax2.grid(axis='y', zorder=0)

    plt.tight_layout()
    plt.show()

    return suggested_k


def plot_clusters_with_labels_and_clusters(raw_data, clustered_data, labels, cluster_labels, category):
    """Plot raw data, clustered data with correct clusters, and labeled clustered data."""
    plt.figure(figsize=(10, 8.5))

    # Plot raw data (subplot 1)
    plt.subplot(3, 1, 1)
    plt.scatter(raw_data['Start_Time'], [category] * len(raw_data), c='black', label='Raw Data', zorder=2)
    plt.title(f"Raw Data for {category}")
    plt.xlabel("Start Time")
    plt.ylabel("Category")
    plt.legend()
    plt.grid(axis='y', zorder=0)

    # Plot clustered data with the correct number of clusters (subplot 2)
    plt.subplot(3, 1, 2)

    # Plot clusters from K-Means (correct amount of clusters)
    for cluster_num in np.unique(labels):
        plt.scatter(clustered_data['Start_Time'][labels == cluster_num],
                    [category] * sum(labels == cluster_num),
                    label=f"Cluster {cluster_num + 1}", zorder=2)

    plt.title(f"Clustered Data for {category}")
    plt.xlabel("Start Time")
    plt.ylabel("Category")
    plt.legend()
    plt.grid(axis='y', zorder=0)

    # Plot labeled clustered data (subplot 3)
    plt.subplot(3, 1, 3)

    # Plot clusters using the custom labels
    unique_labels = np.unique(cluster_labels)
    for cluster_label in unique_labels:
        cluster_indices = cluster_labels == cluster_label
        plt.scatter(clustered_data['Start_Time'][cluster_indices],
                    [category] * sum(cluster_indices),
                    label=f"{cluster_label} Cluster", zorder=2)

    plt.title(f"Labeled Clustered Data for {category}")
    plt.xlabel("Start Time")
    plt.ylabel("Category")
    plt.legend()
    plt.grid(axis='y', zorder=0)

    plt.tight_layout()
    plt.show()


# # User Interaction
# print("Available Categories: Academic, Extracurricular, Social, Personal, Well-being, Work")
# category = input("Please enter a category to view results: ")

# if category not in ["Academic", "Extracurricular", "Social", "Personal", "Well-being", "Work"]:
#     print("Invalid category entered. Please restart the program and try again.")
# else:
#     filtered_data = filter_data_by_category(data, category)

#     if filtered_data.empty:
#         print(f"No data found for category '{category}'.")
#     else:
#         input("\n\nYou will now see the elbow plot, along with a plot of the data from the category you have selected.\n"
#               "The \"elbow\" is the point on the elbow plot where the changes become less significant.\n"
#               "Take note of the k-value (shown on the x-axis) at the elbow.\n"
#               "This number should be consistent with the amount of \"clusters\" you count in the plot of the data from your chosen category.\n"
#               "The computer will attempt to calculate the correct number of clusters and suggest a value. This is not always correct.\n"
#               "Please only use the suggested \"k\" value if you are having trouble with counting the amount of clusters\n"
#               "or can\'t visually identify the elbow on the elbow plot.\n"
#               "Press \"Enter\" to continue.\n\n")
#         print(f"Displaying raw data and elbow plot for {category}...")
#         suggested_k = generate_elbow_plot(filtered_data, category)

#         k = int(input(f"Based on the plots, enter the number of clusters (k) (recommended value is {suggested_k}): "))
#         kmeans = KMeans(n_clusters=k, random_state=42)
#         times = filtered_data['Start_Time'].values.reshape(-1, 1)
#         kmeans.fit(times)
#         labels = kmeans.labels_

#         clustered_data = filtered_data.copy()
#         clustered_data['Cluster'] = labels

#         print("Generating clustered data plot...")
#         plot_clusters(filtered_data, clustered_data, labels, category)