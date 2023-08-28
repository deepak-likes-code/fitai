import streamlit as st
from fpdf import FPDF

from functions import calculate_tdee, generate_plan

st.set_page_config(
    page_title="FitAI",
    page_icon="🏋🏻",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://twitter.com/0xdeepak_eth",
        "About": "# AI App that helps you build a workout routine and plan meals according to the fitness goal you have in mind. ",
    },
)
# Sidebar for OpenAI API Key Input
st.sidebar.title('Insert OpenAI API Key to use GPT4')
user_openai_key = st.sidebar.text_input('Enter OpenAI API Key (Please):')


# Title
st.title(' 🏋🏻 FitAI: Personalized Fitness')

# Introduction
st.markdown("""
Your next-level fitness companion. Combining AI's precision with expert health insights, we craft tailored workout regimes and meal plans just for you. Dive into a personalized fitness journey,
ensuring optimal results tailored to your goals. Elevate your health and well-being with FitAI
smart choices, and never giving up. Now, let's build your personalized plan! (If you have an OpenAI API key, please open the sidebar and insert it. For now, this app is free to use thanks to https://twitter.com/0xdeepak_eth)
""")


# User Name
name = st.text_input('Enter Your Name (Optional)', value='Anon', max_chars=50)

# User Input for Workout Goals
goal = st.selectbox('Choose Your Fitness Goal', [
                    'Weight Loss', 'Muscle Gain', 'Maintenance'])

# User Input for Dietary Preferences
diet = st.multiselect('Select Dietary Preferences (Optional)', [
                      'Vegan', 'Keto', 'Low-Carb', 'High-Carb', 'Carb-Cycling', 'Gluten-Free'])

cuisine = st.multiselect('Select Cuisine Preferences (Optional)', [
    'Indian', 'Continental', 'Lebanese', 'Mediterranean', 'Chinese', 'Japanese'])

# Items in Fridge (for personalized diet recommendations)
fridge_items = st.text_area('Items in Your Fridge (Optional, leave empty if you only want a workout regimen)',
                            value='', placeholder='E.g., eggs, chicken, broccoli, almonds...')


# Preferred Training Styles
training_styles = st.multiselect('Select Your Preferred Training Style - You can mix and match up to 3 trainers thanks to AI (Optional)', [
    'Bodybuilding – Focus on Hypertrophy and Aesthetics',
    'CrossFit – Functional Fitness with Varied High-Intensity Workouts',
    'Powerlifting – Focus on Strength and Power',
    'Yoga – Focus on Flexibility and Mindfulness',
    'Pilates – Focus on Core Strength and Posture',
    'HIIT – High-Intensity Interval Training',
    'Fasted Cardio – Cardio on an Empty Stomach',
    'Kickboxing – Martial Arts and Cardio',
    'Boxing – Martial Arts and Cardio',
    'Muay Thai – Martial Arts and Cardio',
    'Karate – Martial Arts',
    'Taekwondo – Martial Arts',
    'Zumba – Dance Fitness',
    'Arnold Schwarzenegger – Volume Training and Classic Physique',
    'Mike Mentzer – High-Intensity Training (HIT)',
    'Jay Cutler – Balanced Approach with Emphasis on Symmetry',
    'Dorian Yates – HIT with Blood and Guts Training',
    'Frank Zane – Focus on Proportion and Aesthetics',
    'Ronnie Coleman – High Volume and Heavy Lifting',
    'Lee Haney – Stimulate, Don\'t Annihilate; Emphasis on Recovery',
    'Calisthenics – Bodyweight Training for Strength and Flexibility',
    'Rich Gaspari – Pre-Exhaustion Training with Intensity',
    'Lou Ferrigno – Power Bodybuilding with Heavy Weights',
    'Sergio Oliva – Classic Mass Building with Frequent Training',
    'Larry Scott – Focus on Arms and Shoulders',
    'Tom Platz – High Volume Leg Specialization',
    'Flex Wheeler – Quality over Quantity; Focus on Form',
    'Phil Heath – Scientific Approach with Attention to Detail',
    'Chris Bumstead – Classic Physique with Modern Training',
    'Kai Greene – Mind-Muscle Connection and Artistic Expression',



], max_selections=3)


# Height and Weight Inputs
units = st.selectbox('Choose Your Units', ['cm/kg', 'inches/lbs'])

if units == 'inches/lbs':
    height_description = 'Enter Your Height (e.g., 68 inches)'
    weight_description = 'Enter Your Weight (e.g., 160 lbs)'
else:  # Assuming the other option is 'cm/kg'
    height_description = 'Enter Your Height (e.g., 172 cm)'
    weight_description = 'Enter Your Weight (e.g., 73 kg)'

height = st.number_input(
    height_description, min_value=0, max_value=300, step=1)
weight = st.number_input(
    weight_description, min_value=0, max_value=500, step=1)

age = st.number_input('Enter Your Age', min_value=0, max_value=120, step=1)
gender = st.radio('Select your gender', ('Male', 'Female', 'Non-Binary'))

# Activity Level
activity_levels = {
    "Sedentary (little to no exercise)": 1.2,
    "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
    "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
    "Very active (hard exercise/sports 6-7 days a week)": 1.725,
    "Super active (very hard exercise/sports & physical job or training twice a day)": 1.9
}
activity_level = st.selectbox(
    'Choose Your Activity Level', list(activity_levels.keys()))
activity_factor = activity_levels[activity_level]


# Generate Workout and Diet Plan
if st.button('Generate Plan'):
    # Validation checks
    if not height or not weight or not age or not activity_level:
        st.error(
            'Please fill in all required fields (Height, Weight, Age, and Activity Level) before generating the plan.')
    else:
        with st.spinner('We\'re all gonna make it brah... Generating...'):
            # Calculate TDEE
            tdee = calculate_tdee(
                height, weight, activity_levels[activity_level], goal, age, units, gender)

            # Check if TDEE is calculated
            if tdee:
                # Call the generate_plan function with the calculated TDEE
                plan = generate_plan(name,
                                     goal, diet, fridge_items, training_styles, tdee, age, cuisine)
                # Check if the plan has been generated
                if plan:
                    # Define a function to convert your content into a PDF
                    def text_to_pdf(plan):
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Helvetica", size=12)
                        pdf.multi_cell(0, 10, txt=plan,
                                       markdown=True)

                        # Save the pdf with name .pdf
                        file_name = "generated_plan.pdf"
                        pdf.output(file_name)

                        # Return the generated PDF's filename
                        return file_name

                    # Convert the plan into a PDF
                    pdf_file_name = text_to_pdf(plan)

                    # Open and read the generated PDF to provide as data to the download_button
                    with open(pdf_file_name, "rb") as f:
                        pdf_data = f.read()

                    # Create a download button for the generated PDF
                    st.download_button(
                        label="Download Your Plan",
                        data=pdf_data,
                        file_name="generated_plan.pdf",
                        mime="application/pdf",
                    )

            else:
                st.error(
                    'An error occurred while calculating your plan. Please make sure all inputs are correct.')
