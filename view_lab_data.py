from shiny import ui, render, reactive

def layout(db):
    table_choices = db.read_records(
        "sqlite_master", "name", "WHERE type='table'"
    )["name"].tolist()

    return ui.page_fluid(
        ui.h3("SQLite Table Viewer"),
        ui.input_select("table", "Choose a table", choices=table_choices),
        ui.output_table("table_view")
    )

def server(input, output, session, db):
    @reactive.Calc
    def selected_table_data():
        return db.read_records(input.table(), "*", "ORDER BY rowid DESC LIMIT 50")

    @output
    @render.table
    def table_view():
        return selected_table_data()
