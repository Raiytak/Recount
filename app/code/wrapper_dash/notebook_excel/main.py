import pandas as pd
import json

# wb = pd.read_excel("/home/mathieu/Desktop/Projets/Comptes/app/code/data/imported_expenses.xlsx")
# wb.to_html("workbook.html")

from xlsx2html import xlsx2html

data_folder = "/home/mathieu/Desktop/Projets/Comptes/app/code/data"
file_input = data_folder+'/copy_expenses.xlsx'
file_output = data_folder+'/xls2html.html'

xlsx2html(file_input, file_output)


import re
def convertHtmlToDynamicHtml(html_file):
    pattern = "<td"
    repl = '<td contenteditable = "true"'

    return re.sub(pattern, repl, html_file)


data = ""

with open(file_output, 'r') as f:
    data = f.read()
data = convertHtmlToDynamicHtml(data)

with open(file_output, 'w') as f:
    f.write(data)
# data