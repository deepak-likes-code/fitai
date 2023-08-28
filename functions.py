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


EXAMPLE = """
Sure, Deepak. As a vegan with a preference for Indian cuisine, focusing on Powerlifting and Yoga,
and aiming for weight loss, here is a week-long plan for you.
-
*Workouts*

Monday:
*Workout* - Powerlifting
- Squats: 4 sets of 5 reps
- Bench Press: 4 sets of 5 reps
- Deadlift: 3 sets of 5 reps

-
Tuesday:
*Workout* - Yoga
- Surya Namaskar: 5 sets
- Virabhadrasana II: 3 sets of 30 seconds hold each side
- Balasana: 3 sets of 30 seconds hold


-
Wednesday:
*Workout* - Powerlifting
- Overhead Press: 4 sets of 5 reps
- Barbell Rows: 4 sets of 5 reps
- Pull-ups: 3 sets of max reps

-
Thursday:
*Workout* - Yoga
- Tadasana: 3 sets of 30 seconds hold
- Trikonasana: 3 sets of 30 seconds hold each side
- Savasana: 5 minutes

-
Friday:
*Workout* - Powerlifting
- Squats: 4 sets of 5 reps
- Bench Press: 4 sets of 5 reps
- Deadlift: 3 sets of 5 reps

-
Saturday:
*Workout* - Yoga
- Prasarita Padottanasana: 3 sets of 30 seconds hold each side
- Vrksasana: 3 sets of 30 seconds hold each side
- Shavasana: 5 minutes

-
Sunday:
*Rest Day*
-

*Meal Plan*

Monday:
- Breakfast: Vegan Upma (Protein - 13g, Carbs - 72g, Fat - 17g, Calories - 501)
- Lunch: Rajma Masala with Brown Rice (Protein - 19g, Carbs - 90g, Fat - 6g, Calories - 545)
- Dinner: Mixed Vegetable Curry with Millets (Protein - 9g, Carbs - 60g, Fat - 8g, Calories - 380)

Tuesday:
- Breakfast: Vegan Paratha with Vegan Yogurt (Protein - 13g, Carbs - 60g, Fat - 12g, Calories - 450)
- Lunch: Chole Masala with Brown Bread (Protein - 18g, Carbs - 70g, Fat - 9g, Calories - 485)
- Dinner: Vegan Palak Paneer with Quinoa (Protein - 20g, Carbs - 40g, Fat - 10g, Calories - 370)

Wednesday:
- Breakfast: Vegan Poha (Protein - 10g, Carbs - 60g, Fat - 15g, Calories - 435)
- Lunch: Vegan Biryani with Raita (Protein - 15g, Carbs - 85g, Fat - 10g, Calories - 530)
- Dinner: Vegan Dal Tadka with Millets (Protein - 18g, Carbs - 60g, Fat - 8g, Calories - 400)

Thursday:
- Breakfast: Vegan Idli with Sambar (Protein - 12g, Carbs - 60g, Fat - 10g, Calories - 420)
- Lunch: Vegan Kadai Paneer with Brown Rice (Protein - 20g, Carbs - 80g, Fat - 12g, Calories - 540)
- Dinner: Vegan Kofta with Quinoa (Protein - 18g, Carbs - 40g, Fat - 10g, Calories - 380)

Friday:
- Breakfast: Vegan Dosa with Chutney (Protein - 10g, Carbs - 70g, Fat - 12g, Calories - 460)
- Lunch: Vegan Aloo Gobi with Millets (Protein - 14g, Carbs - 85g, Fat - 10g, Calories - 520)
- Dinner: Vegan Matar Paneer with Brown Rice (Protein - 20g, Carbs - 60g, Fat - 12g, Calories -
480)

Saturday:
- Breakfast: Vegan Uttapam with Sambar (Protein - 14g, Carbs - 70g, Fat - 12g, Calories - 480)
- Lunch: Vegan Dal Makhani with Quinoa (Protein - 18g, Carbs - 70g, Fat - 10g, Calories - 500)
- Dinner: Vegan Stuffed Capsicum with Brown Rice (Protein - 15g, Carbs - 60g, Fat - 10g, Calories -
430)

Sunday:
- Breakfast: Vegan Oats with Fruits (Protein - 10g, Carbs - 70g, Fat - 10g, Calories - 440)
- Lunch: Vegan Vegetable Pulao with Raita (Protein - 14g, Carbs - 75g, Fat - 12g, Calories - 500)
- Dinner: Vegan Shahi Paneer with Millets (Protein - 20g, Carbs - 60g, Fat - 15g, Calories - 475)

-

Remember, consistency is key in achieving your fitness goals. As Vince Lombardi said, "It's not
whether you get knocked down, it's whether you get up." Keep pushing, Deepak!
            
            
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
            If there is anything in my fridge {fridge_items}, please include a meal plan according to my preferred cuisine {cuisine} and the {fridge_items},add other ingredients if necessary, along with the macros and Kcal, if not, dont mention the fridge being empty and create a simple meal plan with the preffered cuisine {cuisine} along with the macros and Kcal.
            My TDEE is {tdee} and I am {age} years old. My fitness goal is {goal} so try to give me accurate response based off my info. If i withheld dietary preference or training style, IGNORE IT and carry on with generic response. Do not give me any extra info, just respond as the trainers or mix of trainers and give the workout plan and the philosophy along with some things to research if need be and quotes from the trainers if there are any.
            Be extremely detailed and straight to the point
            
            Give the output for {name} in a structured format for one week, as use the {EXAMPLE} as a template.
           
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
