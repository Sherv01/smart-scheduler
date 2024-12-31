import pandas as pd
import kmc
import knn
import warnings

# Suppress the specific warning about feature names
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


def main():
    # Load the scheduled activities data
    csv_file = "C:/Users/Sherv/Desktop/Coding Portfolio/Calendar Project/V2/scheduled_activities_train.csv" # Replace with your CSV file path
    data = pd.read_csv(csv_file)
    csv_file_test = "C:/Users/Sherv/Desktop/Coding Portfolio/Calendar Project/V2/scheduled_activities.csv"
    data_test = pd.read_csv(csv_file_test)

    # Preprocess the data and initialize label encoders
    data, le_activity, le_category = knn.preprocess_data(data)

    # Train the KNN model for each category
    categories = data['Category'].unique()
    knn_models = {}
    for category in categories:
        print(f"\nTraining KNN model for category: {category}")
        knn_model = knn.train_category_specific_knn(data, category)
        knn_models[category] = knn_model

    # Perform K-Means clustering for each category and label clusters using KNN
    for category in categories:
        print(f"\nProcessing category: {category}")

        # Filter data for the current category
        filtered_data = kmc.filter_data_by_category(data, category)
        if filtered_data.empty:
            print(f"No data found for category '{category}'. Skipping...")
            continue

        filtered_data_test = kmc.filter_data_by_category(data_test, category)
        if filtered_data_test.empty:
            print(f"No data found for category '{category}'. Skipping...")
            continue

        # Generate elbow plot and determine suggested k
        suggested_k = kmc.generate_elbow_plot(filtered_data_test, category)
        print(f"Suggested k for category '{category}': {suggested_k}")

        # Perform K-Means clustering with the suggested k
        kmeans = kmc.KMeans(n_clusters=suggested_k, random_state=42)
        times = filtered_data_test['Start_Time'].values.reshape(-1, 1)
        kmeans.fit(times)
        labels = kmeans.labels_

        # Label the clusters using the KNN model
        knn_model = knn_models[category]
        clustered_data = filtered_data_test.copy()
        clustered_data['Cluster'] = labels
        cluster_labels = [
            knn.predict_activity(knn_model, le_activity, time[0])
            for time in times
        ]
        clustered_data['Cluster_Label'] = cluster_labels
        clustered_data['Cluster'] = clustered_data['Cluster'] + 1

        # Display results
        print(f"Cluster labels for category '{category}':")
        print(clustered_data[['Cluster', 'Cluster_Label']].drop_duplicates())

        # Plot clustered data
        kmc.plot_clusters_with_labels_and_clusters(filtered_data_test, clustered_data, labels, clustered_data['Cluster_Label'], category)

if __name__ == "__main__":
    main()
