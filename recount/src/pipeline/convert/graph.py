from accessors.access_files import AccessCTAuthorized

myAccessCTAuthorized = AccessCTAuthorized()
from wrapper_dash.facilitator_dash.convert_ld_to_graph import ListDictToGraph
from wrapper_dash.facilitator_dash.convert_df_to_ld import DataframeToListOfDicts


class DataframeToGraph:  # main class
    def __init__(self):
        authorizedCT_json = myAccessCTAuthorized.getJson()

        self.DfToLd = DataframeToListOfDicts()
        self.LdToGraph = ListDictToGraph(authorizedCT_json)

    def convertDataframeToGraph(self, dataframe, type_graph, range_date=""):
        list_dicts = self.DfToLd.convertDataframeToListOfDicts(dataframe, type_graph)
        graph = self.LdToGraph.getGraph(list_dicts, type_graph, range_date)
        return graph
