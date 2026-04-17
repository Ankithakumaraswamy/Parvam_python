import os
import pandas as pd


EXCEL_FILE = os.path.join(os.path.dirname(__file__), "Student_Performance.xlsx")
SUBJECTS = ["Math", "Science", "English"]


def calculate_grade(average):
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 50:
        return "C"
    return "D"


def get_student_data():
    print("Student Performance Input System")
    print("-" * 35)

    name = input("Enter student name: ").strip().title()

    marks = {}
    for subject in SUBJECTS:
        while True:
            try:
                score = float(input(f"Enter marks for {subject} (0-100): "))
                if 0 <= score <= 100:
                    marks[subject] = score
                    break
                print("Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter numeric marks.")

    return {
        "Name": name,
        "Math": marks["Math"],
        "Science": marks["Science"],
        "English": marks["English"],
    }


def load_existing_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)

    return pd.DataFrame(columns=["Name", "Math", "Science", "English", "Average", "Grade"])


def save_student_data(student_record):
    df = load_existing_data()
    average = round((student_record["Math"] + student_record["Science"] + student_record["English"]) / 3, 2)
    grade = calculate_grade(average)

    student_record["Average"] = average
    student_record["Grade"] = grade

    if student_record["Name"] in df["Name"].values:
        df.loc[df["Name"] == student_record["Name"], ["Math", "Science", "English", "Average", "Grade"]] = [
            student_record["Math"],
            student_record["Science"],
            student_record["English"],
            student_record["Average"],
            student_record["Grade"],
        ]
        message = f"Updated existing record for {student_record['Name']}."
    else:
        df = pd.concat([df, pd.DataFrame([student_record])], ignore_index=True)
        message = f"Added new record for {student_record['Name']}."

    df.to_excel(EXCEL_FILE, index=False)
    return message


def main():
    student_record = get_student_data()
    message = save_student_data(student_record)
    print(message)
    print(f"Average: {student_record['Average']}")
    print(f"Grade: {student_record['Grade']}")
    print(f"Excel file saved at: {EXCEL_FILE}")


if __name__ == "__main__":
    main()
