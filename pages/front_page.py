from shiny import ui

def layout(db):
    return ui.page_fluid(
        ui.h1("🔆 PVMCF Data Explorer", class_="display-4 mb-4 text-center"),
        ui.p(
            "Welcome! This tool helps you explore photovoltaic module measurements, run analyses, and visualize lab data across characterizations. Get started with the modules below.",
            class_="lead text-center mb-5"
        ),

        ui.accordion(
            ui.accordion_panel(
                "📁 View Lab Data",
                ui.p("Inspect raw database tables from the lab."),
                ui.tags.ul(
                    ui.tags.li("Choose a table to preview recent entries."),
                    ui.tags.li("Displays the last 50 records in descending order."),
                ),
                value="lab-view"
            ),
            ui.accordion_panel(
                "🔍 Module Search",
                ui.p("Search for modules using their ID or serial number. Filter across IV, DIV, EL, IR, UVF, Scanner, and Status characterizations."),
                ui.tags.ul(
                    ui.tags.li("Use comma-separated IDs for batch queries."),
                    ui.tags.li("Download filtered results directly as CSV."),
                ),
                value="search"
            ),
            ui.accordion_panel(
                "📊 IV Parameter Trends",
                ui.p("Visualize trends in IV parameters (Isc, Voc, Rs, etc.) over time."),
                ui.tags.ul(
                    ui.tags.li("Select one or more modules to plot."),
                    ui.tags.li("Choose one or more Y-axis parameters."),
                    ui.tags.li("Use the date range filter to focus on specific time periods."),
                ),
                value="iv-analysis"
            ),
            ui.accordion_panel(
                "🧪 Run Analysis Scripts",
                ui.p("Quickly execute scripted plots and summaries using module metadata."),
                ui.tags.ul(
                    ui.tags.li("Select from predefined analyses like module count by manufacturer."),
                    ui.tags.li("Add your own custom scripts in the backend."),
                ),
                value="analysis"
            )
        
        ),

        ui.div(
            ui.p("🛠️ This app is modular—each tab is easy to maintain and extend. Add new tools or visualizations by including them in the navigation bar."),
            class_="mt-5 text-muted"
        )
    )
