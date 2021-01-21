import pandas as pd

df = pd.read_csv('jeopardy.csv')

# Fixing column names
df.rename(columns ={' Air Date': 'Air Date', ' Round': 'Round', ' Category': 'Category', ' Value': 'Value', ' Question': 'Question', ' Answer': 'Answer'}, inplace=True)

# Display the full contents of a column
pd.set_option('display.max_colwidth', None)
# print(df.Question.head(5))


# Write a function that filters the dataset for questions that contains all of the words in a list of words
def filter_data(data, lst):
# Lowercases all words in the list of words as well as the questions
# Returns true if all of the words in the list appear in the question
  filter = lambda question: all(word.lower() in question.lower() for word in lst)
  # Apply the filter to every question and return the filtered dataset
  return data[data["Question"].apply(filter)].reset_index()

# Test the function
filtered_data = filter_data(df, ["King", "England"])
# print(filtered_data.Question)

# Removing the dollar sign and commas from the string values in value collumn
df['Value'] = df.Value.apply(lambda value: value.replace('$', '').replace(',','') if value != 'None' else 0)
# Convert the string values of Value column to float
df['Float Value'] = df['Value'].astype(float)


# The average value of questions that contain the word King
# We will use the filtered df for the word King
filtered_df = filter_data(df, ["King"])
# Average value for the filtered df
mean_value = filtered_df['Float Value'].mean()
# print(mean_values) 

# Count of unique answers to all of the questions in a dataset
def count_unique_answers(data):
  return data.Answer.value_counts()

# Count of unique answers of the filtered_df
# print(count_unique_answers(filtered_df))  

# Investigate the ways in which questions change over time by filtering by the date.
# How many questions from the 90s use the word 'Computer' compared to questions from 2000s?
filtered_data_90s = df[df['Air Date'].str.startswith('199') & df.Question.str.contains('computer')]
filtered_data_00s = df[df['Air Date'].str.startswith('200') & df.Question.str.contains('computer')]  
# print(filtered_data_90s.Question.count(), filtered_data_00s.Question.count())

# Is there a connection between the round and the category? 
# print(df.Round.head(40))
# print(df.Category.head(40))
# Answer: The categories in Single Jeopardy are different from the ones in Double Jeopardy

# Are you more likely to find certain categories, like "Literature" in Single Jeopardy or Double Jeopardy?
df1 = df.groupby(['Round', 'Category']).Question.count().reset_index()
maxcount = df1[df1.Category == 'LITERATURE'].Question.max()
# print(df1[df1.Question == maxcount])

# Build a system to quiz the user 
# Grab random questions, and use the input function to get a response from the user 
# Check to see if that response was right or wrong
def quiz():
  
  money = 0

  while True:

    # Generate a row from DataFrame randomly 
    random_row = df.sample()
    # Isolate the question, answer and value, convert it to string and remove the index
    random_quest = random_row.Question.to_string().split()
    answer = random_row.Answer.to_string().split()
    value = random_row['Float Value'].to_string().split()
    del(random_quest[0])
    del(answer[0])
    del(value[0])
    random_quest = " ".join(random_quest) 
    answer = " ".join(answer)
    value = " ".join(value)
    value = float(value)

    # Get user response
    user_response = input('Question: %s \nAnswer: ' %random_quest)
    # if the user response is correct the quiz will continue
    if user_response.lower() in answer.lower():
      print('That is correct!!!\nYou gain %.1f dollars.\n' % value)
      money += value
      print('Your current amount of money is %.1f dollars.\n' % money)
      continue
    # if the user's answer is incorrect the quiz stops and the user has to run the program again
    else:
      return 'Wrong answer. The correct answer is %s' % answer
 
       
print(quiz())







  








