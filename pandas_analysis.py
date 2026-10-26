# import pandas as pd
# # import numpy as np
# # Step 2: Create Pandas Series

# salary_series = pd.Series([65000, 58000, 80000, 85000, 68000, 90000, 76000])
# # print("=================salary_series===================")
# # print(salary_series)

# print("===================Defining Properties==================")
# # Check properties:

# print(salary_series.index)
# print(salary_series.values)
# print(salary_series.dtype)

# # Step 3: Series with Custom Index



import pandas as pd
import numpy as np
salary_series=pd.Series([65000,58000,85000,90000,75000])
print("===salary_series===")
print(salary_series)

employee_data = {
    'EmployeeID': [101, 102, 103, 104, 105],
    'Employee_Name': ['John', 'Jane', 'Doe', 'Smith', 'Alice'],
    'Department': ['HR', 'Finance', 'IT', 'Marketing', 'Sales'],
    'Salary': [65000, 58000, 85000, 90000, 75000],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'experience': [5, 3, 8, 6, 4],
    'rating': [4.5, 4.2, 4.8, 4.1, 4.3]

}
print("===employee_data===")
employee_df=pd.DataFrame(employee_data)
print(employee_df)


