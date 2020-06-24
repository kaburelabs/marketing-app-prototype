import dash_bootstrap_components as dbc
import dash_html_components as html

# Navbar menu options
options = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(
            "Developer Docs", href="#", )),
        # dbc.DropdownMenu(
        #     [
        #         dbc.DropdownMenuItem(
        #             dbc.NavLink("Batter vs Pitcher", href="/static"), className="txt-white"),
        #         dbc.DropdownMenuItem(
        #             dbc.NavLink("Animated", href="/animation"), className="txt-white"),
        #         dbc.DropdownMenuItem(
        #             dbc.NavLink("Developer Version", href="/none-page"), className="txt-white")
        #     ],
        #     label="Predictions",

        #     nav=True
        # ),
        dbc.NavItem(dbc.NavLink("About", href="#")),
        dbc.NavItem(dbc.NavLink(
            "Sign In/Register", href="#")),

    ], className="singlearity-font txt-white font-md",
    navbar=True
)

# Setting Navbar as a function


def navbar(logo="/assets/logo-placeholder.png", height="35px"):

    navbar = dbc.Row(dbc.Col([dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src=logo, style={
                                     "height": height}, className="width-100"),
                            width={"offset": 3, "size": 8}, md={"offset": 0, "size": 8}, lg={"offset": 0, "size": 8},
                            className="logo")
                    ],
                    align="center"
                ),
                href="https://singlearity.ai",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(options, id="navbar-collapse",
                         navbar=True, className="navbar-list"),
        ],
        color="#282828",
        dark=True,
    )], width=12, md=10, lg=10), className="row-center bottom32 navbarColor")

    return navbar
