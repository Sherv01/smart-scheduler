import os
from datetime import datetime, timedelta
from calendar_processing import parse_ics_file, get_free_times, format_free_times
from knn import preprocess_data, train_category_specific_knn, predict_activity
# K Means Clustering Model not used yet
import pandas as pd
import warnings
from ics import Calendar, Event
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

def main():
    categories = { # Assume that the data is precategorized into these categories
        "Academic": [
            {"Activity": "Classes/Lectures", "Frequency": 0.34},
            {"Activity": "Study Sessions", "Frequency": 0.33},
            {"Activity": "Exams/Quizzes", "Frequency": 0.33}
        ],
        "Extracurricular": [
            {"Activity": "Sports Practices/Games", "Frequency": 0.33},
            {"Activity": "Club Meetings", "Frequency": 0.33},
            {"Activity": "Volunteer Activities", "Frequency": 0.34}
        ],
        "Social": [
            {"Activity": "Parties/Gatherings", "Frequency": 0.5},
            {"Activity": "Family Events", "Frequency": 0.5}
        ],
        "Personal": [
            {"Activity": "Doctor/Dentist Appointments", "Frequency": 0.33},
            {"Activity": "Errands/Chores", "Frequency": 0.34},
            {"Activity": "Birthdays/Anniversaries", "Frequency": 0.33}
        ],
        "Well-being": [
            {"Activity": "Exercise", "Frequency": 0.5},
            {"Activity": "Meditation/Yoga", "Frequency": 0.5}
        ],
        "Work": [
            {"Activity": "Part-time Job Shifts", "Frequency": 0.5},
            {"Activity": "Work Meetings", "Frequency": 0.5}
        ]
    }

    scheduled_tasks = []
    queued_tasks = []

    print("Welcome to the Smart Scheduler!")

    while True:
        print("\nMain Menu:")
        print("1. Schedule New Activity")
        print("2. Remove Queued Activity")
        print("3. Confirm Scheduling")
        print("4. Quit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Schedule New Activity
            print("Select a category:")
            for i, category in enumerate(categories.keys(), 1):
                print(f"{i}. {category}")

            category_choice = input("Enter the category number: ").strip()
            if not category_choice.isdigit() or int(category_choice) not in range(1, len(categories) + 1):
                print("Invalid choice. Returning to main menu.")
                continue

            selected_category = list(categories.keys())[int(category_choice) - 1]
            print(f"Selected Category: {selected_category}")

            print("Select an activity:")
            activities = categories[selected_category]
            for i, activity in enumerate(activities, 1):
                print(f"{i}. {activity['Activity']}")

            activity_choice = input("Enter the activity number: ").strip()
            if not activity_choice.isdigit() or int(activity_choice) not in range(1, len(activities) + 1):
                print("Invalid choice. Returning to main menu.")
                continue

            selected_activity = activities[int(activity_choice) - 1]["Activity"]
            print(f"Selected Activity: {selected_activity}")

            # Load calendar data
            ics_path = input("Enter the path to your .ics file: ").strip()
            if not os.path.exists(ics_path):
                print("File not found. Returning to main menu.")
                continue

            busy_times = parse_ics_file(ics_path)
            date_input = input("Enter the date to check (YYYY-MM-DD): ").strip()
            try:
                day_to_check = datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Returning to main menu.")
                continue
            active_start_input = input("Enter the start of your active hours (HH:MM): ").strip()
            try:
                active_start = datetime.strptime(active_start_input, "%H:%M").time()
            except ValueError:
                print("Invalid time format. Returning to main menu.")
                continue
            active_end_input = input("Enter the end of your active hours (HH:MM): ").strip()
            try:
                active_end = datetime.strptime(active_end_input, "%H:%M").time()
            except ValueError:
                print("Invalid time format. Returning to main menu.")
                continue

            free_times = get_free_times(busy_times, day_to_check, active_start, active_end)

            if not free_times:
                print("No free times available. Returning to main menu.")
                continue

            formatted_free_times = format_free_times(free_times)
            print("Available Free Times:")
            for idx, free_time in enumerate(formatted_free_times, 1):
                print(f"{idx}. {free_time}")

            # Machine learning integration
            csv_file = "C:/Users/Sherv/Desktop/Coding Portfolio/Calendar Project/V2/scheduled_activities_train.csv"  # Update this path
            data = pd.read_csv(csv_file)

            data, le_activity, le_category = preprocess_data(data)
            knn_model = train_category_specific_knn(data, selected_category, n_neighbors=3)

            # Predict and schedule activity
            # Basically whats happening is we're about to check each time in our free time slots
            # to see what activity usually happens at that time
            # if the activity that usually happens at that time is the activity the user wants to schedule
            # we add that time to the predictions list
            print("Finding the best time for your activity...")
            predictions = []
            for free_time in free_times:
                hour = free_time.hour
                prediction = predict_activity(knn_model, le_activity, hour)
                if prediction == selected_activity:
                    predictions.append(free_time)

            if not predictions:
                print("No suitable time found. Returning to main menu.")
                continue

            print("Suggested Time Slots:")
            for idx, time_slot in enumerate(predictions, 1):
                print(f"{idx}. {time_slot.strftime('%H:%M')}")

            time_choice = input("Enter the time slot number to schedule or type 'home' to return: ").strip()
            if time_choice.lower() == 'home':
                continue

            if not time_choice.isdigit() or int(time_choice) not in range(1, len(predictions) + 1):
                print("Invalid choice. Returning to main menu.")
                continue

            scheduled_time = predictions[int(time_choice) - 1]
            queued_tasks.append({"Activity": selected_activity, "Time": scheduled_time})
            print(f"Task queued: {selected_activity} at {scheduled_time.strftime('%H:%M')}")

        elif choice == "2":
            # Remove Queued Activity
            if not queued_tasks:
                print("No tasks in queue to remove.")
                continue

            print("Queued Tasks:")
            for idx, task in enumerate(queued_tasks, 1):
                print(f"{idx}. {task['Activity']} at {task['Time'].strftime('%H:%M')}")

            task_choice = input("Enter the task number to remove or type 'home' to return: ").strip()
            if task_choice.lower() == 'home':
                continue

            if not task_choice.isdigit() or int(task_choice) not in range(1, len(queued_tasks) + 1):
                print("Invalid choice. Returning to main menu.")
                continue

            removed_task = queued_tasks.pop(int(task_choice) - 1)
            print(f"Removed task: {removed_task['Activity']} at {removed_task['Time'].strftime('%H:%M')}")

        elif choice == "3":
            # Confirm Scheduling
            if not queued_tasks:
                print("No tasks to confirm.")
                continue

            print("Confirming tasks...")
            for task in queued_tasks:
                scheduled_tasks.append(task)
            queued_tasks.clear()

            print("All tasks confirmed. Generating updated .ics file...")

            # Create a new .ics file
            calendar = Calendar()

            # Correctly copy existing events with their original dates
            with open(ics_path, "r") as old_file:
                old_calendar = Calendar(old_file.read())
                for event in old_calendar.events:
                    new_event = Event()
                    new_event.name = event.name
                    new_event.begin = event.begin
                    new_event.end = event.end
                    new_event.description = event.description
                    new_event.uid = event.uid # Important: Copy the UID to avoid duplicates if the file is re-imported
                    calendar.events.add(new_event)

            # Add the new scheduled tasks, using the correct date
            for task in scheduled_tasks:
                event = Event()
                event.name = task["Activity"]
                event.begin = datetime.combine(day_to_check, (datetime.combine(day_to_check, task["Time"].time()) + timedelta(hours=4)).time())
                calendar.events.add(event)

            with open("updated_calendar.ics", "w") as f:
                f.writelines(calendar)

            print("Updated calendar saved.")
        elif choice == "4":
            # Quit
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
