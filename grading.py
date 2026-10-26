# Grading System
if True:
    grade = int(input("Enter the student's score: "))
    if grade < 0 or grade > 100:
        print("Invalid score. Please enter a score between 0 and 100.")
    elif grade < 40:
        print("Fail")
    elif grade < 50:
        print("D")
    elif grade < 60:
        print("C")
    elif grade < 70:
        print("B")
    else:
        print("A")
