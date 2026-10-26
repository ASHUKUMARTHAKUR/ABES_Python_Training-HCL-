import numpy as np
import pandas as pd
import math


def _beta_fraction(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c = 1.0
    d = 1.0 - qab * x / qap
    d = 1e-300 if abs(d) < 1e-300 else d
    d = 1.0 / d
    result = d
    for m in range(1, 201):
        m2 = 2 * m
        coefficient = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + coefficient * d
        d = 1e-300 if abs(d) < 1e-300 else d
        c = 1.0 + coefficient / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        result *= d * c
        coefficient = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + coefficient * d
        d = 1e-300 if abs(d) < 1e-300 else d
        c = 1.0 + coefficient / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        change = d * c
        result *= change
        if abs(change - 1.0) < 3e-14:
            break
    return result


def _regularized_beta(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    factor = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1) / (a + b + 2):
        return factor * _beta_fraction(a, b, x) / a
    return 1.0 - factor * _beta_fraction(b, a, 1.0 - x) / b


def _t_cdf(value, df):
    x = df / (df + value * value)
    tail = 0.5 * _regularized_beta(x, df / 2.0, 0.5)
    return 1.0 - tail if value >= 0 else tail


def _t_quantile(probability, df):
    low, high = -100.0, 100.0
    for _ in range(100):
        midpoint = (low + high) / 2.0
        if _t_cdf(midpoint, df) < probability:
            low = midpoint
        else:
            high = midpoint
    return (low + high) / 2.0


def _sem(values):
    return np.std(values, ddof=1) / math.sqrt(len(values))


class _StudentT:
    @staticmethod
    def interval(confidence, df, loc, scale):
        critical = _t_quantile((1.0 + confidence) / 2.0, df)
        return loc - critical * scale, loc + critical * scale


class _Stats:
    t = _StudentT()
    sem = staticmethod(_sem)

    @staticmethod
    def ttest_1samp(values, population_mean):
        values = np.asarray(values, dtype=float)
        df = len(values) - 1
        statistic = (values.mean() - population_mean) / _sem(values)
        p_value = 2.0 * (1.0 - _t_cdf(abs(statistic), df))
        return statistic, p_value

    @staticmethod
    def ttest_ind(first, second):
        first, second = np.asarray(first, dtype=float), np.asarray(second, dtype=float)
        df = len(first) + len(second) - 2
        pooled_variance = (
            (len(first) - 1) * first.var(ddof=1)
            + (len(second) - 1) * second.var(ddof=1)
        ) / df
        standard_error = math.sqrt(pooled_variance * (1 / len(first) + 1 / len(second)))
        statistic = (first.mean() - second.mean()) / standard_error
        p_value = 2.0 * (1.0 - _t_cdf(abs(statistic), df))
        return statistic, p_value


stats = _Stats()

np.random.seed(42)
n = 40
df = pd.DataFrame({
    "Student_ID": range(1, n + 1),
    "Branch": np.random.choice(["CSE", "ECE", "ME", "CE"], n),
    "Study_Hours": np.round(np.random.uniform(1, 8, n), 1),
    "Attendance": np.random.randint(55, 100, n),
})
df["Marks"] = np.clip(
    np.round(30 + 5 * df["Study_Hours" ] + 0.2 * df["Attendance"] + np.random.normal(0, 6, n)),
    0, 100
).astype(int)

df.head()

  # -- TASK 1 --

def get_grade(marks):
  if marks >= 75:
       return 'A'
  elif marks >= 60:
       return 'B'
  elif marks >= 40:
       return 'C'
  else:
       return 'F'
df['Grade'] = df['Marks'].apply(get_grade)

print("Updated DataFrame")
print(df)
print("\n")

print(" Grade Distribution ")
print(df['Grade'].value_counts())

  # -- TASK 2 --

low_attendance_marks = df[df["Attendance"] < 75]["Marks"].tolist()

print("Marks of students with attendance below 75:")
print(low_attendance_marks)


marks_list = df["Marks"].tolist()


high_marks = list(
    filter(lambda mark: mark is not None and mark > 70, marks_list)
)

print(f"\nMarks above 70 ({len(high_marks)} students found):")
print(high_marks)


# -- TASK 3 --

def summary(*values, round_to=2):
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "average": None}

    count = len(values)
    minimum = min(values)
    maximum = max(values)
    average = round(sum(values) / count, round_to)

    return {
        "count": count,
        "minimum": minimum,
        "maximum": maximum,
        "average": average
    }

print("Test 1 Result (10, 20, 30):")
print(summary(10, 20, 30))
print("-" * 30)

test_df = pd.DataFrame({"Marks": [68, 85, 98, 55, 72]})

print("Test 2 Result (test_df['Marks']):")
print(summary(*test_df["Marks"]))

# -- TASK 4 --

def load_data(assignment1):
    try:
        data = pd.read_csv(assignment1)
        return data
    except FileNotFoundError:
        print(f"File not found: {assignment1}")
        return None

print("Wrong File Name")
wrong_df = load_data("wrong_file_name.csv")

# -- TASK 5 --


print("--- Grouping and Sorting Statistics ---")


branch_averages = df.groupby("Branch")[["Marks", "Study_Hours"]].mean()
print("Average Marks and Study Hours by Branch:")
print(branch_averages)
print("\n")


highest_branch = branch_averages["Marks"].idxmax()
highest_avg_mark = branch_averages["Marks"].max()

print(f"Branch with the highest average marks: {highest_branch} (Average: {highest_avg_mark:.2f})")
print("\n")


top_5_students = df.sort_values(by="Marks", ascending=False).head(5)

print("Top 5 Students by Marks:")
print(top_5_students[["Student_ID", "Branch", "Marks", "Grade"]])


# -- TASK 6 --
marks_array = df["Marks"].to_numpy()
z_scores = (marks_array - np.mean(marks_array)) / np.std(marks_array)
students_above_1 = np.sum(z_scores > 1)
print(f"Students with z-score > 1: {students_above_1}")

# -- TASK 7 --
marks_mean = df["Marks"].mean()
marks_median = df["Marks"].median()
marks_mode = df["Marks"].mode()[0]
marks_var = df["Marks"].var()
marks_std = df["Marks"].std()
marks_min = df["Marks"].min()
marks_max = df["Marks"].max()

Q1 = df["Marks"].quantile(0.25)
Q3 = df["Marks"].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR
outliers = df[(df["Marks"] < lower_limit) | (df["Marks"] > upper_limit)]

print(f"Mean: {marks_mean}, Median: {marks_median}, Std: {marks_std}")
print("Explanation: The mean and median indicate the central tendency or typical score of the class, while the standard deviation shows how spread out the marks are from the average.")

# -- TASK 8 --
corr_study = df["Marks"].corr(df["Study_Hours"])
corr_attendance = df["Marks"].corr(df["Attendance"])
print(f"Study Hours Correlation: {corr_study}, Attendance Correlation: {corr_attendance}")
print("Explanation: The relationship with Study Hours is stronger and positive. A high correlation only indicates a numerical pattern, not that one variable directly causes changes in the other, due to potential unseen variables.")

# -- TASK 9 --
ci_95 = stats.t.interval(0.95, df=len(df["Marks"])-1, loc=np.mean(df["Marks"]), scale=stats.sem(df["Marks"]))
print(f"95% Confidence Interval: {ci_95}")
print("Explanation: This interval means we are 95% confident that the true average marks of the entire student population fall within this specific range.")

# -- TASK 10 --
print("H0: The true average marks of students is 60.")
print("H1: The true average marks of students is not 60.")
t_stat_1, p_val_1 = stats.ttest_1samp(df["Marks"], 60)
print(f"P-value: {p_val_1}")
if p_val_1 < 0.05:
    print("Conclusion: Reject H0. There is significant evidence that the average marks are not 60.")
else:
    print("Conclusion: Fail to reject H0. There is not enough evidence to disprove the department's claim that the average is 60.")

# -- TASK 11 --
cse_marks = df[df["Branch"] == "CSE"]["Marks"]
ece_marks = df[df["Branch"] == "ECE"]["Marks"]
print("H0: There is no difference in average marks between CSE and ECE students.")
print("H1: There is a difference in average marks between CSE and ECE students.")
t_stat_2, p_val_2 = stats.ttest_ind(cse_marks, ece_marks)
print(f"P-value: {p_val_2}")
if p_val_2 < 0.05:
    print("Conclusion: Reject H0, meaning there is a significant difference in marks between CSE and ECE.")
else:
    print("Conclusion: Fail to reject H0, meaning there is no significant difference in average marks between the two branches.")

# -- TASK 12 --
print("Summary: The analysis shows that student marks are fairly spread out, with a clear positive trend based on effort. Study hours have the most significant and strongest positive correlation with final marks. Factors like branch do not drastically dictate performance differences compared to individual study habits. Overall, self-study time is the primary factor that matters most for achieving higher marks.")