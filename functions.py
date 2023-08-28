import os
import streamlit as st
import openai
import time


# Use the user-provided key if available, otherwise use the secret key
user_openai_key = os.environ.get('OPENAI_API_KEY')
openai_api_key = user_openai_key if user_openai_key else st.secrets["OPENAI_API_KEY"]

# Set the OpenAI API key
openai.api_key = openai_api_key

# Replace with your OpenAI API key
# openai.api_key = ""

# Function to calculate TDEE


def calculate_tdee(height, weight, activity_level, goal, age, units, gender):
    # Convert height and weight to centimeters and kilograms
    if units == 'inches/lbs':
        height_cm = height * 2.54
        weight_kg = weight * 0.453592
    else:  # Assuming the other option is 'cm/kg'
        height_cm = height
        weight_kg = weight

    # Calculate BMR using Mifflin-St Jeor Equation
    if gender == 'Male':
        s = 5
    else:
        s = -161

    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + s

    # Multiply by activity factor
    tdee = bmr * activity_level

    # Adjust for goal (e.g., weight loss)
    # if goal == "Weight Loss":
    #    tdee -= 350  # Example deficit for weight loss
    # elif goal == "Muscle Gain":
   #     tdee += 350
   # currently gpt4 already does this part
    return tdee


SCHEMA = """
WorkoutPlan:\n
  Day: Monday
    Workout: Chest
        Exercises:
            - Bench Press
            - Incline Bench Press
            - Dumbbell Flys
            - Cable Crossovers
            - Pushups

     
    notes( Additional information, tips, or instructions related to the workout plan.)
  
DietPlan:
  Day: Monday
  meals:
   Breakfast
    Pancakes
   Lunch
   Chicken Curry
    Dinner
    - 1 cup of brown rice
    - 1 cup of broccoli
        
            
            
"""


def generate_plan(name, goal, diet, fridge_items, training_styles, tdee, age, cuisine):
    messages = [
        {
            "role": "system",
            "content": f"You are an extremely detailed Ai, who is knowledgeable in bodybuilding/fitness/dietitian and an expert! You only respond ethically. You'll be responding to {name}'s request for a workout plan and diet plan."
        },
        {
            "role": "user",
            "content": f"""My dietary preferences are {diet}.
            Create the perfect curated plan from {training_styles}. 
            If there is anything in my fridge {fridge_items}, please include a meal plan according to my preferred cuisine {cuisine} along with the macros and Kcal, if not, dont mention the fridge being empty and create a simple meal plan with the preffered cuisine {cuisine} along with the macros and Kcal.
            My TDEE is {tdee} and I am {age} years old. My fitness goal is {goal} so try to give me accurate response based off my info. If i withheld dietary preference or training style, IGNORE IT and carry on with generic response. Do not give me any extra info, just respond as the trainers or mix of trainers and give the workout plan and the philosophy along with some things to research if need be and quotes from the trainers if there are any.
            Be extremely detailed and straight to the point
            
            Give the output for {name} in a structured format for one week, with meals and workouts for each day.
            """

        }
    ]

    delay_time = 0.01
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.666666666666666666666666666666420,
        stream=True,
    )

    # Container to incrementally update the display
    c = st.empty()

    generated_text = ''
    for event in response:
        event_text = event['choices'][0]['delta'].get('content', '')
        generated_text += event_text
        c.markdown(generated_text)  # Update the entire accumulated text
        time.sleep(delay_time)

    return generated_text
