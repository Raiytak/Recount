import dash_html_components as html
import dash_core_components as dcc


def getLinksDiv():

    link_page_dashhome = dcc.Link('Go to Page Dashboard Home', href='/dashhome')
    link_page_home = dcc.Link('Go to Page Home', href='/home')
    link_page_themes = dcc.Link('Go to Page Themes', href='/themes')

    links_div = html.Div(children=[
        link_page_home,
        link_page_dashhome,
        link_page_themes
        ],

        style={
            "display":"flex",
            "justify-content":"space-between"}
            )

    return links_div

