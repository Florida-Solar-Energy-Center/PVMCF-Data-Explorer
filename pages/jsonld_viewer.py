# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:02:27 2025

@author: Doing
"""

from shiny import ui, render, reactive
import json
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO

def layout():
    return ui.page_fluid(
        ui.h3("🔗 JSON-LD Graph Viewer"),
        ui.input_text_area("jsonld_input", "Paste JSON-LD Content", placeholder="Paste JSON-LD here...", rows=20),
        ui.input_action_button("render_graph", "Render Graph"),
        ui.output_plot("jsonld_graph_plot", height="600px"),
        ui.output_text_verbatim("graph_info")
    )

def server(input, output, session):

    @reactive.Calc
    def parsed_jsonld():
        if not input.jsonld_input():
            return None
        try:
            return json.loads(input.jsonld_input())
        except json.JSONDecodeError as e:
            return {"error": str(e)}

    @output
    @render.plot
    def jsonld_graph_plot():
        data = parsed_jsonld()
        if not data or "error" in data:
            # 🔧 Return an empty placeholder plot instead of None
            fig, ax = plt.subplots()
            ax.axis("off")
            ax.set_title("No graph to display. Paste valid JSON-LD above.")
            return fig
    
        G = nx.DiGraph()
        main_node = data.get("@id", "UnknownModule")
        G.add_node(main_node)
    
        for key, value in data.items():
            if key in ["@context", "@id", "@type"]:
                continue
            G.add_node(f"{key}: {value}")
            G.add_edge(main_node, f"{key}: {value}")
    
        pos = nx.spring_layout(G, seed=42)
        fig, ax = plt.subplots(figsize=(12, 10))
        nx.draw(G, pos, with_labels=True, node_size=500, font_size=8,
                edge_color='gray', node_color='lightblue', ax=ax)
        ax.set_title("JSON-LD Metadata Graph")
        return fig


    @output
    @render.text
    def graph_info():
        data = parsed_jsonld()
        if not data:
            return "Paste JSON-LD to render the graph."
        if "error" in data:
            return f"Error parsing JSON: {data['error']}"
        return f"Parsed {len(data) - 2} fields for module {data.get('@id', 'Unknown')}."

