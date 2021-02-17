import unittest
import os

import getpass


import wrapper_excel

username = getpass.getuser()
print(username)


class PathDocs(unittest.TestCase): 
    def test_excel_exists(self):
        ExcelPath = wrapper_excel.paths_docs.ExcelPath()
        path_to_excel = ExcelPath.getRealExcelPath()
        bool_file = os.path.isfile(path_to_excel)
        self.assertTrue(bool_file)
    
    def test_ToT_exists(self):
        DToTPath = wrapper_excel.paths_docs.DescrToThemePath()
        path_to_dtot = DToTPath.getDescriptionToThemePath()
        bool_file = os.path.isfile(path_to_dtot)
        self.assertTrue(bool_file)
    
    def test_TST_auth_exists(self):
        TSTAuthorized = wrapper_excel.paths_docs.ThemesAndSubthemesAuthorized()
        path_to_tst_auth = TSTAuthorized.getTSTPath()
        bool_file = os.path.isfile(path_to_tst_auth)
        self.assertTrue(bool_file)
        
        
        
class AccessDocsExcel(unittest.TestCase):
    def setUp(self):
        self._ExcelPath = wrapper_excel.paths_docs.ExcelPath()
        self.AccessExcel = wrapper_excel.access_docs.AccessExcel(self._ExcelPath)
        self.ExcelToDf = wrapper_excel.access_docs.ExcelToDataframe(self._ExcelPath)
    
    
    def test_copy_excel_to_project(self):
        self.AccessExcel.copyExcelToData()
        bool_file = os.path.isfile(self._ExcelPath.getProjectExcelPath())
        self.assertTrue(bool_file)
    
    # def test_get_df(self):
    #     dataframe = self.ExcelToDf.getDataframe()
    #     self.assertTrue(type(dataframe))

        
# class AccessDocsDToT(unittest.TestCase):
#     def setUp(self):
#         self._DToTPath = wrapper_excel.paths_docs.DescrToThemePath()
#         self.AccessDToT = wrapper_excel.access_docs.AccessDescrToTheme(self._DToTPath)
        
# class AccessDocsTSTAuth(unittest.TestCase):
#     def setUp(self):
#         self._TSTAuthPath = wrapper_excel.paths_docs.ThemesAndSubthemesAuthorized()
#         self.TSTAuth = wrapper_excel.access_docs.AccessExcel(self._TSTAuthPath)

