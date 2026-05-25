
import gradio as gr
import joblib
import pandas as pd

clf_model = joblib.load("model_classification.pkl")
clf_prep = joblib.load("preprocessor_classification.pkl")


def predict_grade(
    age,
    gender,
    hours_studied,
    attendance,
    sleep_hours,
    stress_level,
    screen_time,
    previous_gpa,
    part_time_job,
    study_method,
    diet_quality,
    internet_quality,
    extracurricular,
    tutoring_sessions_per_week,
    family_income_level,
    exam_anxiety_score,
):
    df = pd.DataFrame(
        [
            {
                "Age": age,
                "Gender": gender,
                "Hours_Studied": hours_studied,
                "Attendance": attendance,
                "Sleep_Hours": sleep_hours,
                "Stress_Level": stress_level,
                "Screen_Time": screen_time,
                "Previous_GPA": previous_gpa,
                "Part_Time_Job": 1 if part_time_job == "Yes" else 0,
                "Study_Method": study_method,
                "Diet_Quality": diet_quality,
                "Internet_Quality": internet_quality,
                "Extracurricular": 1 if extracurricular == "Yes" else 0,
                "Tutoring_Sessions_Per_Week": tutoring_sessions_per_week,
                "Family_Income_Level": family_income_level,
                "Exam_Anxiety_Score": exam_anxiety_score,
            }
        ]
    )

    transformed = clf_prep.transform(df)
    grade = clf_model.predict(transformed)[0]
    probs = clf_model.predict_proba(transformed)[0]
    classes = clf_model.classes_
    prob_dict = {c: float(p) for c, p in zip(classes, probs)}
    return grade, prob_dict


with gr.Blocks(title="Student Performance Grade Predictor") as demo:
    gr.Markdown(
        """
        # Student Performance Grade Predictor
        Enter student details and get the predicted grade along with class probabilities.
        """
    )

    with gr.Row():
        age = gr.Number(label="Age", value=20)
        gender = gr.Dropdown(["Male", "Female"], label="Gender")
        study_method = gr.Dropdown(["Online", "Offline", "Hybrid"], label="Study Method")

    with gr.Row():
        hours_studied = gr.Number(label="Hours Studied", value=6.5)
        attendance = gr.Number(label="Attendance (%)", value=85)
        sleep_hours = gr.Number(label="Sleep Hours", value=7)

    with gr.Row():
        stress_level = gr.Number(label="Stress Level", value=3.5)
        screen_time = gr.Number(label="Screen Time (hrs)", value=2.5)
        previous_gpa = gr.Number(label="Previous GPA", value=3.2)

    with gr.Row():
        part_time_job = gr.Dropdown(["No", "Yes"], label="Part-Time Job", value="No")
        extracurricular = gr.Dropdown(["No", "Yes"], label="Extracurricular", value="Yes")
        tutoring_sessions_per_week = gr.Number(label="Tutoring Sessions/Week", value=2)

    with gr.Row():
        diet_quality = gr.Dropdown(["Poor", "Average", "Good"], label="Diet Quality")
        internet_quality = gr.Dropdown(
            ["Poor", "Average", "Good", "Excellent"], label="Internet Quality"
        )
        family_income_level = gr.Dropdown(["Low", "Middle", "High"], label="Family Income")

    exam_anxiety_score = gr.Number(label="Exam Anxiety Score", value=4.0)

    predict_btn = gr.Button("Predict Grade")
    predicted_grade = gr.Textbox(label="Predicted Grade")
    grade_probabilities = gr.JSON(label="Grade Probabilities")

    predict_btn.click(
        fn=predict_grade,
        inputs=[
            age,
            gender,
            hours_studied,
            attendance,
            sleep_hours,
            stress_level,
            screen_time,
            previous_gpa,
            part_time_job,
            study_method,
            diet_quality,
            internet_quality,
            extracurricular,
            tutoring_sessions_per_week,
            family_income_level,
            exam_anxiety_score,
        ],
        outputs=[predicted_grade, grade_probabilities],
    )


if __name__ == "__main__":
    demo.launch()
