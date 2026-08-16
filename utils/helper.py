import re


# Function to extract scores written in the x/5 format
def extract_scores(text):
    pattern = r"(\d+(?:\.\d+)?)/5"
    matches = re.findall(pattern, text)

    return [float(score) for score in matches]


# Function to calculate the average AI score as a value between 0 and 1
def calculate_average_score(scores):
    if not scores:
        return 0.0

    average_score = sum(scores) / (5 * len(scores))

    return round(average_score, 4)
