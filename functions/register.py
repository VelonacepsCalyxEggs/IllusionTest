import webbrowser

def register(name, age, gender):
        # Example registration logic
        if name == "" or age == "" or gender == "Select Gender":
            # If any of the fields are empty or gender is not selected, show an error popup
            return "Registration Failed", "Please complete all fields."
        elif (not str(age).isdigit()):
            return "Registration Failed", "Age must be a number."
        elif (int(age) >= 100):
            webbrowser.open_new_tab('https://www.horonim.ru/')
            return "Registration Failed", "Ложись в гроб, в вашем браузере открыта ссылка на ритуальное агентство."
        elif (int(age) <= 0):
            return "Registration Failed", "Возраст больше нуля пожалуйста."
        elif (str(name).isdigit()):
             return "Registration Failed", "Name must not be a number!"
        else:
            # If all fields are filled, proceed with registration (this is where your logic would go)
            print("Name:", name)
            print("Age:", age)
            print("Gender:", gender)
            # Show a success message
            return "Registration Successful", "You have been registered successfully!"
