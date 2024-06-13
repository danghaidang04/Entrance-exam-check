import pandas as pd

# Assuming you have a DataFrame named df
df = pd.DataFrame(columns=['Column1', 'Column2', 'Column3'])

# Create a new row as a list containing data for each column
new_row = [4, 5.5, 6]  # Replace 'value1', 'value2', 'value3' with your actual data

# Add the new row to the DataFrame using loc
df.loc[len(df)] = new_row
df.loc[len(df)] = [1, 2, 3]
# Print the DataFrame to verify the addition of the new row
print(df)
# store df as a csv file
df.to_csv('dm.csv', index=False)