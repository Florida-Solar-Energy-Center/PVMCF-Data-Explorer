# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:31:55 2025

@author: Doing
"""

from shiny import ui, render, reactive

def layout(db):
    return ui.page_fluid(
        ui.h3("🔬 Sequential EL Pair Selector"),
        ui.input_text("el_module_id", "Enter Module ID", placeholder="e.g., FPCAL-0001"),
        ui.input_action_button("fetch_el_pairs", "Fetch EL Pairs"),
        ui.output_ui("el_slider_ui"),
        ui.output_text_verbatim("selected_pair_summary")
    )

def server(input, output, session, db):

    @reactive.Calc
    def el_pairs_dict():
        input.fetch_el_pairs()
        module_id = input.el_module_id()
        if not module_id:
            return {}
        return db.get_el_pairs(module_id)

    @reactive.Calc
    def available_pair_dates():
        data = el_pairs_dict()
        if not isinstance(data, dict) or "message" in data or "error" in data:
            return []
        return sorted(data.keys())  # Sort the dictionary keys (dates)

    @output
    @render.ui
    def el_slider_ui():
        dates = available_pair_dates()
        if not dates:
            return ui.p("No EL pairs found.")
        return ui.input_select("el_pair_date", "Select EL Pair by Date", choices=dates)

    @reactive.Calc
    def selected_el_pair():
        data = el_pairs_dict()
        selected_date = input.el_pair_date()
        if not selected_date or selected_date not in data:
            return None
        return data[selected_date]

    @render.text
    def selected_pair_summary():
        pair = selected_el_pair()
        if pair is None:
            return "No EL pair selected."
        first = pair["tenth_isc"]
        second = pair["one_isc"]
        return (
            f"Date: {first['date']} | "
            f"0.1*Isc ID: {first['ID']} Current: {first['current']} | "
            f"Isc ID: {second['ID']} Current: {second['current']}"
        )

    return selected_el_pair

