import csv
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

OUTPUT_FILE = 'papers_data.csv'

categories_with_condition = []
categories_without_condition = []

with open(OUTPUT_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    
    for row in reader:
        if row[2] and row[3]:  
            categories_with_condition.extend([category for category in row[4:14] if category])
        
        categories_without_condition.extend([category for category in row[4:14] if category])


counter_with_condition = Counter(categories_with_condition)
counter_without_condition = Counter(categories_without_condition)


all_categories = list(set(list(counter_with_condition.keys()) + list(counter_without_condition.keys())))


counts_with_condition = [counter_with_condition[category] for category in all_categories]
counts_without_condition = [counter_without_condition[category] for category in all_categories]


plt.figure(figsize=(10, 25))


plt.barh(all_categories, counts_with_condition, color='skyblue', label="With Condition")

plt.barh(all_categories, counts_without_condition, color='salmon', alpha=0.5, label="Without Condition")

plt.xlabel('Frequency')
plt.ylabel('Category')
plt.title('Categories Frequency Distribution')
plt.gca().invert_yaxis()  # To display the category with the highest count at the top
plt.legend()
plt.show()
