#Day3 Project -- Simple Calculator Modified

while True:
    try:
        num1 = float(input("Enter a number: "))
        operator = input("Choose an operator: +, -, *, /, **, %: ").strip()
        num2 = float(input(f"Enter a number you want to {operator} to {num1}: "))
    except ValueError:
        print("Invalid input. Please enter numbers.")
        continue
        
    if operator not in ("+", "-", "*", "/", "**", "%"):
        print("Invalid operator. Please enter one of the following: +, -, *, /, **, %")
        continue

    try:
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ZeroDivisionError("You can't divide by zero.")
            result = num1 / num2
        elif operator == "**":
            result = num1 ** num2
        elif operator == "%":
            result = num1 % num2

        print(f"{num1} {operator} {num2} = {result}")
    except ZeroDivisionError as e:
        print(e)
    except OverflowError:
        print("The calculated result is too large to handle!")
        continue

    user_choice = input("Would you like to continue? Enter c to continue, q to quit.").strip().lower()
    if user_choice != "c":
        print("End of calculation.")
        break