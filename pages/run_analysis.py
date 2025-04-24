# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 13:31:55 2025

@author: Doing
"""

from shiny import ui, render, reactive
from scripts import pixel_metrics

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
        first = pair["tenth_isc"] # Each of these are metadata dictionaries
        second = pair["one_isc"]
        return (
            f"Date: {first['date']} | "
            f"0.1*Isc ID: {first['ID']} Current: {first['current']}| "
            f"Isc ID: {second['ID']} Current: {second['current']}"
        )

    return selected_el_pair

    def prepare_el_image_pairs(selected_pair):
        """
        Takes the selected EL image metadata pair from Shiny app, extracts file paths,
        and runs the pixel metrics pipeline.
        
        Parameters
        ----------
        selected_pair : dict
            A dictionary with keys 'tenth_isc' and 'one_isc' representing image metadata
        
        Returns
        -------
        dict
            Contains rs_values, j0_values, figures, and processed metadata
        """
        if not selected_pair or not all(k in selected_pair for k in ['tenth_isc', 'one_isc']):
            raise ValueError("Selected pair must contain both 'tenth_isc' and 'one_isc' keys.")
    
        filepaths = [
            selected_pair["tenth_isc"]["filename"],
            selected_pair["one_isc"]["filename"]
        ]
    
        # Run the full pixel metrics pipeline
        validated_pair = pixel_metrics.validate_pixel_metrics_pair(filepaths)
        processed = pixel_metrics.process_EL_images_for_pixel_analysis(validated_pair)
        rs_values, j0_values = pixel_metrics.calculate_pixel_metrics(processed)
        figures = pixel_metrics.map_pixel_metrics(rs_values, j0_values)
    
        return {
            "rs_values": rs_values,
            "j0_values": j0_values,
            "figures": figures,
            "processed_metadata": processed
        }

    
        