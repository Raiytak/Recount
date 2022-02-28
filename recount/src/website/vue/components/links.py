import dash_html_components as html
import dash_core_components as dcc

from recount_tools import classproperty


class Links:
    @classproperty
    def home(cls):
        button = html.Button("Home", className="nav-button")
        home_page = dcc.Link(button, className="nav-link", href="/home")
        return home_page

    @classproperty
    def dashboardHome(cls):
        button = html.Button("Dashboard", className="nav-button")
        dashhome = dcc.Link(button, className="nav-link", href="/dashhome")
        return dashhome

    @classproperty
    def notebook(cls):
        button = html.Button("Notebook", className="nav-button")
        notebook = (dcc.Link(button, className="nav-link", href="/excel"),)
        return notebook

    @classproperty
    def categories(cls):
        button = html.Button("Categories", className="nav-button")
        categories = dcc.Link(button, className="nav-link", href="/categories")
        return categories


# class ReusableSingleLinks:
#     def __init__(cls):
#         pass

#     def getLinkPageHome(cls):
#         link_page_home = html.Button("Home", className="header-button")
#         return link_page_home

#     def getLinkPageDashhome(cls):
#         link_page_dashhome = html.Button("Dashboard", className="header-button")
#         return link_page_dashhome

#     def getLinkPageNotebook(cls):
#         link_page_notebook = html.Button("Notebook", className="header-button")
#         return link_page_notebook

#     def getLinkPageCategories(cls):
#         link_page_categories = html.Button("Categories", className="header-button")
#         return link_page_categories

#     def getImageSite(cls):
#         logo_site = html.Img(
#             src="/assets/doit.gif",
#             # height=100,
#         )
#         return logo_site


# class ReusableLinks(ReusableSingleLinks):
#     def __init__(cls):
#         super().__init__()

#     def getLinksDiv(cls):
#         link_page_home = cls.getLinkPageHome()
#         link_page_dashhome = cls.getLinkPageDashhome()
#         # link_page_notebook = cls.getLinkPageNotebook()
#         # link_page_categories = cls.getLinkPageCategories()

#         links_div = html.Nav(
#             children=[
#                 dcc.Link(link_page_home, className="header-link", href="/home"),
#                 dcc.Link(link_page_dashhome, className="header-link", href="/dashhome"),
#                 # dcc.Link(link_page_notebook, className="header-link", href='/excel'),
#                 # dcc.Link(link_page_categories, className="header-link", href='/categories')
#             ],
#             style={
#                 "display": "flex",
#                 "justify-content": "space-between",
#                 "height": "100px",
#             },
#         )
#         return links_div

#     def getLogoDivSite(cls):
#         logo = cls.getImageSite()
#         logo_div = html.A(children=logo, href="/assets/notme.gif")
#         return logo_div

#     def getNavDivSite(cls):
#         links_div = cls.getLinksDiv()

#         header_site = html.Header(children=[links_div], style={"display": "flex"})
#         return header_site
