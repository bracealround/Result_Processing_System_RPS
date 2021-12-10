from decimal import *

# Function for calculating GPA
def calculate_gpa_and_grade(mark):

    if mark <= 100 and mark >= 80:
        return Decimal("4.00"), "A+"

    elif mark < 80 and mark >= 75:
        return Decimal("3.75"), "A"

    elif mark < 75 and mark >= 70:
        return Decimal("3.50"), "A-"

    elif mark < 70 and mark >= 65:
        return Decimal("3.25"), "B+"

    elif mark < 65 and mark >= 60:
        return Decimal("3.00"), "B"

    elif mark < 60 and mark >= 55:
        return Decimal("2.75"), "B-"

    elif mark < 55 and mark >= 50:
        return Decimal("2.50"), "C+"

    elif mark < 50 and mark >= 45:
        return Decimal("2.25"), "C"

    elif mark < 45 and mark >= 40:
        return Decimal("2.00"), "C-"

    elif mark < 40 and mark >= 0:
        return Decimal("0.00"), "F"

    else:
        raise ValueError("The value must be between 0 and 100 inclusive")
