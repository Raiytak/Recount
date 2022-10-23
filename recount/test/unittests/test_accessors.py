from unittest.mock import patch

from .conftest import *

# from recount.src.accessors.__main__ import initializeFolders

# import access as access
# from access.path_files import UserFilesPath


# @patch("os.mkdir")
# def test_create_folders(mock_mkdir):
#     pass


# def test_instanciate_user_folder():
#     user_path = UserFilesPath(USERNAME)
#     assert not user_path.user_folder.exists()
#     user_access = access.UserFolder(USERNAME)
#     assert user_path.user_folder.exists()
#     assert user_path.excel.exists()
#     assert not user_access.isDecryptedExcelFile(user_path.excel)
#     assert user_path.categories.exists()
#     assert user_path.intelligent_fill.exists()
#     assert user_path.translations.exists()

#     user_access.removeUserFolder()
#     assert not user_path.user_folder.exists()


# def test_initialize_excel():
#     USER_ACCESS.removeUserFolder()
#     user_path = UserFilesPath(USERNAME)
#     user_access = access.UserFolder(USERNAME)

#     user_excel = user_access.excel()
#     example_excel = user_access.excel(user_path.example_excel)
#     assert user_excel == example_excel

#     user_df = user_access.dataframe()
#     assert type(user_df) == pandas.core.frame.DataFrame


# def test_update_files():
#     user_access = access.UserFolder(USERNAME)
#     user_path = UserFilesPath(USERNAME)

#     # Categories part
#     categories = user_access.categories
#     categories["TEST"] = 2
#     user_access.updateCategories(categories)
#     updated_categories = user_access.categories
#     assert updated_categories == categories

#     # Intelligent fill part
#     intelligent_fill = user_access.intelligent_fill
#     intelligent_fill["TEST"] = 2
#     user_access.updateIntelligentFill(intelligent_fill)
#     updated_intelligent_fill = user_access.intelligent_fill
#     assert updated_intelligent_fill == intelligent_fill

#     # Translations part
#     translations = user_access.translations
#     translations["TEST"] = 2
#     user_access.updateTranslations(translations)
#     updated_translations = user_access.translations
#     assert updated_translations == translations

#     # Excel part
#     excel_test_name = "test.xlsx"
#     excel_test_path = user_path.user_folder / excel_test_name

#     assert not excel_test_path.exists()
#     excel = user_access.excel()
#     user_access.saveExcel(excel, name=excel_test_name)
#     assert excel_test_path.exists()
#     assert not user_access.isDecryptedExcelFile(excel_test_path)

#     user_access.removeFile(excel_test_path)
#     user_pipeline = pipeline.UserDataPipeline(USERNAME)
#     dataframe = user_pipeline.getDataframeFromExcel()

#     assert not excel_test_path.exists()
#     user_access.saveExcel(dataframe, name=excel_test_name, to_encode=False)
#     assert excel_test_path.exists()
#     assert user_access.isDecryptedExcelFile(excel_test_path)
