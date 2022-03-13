from typing import Iterable, List

AVAILABLE_COLORS = [
    "navy",
    "royalblue",
    "lime",
    "crimson",
    "slategray",
    "darkred",
    "khaki",
    "darkgreen",
    "chocolate",
]
EXTRA_COLORS = ["orange", "b", "c", "g", "m", "y", "r", "k"]


def getColors(number_colors: int) -> list:
    number_available_colors = len(AVAILABLE_COLORS)
    if number_available_colors > number_colors:
        return AVAILABLE_COLORS
    available_colors = AVAILABLE_COLORS + EXTRA_COLORS
    number_available_colors = len(available_colors)
    if number_available_colors < number_colors:
        raise AttributeError("Too many colors asked!")
    return available_colors


def scatterGraph(expenses: Iterable, range_date: List[str]):
    list_data = []
    number_colors = len(expenses)
    for dict_exp, color in zip(expenses, getColors(number_colors)):
        dict_exp["mode"] = "markers"
        dict_exp["marker"] = {"color": color}
        dict_exp["hoverinfo"] = "text+y+x"
        list_data.append(dict_exp)
    fig_data = {
        "data": list_data,
        "layout": {
            "title": {"text": "Expenses by category"},
            "yaxis": {"type": "log", "title": "Expenses (euros)"},
            "xaxis": {"title": "Day", "range": range_date},
        },
    }
    return fig_data


def pieGraph(dict_of_expenses: dict):
    number_categories = len(dict_of_expenses["names"])
    dict_of_expenses["type"] = "pie"
    dict_of_expenses["marker"] = {"colors": getColors(number_categories)}
    fig_data = {
        "data": [dict_of_expenses],
        "layout": {"title": {"text": "Pie chart of categories"}},
    }
    return fig_data


def meanGraph(expenses: dict):  # , range_date: List[str]
    list_data = []
    number_colors = len(expenses)
    for dict_exp, color in zip(expenses, getColors(number_colors)):
        dict_exp["type"] = "bar"
        dict_exp["marker"] = {"color": color}
        list_data.append(dict_exp)
    fig_data = {
        "data": list_data,
        "layout": {
            "title": {"text": "Total expenses by week"},
            "barmode": "stack",
            "yaxis": {"title": "Expenses (euros)"},
            # "xaxis": {"title": "Day", "range": range_date},
            "xaxis": {"title": "Day"},
        },
    }
    return fig_data
