from shiny import App, ui
from pages import view_lab_data, search_plot, search_module
from sqlite_operations import SQLiteDB

DB_PATH = "C:/Users/Doing/University of Central Florida/UCF_Photovoltaics_GRP - module_databases/Complete_Dataset.db"
DB = SQLiteDB(DB_PATH)

app_ui = ui.page_navbar(
    ui.nav_panel("View Data", view_lab_data.layout(DB)),
    ui.nav_panel("Search & Plot", search_plot.layout(DB)),
    ui.nav_panel("Search Modules", search_module.layout(DB)),

    title="PVMCF Data Explorer"
)

def server(input, output, session):
    view_lab_data.server(input, output, session, DB)
    search_plot.server(input, output, session, DB)
    search_module.server(input, output, session, DB)


app = App(app_ui, server)
