# -*- coding: utf-8 -*-

import numpy as np

from accessors.access_files import AccessCTAuthorized as AccessCTAuthorized


class ReviewerDataframe:
    def __init__(self):
        self._ct_json = AccessCTAuthorized().getJson()

    def checkConformity(self, dataframe):
        pass
        # self.checkCategoryThemes(dataframe)

    def checkCategoryThemes(self, dataframe):
        """This function returns the row only if it recognises the category and theme"""

        def chekCTByRow(row):
            category = row["Category"]
            if (category == str(np.nan)) or (category == "reimbursement"):
                return row
            if category in self._ct_json.keys():
                theme = row["Theme"]
                if (theme in self._ct_json[category]) or (theme == str(np.nan)):
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

        dataframe.apply(chekCTByRow, axis=1)
