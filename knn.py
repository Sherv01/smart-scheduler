import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load data
csv_file = "C:/Users/Sherv/Desktop/Coding Portfolio/Calendar Project/V2/scheduled_activities_train.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file)

def preprocess_data(data):
    """Preprocess the data for KNN."""
    # Encode the activity names and categories as numeric labels
    le_activity = LabelEncoder()
    le_category = LabelEncoder()

    data['Activity_Label'] = le_activity.fit_transform(data['Activity'])
    data['Category_Label'] = le_category.fit_transform(data['Category'])

    return data, le_activity, le_category

def train_category_specific_knn(data, category, n_neighbors=3):
    """Train a KNN model using only data for the specified category."""
    # Filter data for the given category
    category_data = data[data['Category'] == category]

    # Select features (Start_Time) and target (Activity_Label)
    X = category_data[['Start_Time']]
    y = category_data['Activity_Label']

    # Split into training and test sets for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train KNN model
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)

    # Evaluate accuracy on the test set
    accuracy = knn.score(X_test, y_test)
    print(f"KNN Model for category '{category}' trained with accuracy: {accuracy:.2f}")

    return knn

def predict_activity(knn, le_activity, start_time):
    """Predict the activity based on start time."""
    # Prepare the input for prediction
    input_data = np.array([[start_time]])

    # Predict the activity label
    activity_label = knn.predict(input_data)[0]

    # Decode the activity label to the activity name
    predicted_activity = le_activity.inverse_transform([activity_label])[0]

    return predicted_activity


# # Preprocess the data
# data, le_activity, le_category = preprocess_data(data)

# # Example: Predict an activity
# example_start_time = 9  # Replace with actual start time
# example_category = "Academic"  # Replace with actual category

# # Train a category-specific KNN model
# knn_model = train_category_specific_knn(data, example_category, n_neighbors=3)

# # Predict activity for the specified category
# predicted_activity = predict_activity(knn_model, le_activity, example_start_time)

# print(f"Predicted activity for start time {example_start_time} and category '{example_category}': {predicted_activity}")
