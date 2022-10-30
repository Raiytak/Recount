from typing import List
from datetime import datetime

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


def getColors(columns: list):
    nbr_colors = len(columns)
    if len(AVAILABLE_COLORS) + len(EXTRA_COLORS) < nbr_colors:
        raise AttributeError("Too many colors asked!")

    if len(AVAILABLE_COLORS) > nbr_colors:

        available_colors = AVAILABLE_COLORS
    else:
        available_colors = AVAILABLE_COLORS + EXTRA_COLORS

    ordered_columns = columns.copy()
    ordered_columns.sort()
    ordered_index = [columns.index(col) for col in ordered_columns]
    return [available_colors[i] for i in ordered_index]


def scatterGraph(expenses: list, range_date: List[str]):
    data = []
    for dict_exp, color in zip(expenses, getColors([exp["name"] for exp in expenses])):
        dict_exp["mode"] = "markers"
        dict_exp["marker"] = {"color": color}
        dict_exp["hoverinfo"] = "text+y+x"
        data.append(dict_exp)
    fig_data = {
        "data": data,
        "layout": {
            "title": {"text": "Expenses by category"},
            "yaxis": {"type": "log", "title": "Expenses (euros)"},
            "xaxis": {"title": "Day", "range": range_date},
        },
    }
    return fig_data


def pieGraph(expenses: dict):
    expenses["type"] = "pie"
    expenses["marker"] = {"colors": getColors(expenses["names"])}
    fig_data = {
        "data": [expenses],
        "layout": {"title": {"text": "Pie chart of categories"}},
    }
    return fig_data


def meanGraph(expenses: list, range_date: List[datetime]):
    data = []
    for dict_exp, color in zip(expenses, getColors([exp["name"] for exp in expenses])):
        dict_exp["type"] = "bar"
        dict_exp["marker"] = {"color": color}
        dict_exp["hoverinfo"] = "y+name"
        data.append(dict_exp)
    fig_data = {
        "data": data,
        "layout": {
            "title": {"text": "Total expenses by week"},
            "barmode": "stack",
            "yaxis": {"title": "Expenses (euros)"},
            "xaxis": {"title": "Day"},  # , "range": range_date
        },
    }
    return fig_data
