
### Run python 'filename.py'. python3 doesn't work.

## Run the python script in terminal to run the code in the file.

### To import openpyxl input the following:

```python
from openpyxl import Workbook, load_workbook
```

### Instantiate the workbook

The first thing we do is instantiating the workbook

```python
wb = load_workbook('name of the .xlsx file')
```

Or we could initialise a new workbook

```python
wb = Workbook()
```

### Accessing worksheets to modify them / it

```python
ws = wb.active # This gives the active worksheet from the workbook
```

### Changing the title of worksheets

```python
ws.title = "name"
```

### Accessing individual cell values

to access the cell values of the worksheet, specify which cell you want to look at. 

```python
print(ws['A1'].value)
```

### Changing the cell values 

```python
ws['A2'].value = "new_value"
```

### Saving the workbook

The excel file must be closed in excel in order to save the workbook

```python
wb.save('filename.xlsx')
```

### Creating, Listing and Changing sheets

To see all of the sheets in the workbook run

```python
print(wb.sheetnames)
```

To access a worksheet run 

```python
ws = wb['sheetname']
```

To create a worksheet run

```python
wb.create_sheet("name")
```

### Appending rows of data as a Python list

```python
ws.append(['Tim', 'Is', 'Great'])
```

### Accessing multiple cells

```python
for row in range(1, 11): # loop over the rows
    for col in range(1, 5): # loop over the columns
        # This gives the column letter
        char = get_column_letter(col)
        print(ws[char + str(row)].value) # print values of each cell
```

### Merging cells

```python
ws.merge_cells("A1:D1") # Merges the cells from first cell to specified cell
# Keeps the data from the first cell and gets rid of the rest.
```

### Unmerging cells

```python
ws.unmerge_cells("A1:D1") # un merges the range of cells specified
# But the data of the previous cell that were merged will be lost
```

### Inserting and Deleting rows and columns

Inserting empty rows and columns

```python
ws.insert_rows(7) # Inserts empty row after row 7
ws.insert_cols(2) # Inserts empty col at col 2
```

deleting rows

```python
ws.delete_rows(7) # Deletes row after row 7
ws.delete_cols(2) # Deletes col 2
```

### Copying and Moving cells

Shifting a range of columns to another set of columns and rows
To move up a row requires negative value. To move rows down, requires positive value
To move a column to the right requires a positive value, to move it left, requires a negative value.

```python
ws.move_range("C1:D11", rows=2, cols=2) #
```
