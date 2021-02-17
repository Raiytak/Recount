import os
import io
import base64



class FileSaver():
    def __init__(self, excel_path):
        self.path_to_save = excel_path.getDataPath()
        

    def saveFile(self, csv_file_in_str):
        if csv_file_in_str == None:
            # print("Nothing to register")
            return 0

        content_type, content_string = csv_file_in_str.split(',')
        decoded = base64.b64decode(content_string)
 
        csvFile = io.BytesIO(decoded)

        name_file = 'imported.xlsx'
        path_file = self.path_to_save + "/" + name_file
        
        os.remove(path_file)
        with open(path_file, 'wb') as f:
            f.write(csvFile.read())