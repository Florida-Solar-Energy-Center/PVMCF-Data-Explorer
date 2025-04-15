from pathlib import Path
from shiny import App, ui
from pages import front_page, view_lab_data, search_module, run_analysis, iv_analysis, jsonld_viewer
from sqlite_operations import SQLiteDB
from theme import dark_theme  

SCHEMA_DIR = Path(__file__).parent / "schemas"
DB_PATH = "C:/Users/Doing/University of Central Florida/UCF_Photovoltaics_GRP - module_databases/Complete_Dataset.db"
DB = SQLiteDB(DB_PATH)

app_ui = ui.page_bootstrap(
    dark_theme(),
    ui.page_navbar(
        ui.nav_panel("🏠 Home", front_page.layout(DB)),
        ui.nav_panel("View Data", view_lab_data.layout(DB)),
        ui.nav_panel("Search Modules", search_module.layout(DB)),
        ui.nav_panel("IV Analysis", iv_analysis.layout(DB)),
        ui.nav_panel("Run Analysis", run_analysis.layout(DB)), 
        ui.nav_panel("JSON-LD Viewer", jsonld_viewer.layout()),
        title="🔬 PVMCF Data Explorer",
        id="main_navbar"
    )
)

def server(input, output, session):
    view_lab_data.server(input, output, session, DB)
    search_module.server(input, output, session, DB)
    run_analysis.server(input, output, session, DB)  
    iv_analysis.server(input, output, session, DB) 
    jsonld_viewer.server(input, output, session) 


app = App(app_ui, server)
