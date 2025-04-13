# PVMCF-Data-Explorer
# 🔆 Photovoltaic Module Database Viewer

This is a modular Python web app built using [Shiny for Python](https://shiny.posit.co/py/) for viewing, searching, and visualizing photovoltaic (PV) module data stored in an SQLite database.

## 📚 Features

- 🔍 **Search by Serial Number or Module ID** across all characterization tables (IV, EL, IR, etc.)
- 📈 **Dynamic Plotting** from any table with flexible column selection (line, scatter, histogram)
- 🧮 **Multi-tab Interface** for viewing, searching, plotting, and tool integration
- 🗃️ Uses a centralized `SQLiteDB` class to handle database read/write, logging, and table joins
- 🧠 Designed for research teams analyzing solar panel reliability and multimodal measurements

---

## 🏗️ Project Structure

```text
project-root/
│
├── app.py                     # Main Shiny app entrypoint
├── sqlite_operations.py       # Modular SQLiteDB class
├── pages/
│   ├── view_data.py           # Table viewer tab
│   ├── search_plot.py         # Search and plot interface
│   └── tools.py               # Search by Module ID or serial numbers
│
├── Complete_Dataset.db        # SQLite database (add your own path)
└── README.md                  # You're here
