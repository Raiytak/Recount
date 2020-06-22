import unittest
import os



import paths_docs
import access_docs



class PathDocs(unittest.TestCase): 
    def test_excel_exists(self):
        ExcelPath = paths_docs.ExcelPath()
        path_to_excel = ExcelPath.getRealExcelPath()
        bool_file = os.path.isfile(path_to_excel)
        self.assertTrue(bool_file)
    
    def test_ToT_exists(self):
        DToTPath = paths_docs.DescrToThemePath()
        path_to_dtot = DToTPath.getDescriptionToThemePath()
        bool_file = os.path.isfile(path_to_dtot)
        self.assertTrue(bool_file)
    
    def test_TST_auth_exists(self):
        TSTAuthorized = paths_docs.ThemesAndSubthemesAuthorized()
        path_to_tst_auth = TSTAuthorized.getTSTPath()
        bool_file = os.path.isfile(path_to_tst_auth)
        self.assertTrue(bool_file)
        
        
        
class AccessDocsExcel(unittest.TestCase):
    def setUp(self):
        self._ExcelPath = paths_docs.ExcelPath()
        self.AccessExcel = access_docs.AccessExcel(self._ExcelPath)
        self.ExcelToDf = access_docs.ExcelToDataframe(self._ExcelPath)
    
    
    def test_copy_excel_to_project(self):
        self.AccessExcel.copyExcelToData()
        bool_file = os.path.isfile(self._ExcelPath.getProjectExcelPath())
        self.assertTrue(bool_file)
    
    # def test_get_df(self):
    #     dataframe = self.ExcelToDf.getDataframe()
    #     self.assertTrue(type(dataframe))

        
# class AccessDocsDToT(unittest.TestCase):
#     def setUp(self):
#         self._DToTPath = paths_docs.DescrToThemePath()
#         self.AccessDToT = access_docs.AccessDescrToTheme(self._DToTPath)
        
# class AccessDocsTSTAuth(unittest.TestCase):
#     def setUp(self):
#         self._TSTAuthPath = paths_docs.ThemesAndSubthemesAuthorized()
#         self.TSTAuth = access_docs.AccessExcel(self._TSTAuthPath)

