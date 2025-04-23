from shiny import ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

def layout(db):
    return ui.page_fluid(
        ui.h3("📈 IV Parameter Over Time"),
        ui.input_selectize("iv_module_select", "Select Module(s)", choices=[], multiple=True),
        ui.input_selectize("iv_y_params", "Select Y-axis Parameter(s)", choices=[], multiple=True),
        ui.input_date_range("iv_date_range", "Select Date Range", start=None, end=None),
        ui.output_plot("iv_param_plot", height="500px"),
        ui.output_text_verbatim("iv_param_summary")
    )

def server(input, output, session, db):

    @reactive.Calc
    def iv_df():
        df = db.read_records("sinton_normalized")
        if df is not None:
            df = df.dropna(subset=["Measurement_Date-Time", "module-id"])
            df["Measurement_Date-Time"] = pd.to_datetime(df["Measurement_Date-Time"], errors="coerce")
        return df

    @reactive.Effect
    def _update_module_choices():
        df = iv_df()
        if df is not None and not df.empty:
            module_ids = sorted(df["module-id"].dropna().unique())
            ui.update_select("iv_module_select", choices=["All"] + module_ids, selected="All")
    
    @reactive.Effect
    def _set_default_date_range():
        df = iv_df()
        if df is not None and not df.empty:
            start = df["Measurement_Date-Time"].min()
            end = df["Measurement_Date-Time"].max()
            ui.update_date_range("iv_date_range", start=start, end=end)

    @reactive.Effect
    def _update_param_choices():
        df = iv_df()
        if df is not None and not df.empty:
            # Detect potential numeric columns (try convert first 100 rows)
            numeric_candidates = []
            for col in df.columns:
                try:
                    pd.to_numeric(df[col].dropna().head(100))
                    numeric_candidates.append(col)
                except ValueError:
                    continue
            ui.update_selectize("iv_y_params", choices=numeric_candidates)
    
    @render.plot
    def iv_param_plot():
        df = iv_df()
        if df is None or df.empty:
            return
    
        selected_modules = input.iv_module_select()
        y_cols = input.iv_y_params()
        date_range = input.iv_date_range()
    
        if not selected_modules or not y_cols or not date_range:
            return
    
        df = df[df["module-id"].isin(selected_modules)]
    
        # Filter by date range
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["Measurement_Date-Time"] >= start_date) & (df["Measurement_Date-Time"] <= end_date)]
        df = df.sort_values("Measurement_Date-Time")
    
        plt.figure(figsize=(12, 6))
        for module in selected_modules:
            df_mod = df[df["module-id"] == module]
            for col in y_cols:
                try:
                    y = pd.to_numeric(df_mod[col], errors="coerce")
                    plt.plot(df_mod["Measurement_Date-Time"], y, marker='o', label=f"{module} - {col}")
                except Exception as e:
                    print(f"Skipping {col} for {module}: {e}")
    
        plt.xlabel("Measurement Date-Time")
        if len(y_cols) == 1:
            plt.ylabel(y_cols[0])
        else:
            plt.ylabel("Selected Parameters")
        plt.title(f"Modules: {', '.join(selected_modules)}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()


    @render.text
    def iv_param_summary():
            modules = input.iv_module_select()
            y_cols = input.iv_y_params()
            return f"Showing parameters: {', '.join(y_cols)} for modules: {', '.join(modules)}"