## Exercise 1.2 - Data Types in Python

## Learning Goals

- Explain variables and data types in Python
- Summarize the use of objects in Python
- Create a data structure for your Recipe app

## Topics Covered
- Benefits of IPython Shell
- Non-Scalar Objects vs Scalar Objects
- Tuples, Lists, Strings, and Dictionaries

## Directions (Part 1)

- name (str): Contains the name of the recipe
- cooking_time (int): Contains the cooking time in minutes
- ingredients (list): Contains a number of ingredients, each of the str data type

I have chosen to use dictionaries for storing the data for each recipe because of its flexibility and easy access to values. Dictionaries
contain key-value pairs where values can be of any type including strings, integers, and lists which are needed for the name, cooking time,
and list of ingredients. Additionally, dictionaries are mutable and allow for easy modification if necessary.

For the outer structure, I have decided to use lists since it is easy to append each of the separate recipes to the recipies dictionaries and
can be modified or deleted if needed.
