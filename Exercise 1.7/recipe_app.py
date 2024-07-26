from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
import sys


#Connect SQLAlchemy to database
engine = create_engine("mysql://cf-python:Vanitakhan1@localhost/my_database")

#Create declarative base class
Base = declarative_base()

#Create session class and connect it to engine
Session = sessionmaker(bind=engine)
session = Session()


#Create recipe table
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    #Define __repr__ method
    def __repr__(self):
        return f"<Recipe ID: {self.id}, Name: {self.name}, Difficulty: {self.difficulty}"
    
    #Define __str__ method
    def __str__(self):
        return (
            f"\nRecipe: {self.name}\n"
            f"\n("-"*10)\n"
            f"\nIngredients: {self.ingredients}\n"
            f"\nCooking Time (in minutes): {self.cooking_time}\n"
            f"\nDifficulty: {self.difficulty}\n"
        )
    
    def calculate_difficulty(self):
        ingredients_len = len(self.ingredients.split(","))
        self.difficulty = ""
        if self.cooking_time < 10 and ingredients_len < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and ingredients_len >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and ingredients_len < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and ingredients_len >= 4:
           self.difficulty = "Hard"

    def return_ingredients_as_list(self):
       return [] if self.ingredients == "" else self.ingredients.split(",")

Base.metadata.create_all(engine)

#Create new recipe
class Menu(Recipe):
    def create_recipe(self):
            #Recipe name
            name = self.name_input()
            if name is None: return 
            #Recipe cooking time
            cooking_time = self.cooking_time_input()
            if cooking_time is None: return
            #Recipe ingredients
            ingredients = self.ingredients_input()
            if ingredients is None: return

            recipe_entry = Recipe(name=name, cooking_time=cooking_time, ingredients=ingredients)
            recipe_entry.calculate_difficulty()
            session.add(recipe_entry)
            session.commit()
            print("Recipe successfully added.\n")
    

    def name_input(self):
        name = input("Enter the name of the recipe: ")
        if len(name) > 50:
            print("\nRecipe name must be under 50 characters.\n")
            return None
        elif not name.replace(" ", "").isalnum():
            print("\nInvalid input. Please enter a name containing only letters and numbers.\n")
            return None
        else:
            return name
        

    def cooking_time_input(self):
        cooking_time = int(input("Enter the cooking time of the recipe(in minutes): "))
        if cooking_time <= 0:
            print("/nThe cooking time time needs to be a positive number.")
        elif cooking_time.isnumeric() == False:
            print("/nThe cooking time cannot include letters. Please enter a valid number.")
        else: 
            return cooking_time
        
    def ingredients_input(self):
        ingredients = []
        ingredients_number = input("How many ingredients would you like to enter: ")
        if ingredients_number.isnumeric() == False or int(ingredients_number) <= 0:
            print("\nYou need to enter a positive number.\n")
            return None
        for i in range(int(ingredients_number)):
            ingredient = input("Enter one ingredient and hit Enter: ")
            if ingredient != "":
                ingredients.append(ingredient)
            else:
                break
            ingredients = ", ".join(ingredients)
            return ingredients


    #View all recipes
    def view_all_recipes():
        all_recipes = session.query(Recipe).all()
        if len(all_recipes) < 1:
            print("\nThere are no recipes in the database!/n")
            return None
        for recipe in all_recipes:
            print(recipe)

    def search_by_ingredients():
        if session.query(Recipe).count() == 0: 
            print("\n There are currently no recipes yet. Exiting now\n")
            return None
        
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []

        for result in results:
            ingredients_list = result[0].split(",")
            for ingredient in ingredients_list:
                if ingredient not in ingredients_list:
                    all_ingredients.append(ingredient)

        for position, ingredient in enumerate(all_ingredients):
            print("Ingredient " + str(position) + ": " + ingredient)

        try:
            ingredient_indexes = input("Enter the numbers of the ingredient you would like to search for (comma-separated): ").split(", ")
            search_ingredients = []
            for index in ingredient_indexes:
                ingredient_index = int(index)
                search_ingredients.append(all_ingredients[ingredient_index])
        except ValueError:
            print("\n One or more of your inputs aren't numbers.\n")
            return 
        except IndexError:
            print("\n The number you entered is not on the list.\n")
            return 
        except:
            print("An unexpected error occurred.\n")
            sys.exit(1)

        conditions = []
        for search_ingredient in search_ingredients:
            like_term = f"%{search_ingredient}%"
            conditions.append(Recipe.ingredients.like(like_term))
        filtered_recipes = session.query(Recipe).filter(*conditions).all()
        if len(filtered_recipes) <= 0:
            print("/n There are no recipes containing all of the ingredients\n")
        else:
            for filtered_recipe in filtered_recipes:
                print(filtered_recipe)


    def choose_recipe_id(self):
        if session.query(Recipe).count() == 0:
            print("\nThere are no recipes yet.\n")
            return None

        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        recipe_ids = [result[0] for result in results]
        for result in results:
            print("\nRecipe ID:", result[0], "- Recipe Name: ", result[1]+"\n")

        try:
            recipe_id = int(input("Enter the the id of the recipe you want to choose: "))
        except ValueError:
            print("\nOne or more of your inputs aren't in the right format.\n")
            return None
        except Exception as e:
            print("An unexpected error occurred.{e}\n")
            sys.exit(1)
        
        if recipe_id not in recipe_ids:
            print("\nID doesn't exists.\n")
            return None
        else:
            return recipe_id

        
    def edit_recipe(self):
        recipe_id = self.choose_recipe_id()
        if recipe_id is None: return

        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        print("Recipe")
        print("-"*10)
        print("1. Name", recipe_to_edit.name)
        print("2. Ingredients", recipe_to_edit.ingredients)
        print("3. Cooking Time", recipe_to_edit.cooking_time)

        try:
            attribute = int(input("Please enter the number of the attribute you'd like to enter: "))
        except ValueError:
            print("One or more of your inputs aren't in the right format.\n")
            return
        except:
            print("\nAn unexpected error occurred.\n")
            sys.exit(1)

        if attribute == 1:
            while True:
                name = str(input("Please enter the new recipe name here: "))
                if len(name) > 50: 
                    print("/nName is too long, please enter a name that does not exceed 50 characters including spaces: ")
                else: break
            recipe_to_edit.name = name
        elif attribute == 2:
            ingredients_list = []
            while True:
                ingredient = str(input("Enter new ingredient or hit enter if done: "))
                if ingredient != "":
                    ingredients_list.append(ingredient)
                else: break
            ingredients = ", ".join(ingredients_list)
            recipe_to_edit.ingredients = ingredients
            recipe_to_edit.calculate_difficulty()
        elif attribute == 3:
            while True:
                cooking_time_input = input("Enter new cooking time in minutes: ")
                if not cooking_time_input.isnumeric():
                    print("This is not a number. Please enter minutes as a number.")
                else:
                    cooking_time = int(cooking_time_input)
                    break
            recipe_to_edit.cooking_time = cooking_time
            recipe_to_edit.calculate_difficulty()
        else:
            print("Number is invalid! Going back to main menu.")
            return
        # Commit changes
        session.commit()


    def delete_recipe(self):
        recipe_id = self.choose_recipe_id()
        if recipe_id is None: return

        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        decision = input(f"\nIf you are sure that you want to delete {recipe_to_delete.name} type 'yes': ")

        if decision.lower() == "yes":
            session.delete(recipe_to_delete)
            session.commit()
            print("\nRecipe successfully deleted.\n")
        else:
            print("\nDid't delete recipe.\n")
            return None


    # MAIN MENU

    def main_menu(self):
        choice = ""
        while(choice != 'quit'):
            print("Main Menu")
            print("----------")
            print("What would you like to do? Pick a choice!")
            print("1. Create a new recipe")
            print("2. Search for recipe by ingredient")
            print("3. Update an existing recipe")
            print("4. Delete a recipe")
            print("Type 'quit' to exist the program.")
            choice = (input("\nYour choice (type in a number or 'quit'): "))

            if choice == "1":
                self.create_recipe()
            elif choice == "2":
                self.view_all_recipes()
            elif choice == "3":
                self.edit_recipe()
            elif choice == "4":
                self.delete_recipe()
            elif choice == "quit":
                print("Exiting the program.\n")
                session.close()
                engine.dispose()
                break
            else:
                print("Please write the number of one of the choices.\n")

menu = Menu()
menu.display_menu()
