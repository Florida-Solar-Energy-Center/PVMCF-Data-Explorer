
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 16:54:00 2025
@author: Doing
"""

from shiny import ui, render, reactive
import pandas as pd

def layout(db):
    return ui.page_fluid(
        ui.h3("Module Search Across Characterizations"),
        ui.input_select("search_type", "Search by", choices=["module-id", "serial-number"], selected="module-id"),
        ui.input_text("search_value", "Enter Module ID(s) or Serial Number(s)", placeholder="e.g. 1234, 5678, ABCD"),
        ui.input_action_button("search", "Search"),
        ui.navset_tab(
            ui.nav_panel("IV", ui.output_table("iv_table")),
            ui.nav_panel("DIV", ui.output_table("darkiv_table")),
            ui.nav_panel("EL", ui.output_table("el_table")),
            ui.nav_panel("IR", ui.output_table("ir_table")),
            ui.nav_panel("UVF", ui.output_table("uvf_table")),
            ui.nav_panel("Scanner", ui.output_table("scanner_table"))
        )
    )

def server(input, output, session, db):
    @reactive.Calc
    def search_column():
        return input.search_type()

    @reactive.Calc
    def search_values():
        raw = input.search_value().strip()
        if not raw:
            return []
        return [v.strip() for v in raw.split(",") if v.strip()]

    def query_table(table_name):
        column = search_column()
        values = search_values()
        if values:
            try:
                if len(values) == 1:
                    query = f'WHERE "{column}" = "{values[0]}"'
                else:
                    quoted = ', '.join(f"'{v}'" for v in values)

                    query = f'WHERE "{column}" IN ({quoted})'
                return db.read_records(table_name, '*', query)
            except Exception as e:
                db.handle_error(e, f"Querying {table_name} for {column} in {values}")
                return pd.DataFrame()
        return pd.DataFrame()

    @output
    @render.table
    def iv_table():
        return query_table("sinton-iv-metadata")

    @output
    @render.table
    def darkiv_table():
        return query_table("dark-iv-metadata")

    @output
    @render.table
    def el_table():
        return query_table("el-metadata")

    @output
    @render.table
    def ir_table():
        return query_table("ir-indoor-metadata")

    @output
    @render.table
    def uvf_table():
        return query_table("uvf-indoor-metadata")

    @output
    @render.table
    def scanner_table():
        return query_table("scanner-nc-metadata")
