

class DataframeToGraph(): #main class
    def __init__(self, DataframeToListDict, ListDictToGraph):
        self.DfToLd = DataframeToListDict
        self.LdToGraph = ListDictToGraph
    
    
    def convertDataframeToGraph(self, dataframe, type_graph):
        list_dicts = self.DfToLd.convertDataframeToListOfDicts(dataframe, type_graph)
        graph = self.LdToGraph.getGraph(list_dicts, type_graph)
        return graph
    
    
    