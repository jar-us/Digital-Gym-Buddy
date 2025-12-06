import gspread

# Create a connection variable using the service account JSON file
connection = gspread.service_account(filename='../service_account.json')

spreadsheet = connection.open('Gym Data')

wks = spreadsheet.worksheet('Sheet1')

# wks.update_acell('A1', 'Hello, World!')
# wks.update_acell('A2', 'Hello, World! Again!')

cell_value = wks.get("A2")
print(cell_value)  # Output: [['Hello, World!']]

cell_value = wks.acell('A2').value
print(cell_value)

# read entire first row which as a header
header = wks.row_values(1)
print(header)

# append a new row
new_row = ['John Doe', '25', 'M', 'Intermediate']
wks.append_row(new_row)
