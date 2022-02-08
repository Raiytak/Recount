# -*- coding: utf-8 -*-
""" 
                    ====     DESCRIPTION    ====
Assert that the categories and themes used in the analysed excel are present
in the dat_theme_authorized file.
"""

import numpy as np

import access

AUTHORIZED_CATEGORIES = access.AccessUserFiles.categoriesAuthorized


# TODO : Improve readability and usefulness of this function
# TODO: make this function work
def checkConformity(self, dataframe):
    """This function returns the row only if it recognises the category and theme"""

    def chekCTByRow(row):
        category = row["Category"]
        if (category == str(np.nan)) or (category == "reimbursement"):
            return row
        if category in AUTHORIZED_CATEGORIES.keys():
            theme = row["Theme"]
            if (theme in AUTHORIZED_CATEGORIES[category]) or (theme == str(np.nan)):
                return row
            raise Exception(
                "ERROR THEME : In row "
                + row["ID"]
                + "orthograph error in theme : "
                + row["Theme"]
            )
        raise Exception(
            "ERROR CATEGORY : In row "
            + row["ID"]
            + "orthograph error in category : "
            + row["Category"]
        )

    # dataframe.apply(chekCTByRow, axis=1)
    pass
