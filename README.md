# 🔬 PVMCF Data Explorer

A modular Shiny for Python web application for visualizing and analyzing photovoltaic (PV) module measurement data.

---

## 🌟 Features

- **🏠 Home Overview**: Brief descriptions and tips for each tool in the app.
- **📁 View Lab Data**: Browse any table in the SQLite database and preview the latest 50 rows.
- **🔍 Module Search**: Filter data across multiple characterization types (IV, EL, IR, UVF, Scanner, Status) by module ID or serial number, and download results as ZIP or individual CSVs.
- **📊 IV Analysis**: Select one or more modules and track electrical parameters over time with interactive plots.
- ** Run Analysis Scripts**: Run built-in summaries and visual analytics using the `module-metadata` table (e.g., average Voc by model).
- ** JSON-LD Viewer**: Planned extension to explore semantic metadata representations.

---

## 🗂 Project Structure

```
project_root/
│
├── app.py                   # Main application entrypoint
├── sqlite_operations.py     # SQLiteDB utility class
├── pages/
│   ├── front_page.py        # Home page with overview
│   ├── view_lab_data.py     # Raw database viewer
│   ├── search_module.py     # Characterization-based search & download
│   ├── iv_analysis.py       # IV time-series visualization
│   ├── run_analysis.py      # Simple analysis scripts
│   └── jsonld_viewer.py     # [Planned] Graph view for JSON-LD exports
├── theme/                   # Dark mode support (e.g., `theme.py`)
└── Complete_Dataset.db      # SQLite database (not included in repo)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [`shiny`](https://shiny.posit.co/py/docs/) for Python
- `pandas`, `matplotlib`, `sqlite3`

### Installation

```bash
pip install shiny pandas matplotlib
```

### Run the App

```bash
shiny run --reload app.py
```

Make sure to update the `DB_PATH` in `app.py` to your local SQLite file.

---

## 🧐 Notes

- Modular structure means it's easy to extend or debug individual tools.
- Built for use with PVMCF’s `Complete_Dataset.db` structure.
- Includes CSV export, summaries, and plotting tools ready for research documentation or reporting.

---

## 👨‍💻 Author

Brent Thompson  
Florida Solar Energy Center
Photovoltaics Research – University of Central Florida

---

## 📜 License

MIT License

