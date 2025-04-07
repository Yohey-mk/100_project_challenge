#day1 project--四則演算プログラム
try:
    num1 = int(input("Enter a first number: "))
    num2 = int(input("Enter a second number: "))
    op = input("Enter an operational mark(+, -, *, /): ")
except ValueError:
    print("Invalid input. Please enter integer numbers only.")
    exit()

if op in ("+", "-", "*", "/"):
    if op == "+":
        calculation_result = num1 + num2
    elif op == "-":
        calculation_result = num1 - num2
    elif op == "*":
        calculation_result = num1 * num2
    elif op == "/" and num2 != 0:
        calculation_result = round(num1 / num2, 2)
    elif op == "/" and num2 == 0:
        print("You can't divide by zero. Please try again with a different number.")
        exit()
else:
    print("Oops! That doesn't seem like a valid operator. Please use one of the following: +, -, *, /.")
    exit()

print(f"Result: {calculation_result}")
