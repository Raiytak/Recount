from .__init__ import *

import pandas

import src.access as access
from src.access.path_files import UserFilesPath


# Initialization
USER_ACCESS.removeUserFolder()


def test_instanciate_user_folder():
    user_path = UserFilesPath(USERNAME)
    assert not user_path.pathExists(user_path.user_folder)
    user_access = access.UserFilesAccess(USERNAME)
    assert user_path.pathExists(user_path.user_folder)
    assert user_path.pathExists(user_path.excel)
    assert not user_access.isDecryptedExcelFile(user_path.excel)
    assert user_path.pathExists(user_path.categories)
    assert user_path.pathExists(user_path.intelligent_fill)
    assert user_path.pathExists(user_path.translations)

    user_access.removeUserFolder()
    assert not user_path.pathExists(user_path.user_folder)


def test_initialize_excel():
    USER_ACCESS.removeUserFolder()
    user_path = UserFilesPath(USERNAME)
    user_access = access.UserFilesAccess(USERNAME)

    user_excel = user_access.excel()
    example_excel = user_access.excel(user_path.example_excel)
    assert user_excel == example_excel

    user_df = user_access.dataframe()
    assert type(user_df) == pandas.core.frame.DataFrame


def test_update_files():
    user_access = access.UserFilesAccess(USERNAME)
    user_path = UserFilesPath(USERNAME)

    # Categories part
    categories = user_access.categories
    categories["TEST"] = 2
    user_access.updateCategories(categories)
    updated_categories = user_access.categories
    assert updated_categories == categories

    # Intelligent fill part
    intelligent_fill = user_access.intelligent_fill
    intelligent_fill["TEST"] = 2
    user_access.updateIntelligentFill(intelligent_fill)
    updated_intelligent_fill = user_access.intelligent_fill
    assert updated_intelligent_fill == intelligent_fill

    # Translations part
    translations = user_access.translations
    translations["TEST"] = 2
    user_access.updateTranslations(translations)
    updated_translations = user_access.translations
    assert updated_translations == translations

    # Excel part
    excel_test_name = "test"
    excel_test_path = user_path.formPathUsing(
        user_path.user_folder, excel_test_name + ".xlsx"
    )

    assert not user_path.pathExists(excel_test_path)
    excel = user_access.excel()
    user_access.saveExcel(excel, name=excel_test_name)
    assert user_path.pathExists(excel_test_path)
    assert not user_access.isDecryptedExcelFile(excel_test_path)

    user_access.removeFile(excel_test_path)
    user_pipeline = pipeline.DataPipeline(USERNAME)
    dataframe = user_pipeline.getDataframeFromExcel()

    assert not user_path.pathExists(excel_test_path)
    user_access.saveExcel(dataframe, name=excel_test_name, to_encode=False)
    assert user_path.pathExists(excel_test_path)
    assert user_access.isDecryptedExcelFile(excel_test_path)

