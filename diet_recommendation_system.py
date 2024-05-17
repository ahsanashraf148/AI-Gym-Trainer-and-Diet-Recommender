from typing import List,Optional
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from random import uniform as rnd

import tkinter as tk
from tkinter import messagebox


nutrition_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']

def diet():
    def get_recommendations():
        nutrition_input = get_values()
        ingredients = ingredients_entry.get().split(',')
        recommendations = update_item(nutrition_input,ingredients,dataset)
        recommendations = recommendations['output']
        if recommendations is None:
            messagebox.showinfo("Recommendations", "Couldn't find any recipes with the specified ingredients")
        else:
            display_recommendation(recommendations)

    def get_values() -> list[float]:
        values = [calories_scale.get(), fat_content_scale.get(), saturated_fat_content_scale.get(), cholesterol_content_scale.get(), sodium_content_scale.get(), carbohydrate_content_scale.get(), fiber_content_scale.get(), sugar_content_scale.get(), protein_content_scale.get()]
        return values

    def on_frame_configure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    def display_recommendation(recommendations):
        recommendations_text.delete('1.0', tk.END)
        recommendations_text.insert(tk.END, 'Recommended recipes:\n')
        if recommendations is not None:
            rows = len(recommendations) // 5
            for row in range(5):
                for recipe in recommendations[rows*row:rows*(row+1)]:
                    recipe_name = recipe['Name']
                    recommendations_text.insert(tk.END, "\nRecipe Name: " + recipe_name + '\n')
                    nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutrition_values})
                    recommendations_text.insert(tk.END, "Nutritional Values (g): \n" + str(nutritions_df) + '\n')
                    recommendations_text.insert(tk.END, "Ingredients: \n")
                    for ingredient in recipe['RecipeIngredientParts']:
                        recommendations_text.insert(tk.END, "- " + ingredient + '\n')
                    recommendations_text.insert(tk.END, "Recipe Instructions: \n")
                    for instruction in recipe['RecipeInstructions']:
                        recommendations_text.insert(tk.END, "- " + instruction + '\n')
                    recommendations_text.insert(tk.END, "Cooking and Preparation Time: \n")
                    recommendations_text.insert(tk.END, "- Cook Time       : " + str(recipe['CookTime']) + " min\n")
                    recommendations_text.insert(tk.END, "- Preparation Time: " + str(recipe['PrepTime']) + " min\n")
                    recommendations_text.insert(tk.END, "- Total Time      : " + str(recipe['TotalTime']) + " min\n")
        else:
            recommendations_text.insert(tk.END, "Couldn't find any recipes with the specified ingredients")


    root = tk.Tk()
    root.title("Diet Recommendation System")
    root.geometry("600x400+350+10")
    root.config(bg='black')

    canvas = tk.Canvas(root, bg='black')
    scrollbar = tk.Scrollbar(root, command=canvas.yview, bg='gold')
    frame = tk.Frame(canvas, bg='black')

    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))

    calories_scale = tk.Scale(frame, from_=0, to=2000, orient=tk.HORIZONTAL, label="Calories", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    calories_scale.pack()

    fat_content_scale = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Fat Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    fat_content_scale.pack()

    saturated_fat_content_scale = tk.Scale(frame, from_=0, to=13, orient=tk.HORIZONTAL, label="Saturated Fat Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    saturated_fat_content_scale.pack()

    cholesterol_content_scale = tk.Scale(frame, from_=0, to=300, orient=tk.HORIZONTAL, label="Cholesterol Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    cholesterol_content_scale.pack()

    sodium_content_scale = tk.Scale(frame, from_=0, to=2300, orient=tk.HORIZONTAL, label="Sodium Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    sodium_content_scale.pack()

    carbohydrate_content_scale = tk.Scale(frame, from_=0, to=325, orient=tk.HORIZONTAL, label="Carbohydrate Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    carbohydrate_content_scale.pack()

    fiber_content_scale = tk.Scale(frame, from_=0, to=50, orient=tk.HORIZONTAL, label="Fiber Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    fiber_content_scale.pack()

    sugar_content_scale = tk.Scale(frame, from_=0, to=40, orient=tk.HORIZONTAL, label="Sugar Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    sugar_content_scale.pack()

    protein_content_scale = tk.Scale(frame, from_=0, to=40, orient=tk.HORIZONTAL, label="Protein Content", length=500, resolution=5, bg='black', fg='gold', troughcolor='gold')
    protein_content_scale.pack()

    ingredients_label = tk.Label(frame, text="Enter Ingredients (comma separated):", bg='black', fg='gold')
    ingredients_label.pack()
    ingredients_entry = tk.Entry(frame, bg='gold', fg='black', width=50)
    ingredients_entry.pack()

    recommend_button = tk.Button(frame, text="Get Recommendations", command=get_recommendations, bg='gold', fg='black')
    recommend_button.pack()

    recommendations_text = tk.Text(frame, bg='black', fg='gold')
    recommendations_text.pack()

    recommendations_scrollbar = tk.Scrollbar(frame, command=recommendations_text.yview, bg='gold')
    recommendations_scrollbar.pack(side='right', fill='y')

    recommendations_text.config(yscrollcommand=recommendations_scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    root.mainloop()


def diet2():
    display=Display()
    def submit_form():
        age = age_entry.get()
        height = height_entry.get()
        weight = weight_entry.get()
        gender = gender_var.get()
        activity = activity_var.get()
        option = option_var.get()
        number_of_meals = number_of_meals_scale.get()
        plans=["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        weights=[1,0.9,0.8,0.6]
        losses=['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']

        weight_loss=weights[plans.index(option)]
        if number_of_meals==3:
            meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}
        elif number_of_meals==4:
            meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
        else:
            meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}
        person = Person(age,height,weight,gender,activity,meals_calories_perc,weight_loss)
        display=Display()
        display.display_bmi(root, person)
        display.display_calories(root, person)
        recommendations=person.generate_recommendations()


        display.display_recommendation(root, person,recommendations)
        # Your code to generate the diet recommendations goes here

    root = tk.Tk()
    root.title("Automatic Diet Recommendation")
    root.geometry("700x400+350+10")
    root.config(bg='blue')

    frame = tk.Frame(root, bg='blue')
    frame.pack()

    age_label = tk.Label(frame, text="Age", bg='blue', fg='white')
    age_label.pack()
    age_entry = tk.Entry(frame, bg='white', fg='black')
    age_entry.pack()

    height_label = tk.Label(frame, text="Height(cm)", bg='blue', fg='white')
    height_label.pack()
    height_entry = tk.Entry(frame, bg='white', fg='black')
    height_entry.pack()

    weight_label = tk.Label(frame, text="Weight(kg)", bg='blue', fg='white')
    weight_label.pack()
    weight_entry = tk.Entry(frame, bg='white', fg='black')
    weight_entry.pack()

    gender_var = tk.StringVar()
    gender_label = tk.Label(frame, text="Gender", bg='blue', fg='white')
    gender_label.pack()
    gender_radio1 = tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male", bg='blue', fg='white')
    gender_radio1.pack()
    gender_radio2 = tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female", bg='blue', fg='white')
    gender_radio2.pack()

    activity_var = tk.StringVar()
    activity_label = tk.Label(frame, text="Activity", bg='blue', fg='white')
    activity_label.pack()
    activity_options = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
    activity_optionmenu = tk.OptionMenu(frame, activity_var, *activity_options)
    activity_optionmenu.config(bg='white', fg='black')
    activity_optionmenu.pack()

    option_var = tk.StringVar()
    option_label = tk.Label(frame, text="Choose your weight loss plan:", bg='blue', fg='white')
    option_label.pack()
    option_options = display.plans  # Replace this with your list of plans
    option_optionmenu = tk.OptionMenu(frame, option_var, *option_options)
    option_optionmenu.config(bg='white', fg='black')
    option_optionmenu.pack()

    number_of_meals_label = tk.Label(frame, text="Meals per day", bg='blue', fg='white')
    number_of_meals_label.pack()
    number_of_meals_scale = tk.Scale(frame, from_=3, to=5, orient=tk.HORIZONTAL, length=500, resolution=1, bg='blue', fg='white', troughcolor='white')
    number_of_meals_scale.pack()

    submit_button = tk.Button(frame, text="Generate", command=submit_form, bg='white', fg='black')
    submit_button.pack()

    root.mainloop()

dataset=pd.read_csv('Data\\dataset.csv',compression='gzip')

def scaling(dataframe):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    return extracted_data

def extract_ingredient_filtered_data(dataframe,ingredients):
    extracted_data=dataframe.copy()
    # print(extracted_data)
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    # print(extracted_data)
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    _input=np.array(_input).reshape(1,-1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommend(dataframe,_input,ingredients=[],params={'n_neighbors':5,'return_distance':False}):
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]>=params['n_neighbors']:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
        else:
            return None

def extract_quoted_strings(s):
    # Find all the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # Join the strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output=dataframe.copy()
        output=output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
    else:
        output=None
    return output

def update_item(nutrition_input, ingredients=[], dataset=dataset):
    recommendation_dataframe=recommend(dataset, nutrition_input, ingredients)
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

# def display_recommendation(recommendations):
#     print('Recommended recipes:')
#     if recommendations is not None:
#         rows = len(recommendations) // 5
#         for row in range(5):
#             for recipe in recommendations[rows*row:rows*(row+1)]:
#                 recipe_name = recipe['Name']
#                 print("\nRecipe Name: ", recipe_name)
#                 # recipe_link = recipe['image_link']
#                 # print("Recipe Link: ", recipe_link)
#                 nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutrition_values})
#                 print("Nutritional Values (g): ")
#                 print(nutritions_df)
#                 print("Ingredients: ")
#                 for ingredient in recipe['RecipeIngredientParts']:
#                     print("- ", ingredient)
#                 print("Recipe Instructions: ")
#                 for instruction in recipe['RecipeInstructions']:
#                     print("- ", instruction)
#                 print("Cooking and Preparation Time: ")
#                 print("- Cook Time       : ", recipe['CookTime'], "min")
#                 print("- Preparation Time: ", recipe['PrepTime'], "min")
#                 print("- Total Time      : ", recipe['TotalTime'], "min")
#     else:
#         print("Couldn't find any recipes with the specified ingredients")

# recommendations=update_item(dataset, nutrition_input=[500,50,0,0,400,100,10,10,10], ingredients=['chicken','Milk','eggs','butter'])
# # recommendations = recommendations.json()['output']
# recommendations=recommendations['output']
# display_recommendation(recommendations)

class Person:

    def __init__(self,age,height,weight,gender,activity,meals_calories_perc,weight_loss):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.meals_calories_perc=meals_calories_perc
        self.weight_loss=weight_loss
    def calculate_bmi(self,):
            self.height = float(self.height)
            self.weight = float(self.weight)
            bmi = round(self.weight / ((self.height / 100) ** 2), 2)
            return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        self.weight = float(self.weight)
        self.height = float(self.height)
        self.age = float(self.age)
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories

    def generate_recommendations(self,):
        total_calories=self.weight_loss*self.calories_calculator()
        recommendations=[]
        for meal in self.meals_calories_perc:
            meal_calories=self.meals_calories_perc[meal]*total_calories
            if meal=='breakfast':
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            elif meal=='launch':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
            elif meal=='dinner':
                recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
            else:
                recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
            recommended_recipes=update_item(recommended_nutrition)
            recommended_recipes = recommended_recipes["output"]
            recommendations.append(recommended_recipes)
        return recommendations


class Display:
    def __init__(self):
        self.plans=["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        self.weights=[1,0.9,0.8,0.6]
        self.losses=['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']
        pass

    def display_bmi(self,root,person):
        bmi_string, category, color = person.display_result()
        bmi_window = tk.Toplevel(root)
        bmi_window.title("BMI Calculator")
        bmi_label = tk.Label(bmi_window, text=f"Body Mass Index (BMI): {bmi_string}\n{category}", fg=color)
        bmi_label.pack()

    def display_calories(self,root,person):
        maintain_calories = person.calories_calculator()
        calories_window = tk.Toplevel(root)
        calories_window.title("Calories Calculator")
        for plan, weight, loss in zip(self.plans, self.weights, self.losses):
            calories_label = tk.Label(calories_window, text=f"{plan}: {round(maintain_calories*weight)} Calories/day, {loss}")
            calories_label.pack()

    def display_recommendation(self,root, person, recommendations):
        meals = person.meals_calories_perc
        recommendation_window = tk.Toplevel(root)
        recommendation_window.title("Diet Recommender")
        for meal_name, recommendation in zip(meals, recommendations):
            meal_label = tk.Label(recommendation_window, text=f"{meal_name.upper()}")
            meal_label.pack()
            for recipe in recommendation:
                recipe_name = recipe['Name']
                recipe_label = tk.Label(recommendation_window, text=recipe_name)
                recipe_label.pack()

                nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutrition_values})
                nutritions_label = tk.Label(recommendation_window, text=nutritions_df.to_string())
                nutritions_label.pack()

                # Display the ingredients
                ingredients_label = tk.Label(recommendation_window, text="Ingredients:")
                ingredients_label.pack()
                for ingredient in recipe['RecipeIngredientParts']:
                    ingredient_label = tk.Label(recommendation_window, text=f"- {ingredient}")
                    ingredient_label.pack()

                instructions_label = tk.Label(recommendation_window, text="Recipe Instructions:")
                instructions_label.pack()
                for instruction in recipe['RecipeInstructions']:
                    instruction_label = tk.Label(recommendation_window, text=f"- {instruction}")
                    instruction_label.pack()

                time_label = tk.Label(recommendation_window, text=f"Cook Time: {recipe['CookTime']}min\nPreparation Time: {recipe['PrepTime']}min\nTotal Time: {recipe['TotalTime']}min")
                time_label.pack()
