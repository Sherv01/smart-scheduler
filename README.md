# Smart Scheduler

**Smart Scheduler** is an intelligent scheduling tool that combines calendar parsing, K-Nearest Neighbors (KNN), and K-Means Clustering to help users manage their activities efficiently. It leverages machine learning to predict the best time slots for user-specified activities, ensuring productivity and balanced time management.

## Features
- **Dynamic Scheduling**: Parse `.ics` calendar files and determine free time slots.
- **Machine Learning Integration**: Utilize KNN and K-Means Clustering to predict and categorize activities.
- **Interactive Interface**: Schedule, queue, and confirm activities via a user-friendly command-line menu.
- **Customizable Categories**: Predefined categories and activities for easy selection.
- **ICS File Update**: Generate updated `.ics` files with newly scheduled activities.

## Technologies Used
- **Python**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: KNN and K-Means Clustering implementation.
- **ICS Library**: Parsing and generating `.ics` calendar files.

## Installation
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure you have sample `.ics` files and activity datasets in `.csv` format.

## Usage
1. Run the main script:
   ```bash
   python main.py
   ```
   - You can also run the ML script to see the K-Means Clustering model working alongside the KNN model
     ```bash
     python ML.py
     ```
2. Follow the on-screen instructions to:
   - Schedule new activities.
   - Remove queued tasks.
   - Confirm scheduling and generate updated `.ics` files.
3. Use the generated `updated_calendar.ics` file with your preferred calendar application.

## Directory Structure
```
smart-scheduler/
│
├── main.py                     # Main application logic
├── knn.py                      # K-Nearest Neighbors implementation
├── kmc.py                      # K-Means Clustering module
├── calendar_processing.py      # Calendar parsing and free-time detection
├── data/                       # Sample datasets and training data, you must add this directory into parts of the code
├── updated_calendar.ics        # Generated calendar file
└── requirements.txt            # Project dependencies
```

## Key Components
### 1. **Calendar Processing**
- Parses `.ics` files to extract busy times and find free slots within user-defined active hours.

### 2. **KNN Prediction**
- Predicts suitable activities for free time slots based on historical data.

### 3. **K-Means Clustering**
- Groups activities into clusters and labels them using KNN for better categorization.

## Example Workflow
1. Load an existing `.ics` file.
2. Choose an activity category and specify the desired activity.
3. Select a suggested time slot based on predictions.
4. Confirm the schedule, and generate an updated `.ics` file.

## Future Enhancements
- Integrate K-Means Clustering Model into main program.
- Improve clustering accuracy using additional features.
- Add a graphical user interface (GUI) for better usability.
- Integrate cloud-based calendar services like Google Calendar.
