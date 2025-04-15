# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 18:35:39 2025

@author: Doing
"""

from shiny import ui

def dark_theme():
    return ui.tags.head(
        # Load monospace research-style font
        ui.tags.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Fira+Code&display=swap"),

        # Inject CSS for dark theme + photonics vibe
        ui.tags.style("""
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Fira Code', monospace;
            }
            .navbar, .nav-tabs {
                background-color: #1e1e2f !important;
                border-bottom: 1px solid #444;
            }
            .nav-link, .navbar-brand {
                color: #00c9ff !important;
            }
            .nav-link.active {
                background-color: #27293d !important;
                color: #00ffcc !important;
            }
            h1, h2, h3, h4 {
                color: #00ffcc;
                text-shadow: 0 0 5px #0ff;
            }
            .shiny-input-container {
                margin-bottom: 15px;
            }
            .form-control, .btn, .table {
                background-color: #1c1c2b;
                color: #ffffff;
                border: 1px solid #333;
            }
            .btn {
                background-color: #00c9ff;
                color: #121212;
                font-weight: bold;
                box-shadow: 0 0 10px #00c9ff;
            }
            .table {
                border-collapse: collapse;
            }
            .table th, .table td {
                border: 1px solid #333;
                padding: 0.5rem;
            }
        """)
    )