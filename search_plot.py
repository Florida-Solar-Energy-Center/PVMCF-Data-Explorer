from shiny import ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Hypothetical simplified layout
def layout(db):
    return ui.page_fluid(
        ui.h3("Simple Data Plotting"),
        ui.input_select("plot_table", "Select Table", choices=[]),
        # Instead of separate column selection and plot type, combine them conceptually
        ui.input_selectize("plot_variables", "Select Variable(s) for Plotting", choices=[], multiple=True),
        ui.output_plot("simple_plot_preview", height="400px")
    )

def server(input, output, session, db):
    # Populate tables on load (same as before)
    @reactive.Effect
    def _populate_tables():
        tables = db.read_records(
            "sqlite_master", "name", "WHERE type='table'"
        )["name"].tolist()
        ui.update_select("plot_table", choices=tables)

    # Update column choices when table is selected (renamed for clarity)
    @reactive.Effect
    def _update_plot_variables():
        if not input.plot_table():
            return
        df = db.read_records(input.plot_table(), "*", "LIMIT 1")
        ui.update_selectize("plot_variables", choices=list(df.columns))

    @reactive.Calc
    def selected_data_simple():
        if not input.plot_table() or not input.plot_variables():
            return pd.DataFrame()
        columns = input.plot_variables()
        return db.read_records(input.plot_table(), columns)

    @output
    @render.plot
    def simple_plot_preview():
        df = selected_data_simple()
        if df.empty or not input.plot_variables():
            return

        cols = input.plot_variables()
        fig, ax = plt.subplots()

        # Simple logic to infer plot type (this is a basic example)
        if len(cols) == 1:
            # Default to histogram for single numerical variable
            if pd.api.types.is_numeric_dtype(df[cols]):
                df[cols].dropna().plot.hist(ax=ax, bins=15, edgecolor="black", alpha=0.7)
                ax.set_title(f"Histogram of {cols}")
            else:
                ax.text(0.5, 0.5, f"Cannot create default plot for non-numeric column: {cols}", ha='center', va='center')
        elif len(cols) == 2:
            # Default to scatter plot for two numerical variables
            if all(pd.api.types.is_numeric_dtype(df[col]) for col in cols):
                x, y = cols
                ax.scatter(df[x], df[y], alpha=0.7)
                ax.set_xlabel(x)
                ax.set_ylabel(y)
                ax.set_title(f"Scatter Plot of {x} vs {y}")
            else:
                ax.text(0.5, 0.5, "Select two numeric columns for a scatter plot", ha='center', va='center')
        elif len(cols) > 2:
            ax.text(0.5, 0.5, "Select one or two columns for a simple default plot.", ha='center', va='center')
        else:
            return

        plt.tight_layout()
        return fig