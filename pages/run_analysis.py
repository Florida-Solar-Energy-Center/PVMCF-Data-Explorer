# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:31:55 2025

@author: Doing
"""

from shiny import ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import io

def layout(db):
    return ui.page_fluid(
        ui.h3("📈 Run Analysis Scripts"),
        ui.input_select("analysis_type", "Choose Analysis", choices=[
            "Module Count by Manufacturer",
            "Average Voc by Model",
            "Custom Script (Placeholder)"
        ]),

        ui.output_plot("analysis_plot", height="400px"),
        ui.output_text_verbatim("analysis_summary")
    )

def server(input, output, session, db):
    @reactive.Calc
    def selected_analysis():
        return input.analysis_type()

    def load_metadata():
        return db.read_records("module-metadata")

    @output
    @render.plot
    def analysis_plot():
        df = load_metadata()
        if df is None or df.empty:
            return
    
        fig, ax = plt.subplots()
        if selected_analysis() == "Module Count by Manufacturer":
            df["make"].value_counts().plot(kind="bar", ax=ax, title="Modules by Manufacturer")
        elif selected_analysis() == "Average Voc by Model":
            if "nameplate-voc" in df.columns and "model" in df.columns:
                # Ensure numeric and drop NaNs
                df = df[["model", "nameplate-voc"]].dropna()
                df["nameplate-voc"] = pd.to_numeric(df["nameplate-voc"], errors="coerce")
                df = df.dropna()
    
                avg_voc = df.groupby("model")["nameplate-voc"].mean().sort_values(ascending=False)
                avg_voc.plot(kind="bar", ax=ax)
                ax.set_title("Average Nameplate Voc by Model")
                ax.set_ylabel("Voc (V)")
                ax.set_xlabel("Model")
            else:
                ax.text(0.5, 0.5, "Required columns not found", ha="center", va="center")
        else:
            ax.text(0.5, 0.5, "Custom script output goes here", ha="center", va="center")
        return fig

    @output
    @render.text
    def analysis_summary():
        df = load_metadata()
        if df is None or df.empty:
            return "No data available."
    
        if selected_analysis() == "Module Count by Manufacturer":
            return df["make"].value_counts().to_string()
        elif selected_analysis() == "Average Voc by Model":
            if "nameplate-voc" in df.columns and "model" in df.columns:
                df = df[["model", "nameplate-voc"]].dropna()
                df["nameplate-voc"] = pd.to_numeric(df["nameplate-voc"], errors="coerce")
                df = df.dropna()
                return df.groupby("model")["nameplate-voc"].mean().sort_values(ascending=False).round(2).to_string()
            return "Required columns not found."
        
        return "Custom script execution results will be shown here."
