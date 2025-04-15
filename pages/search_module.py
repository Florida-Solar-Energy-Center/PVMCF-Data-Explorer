from shiny import ui, render, reactive
import pandas as pd
import io
import zipfile
import tempfile
import os

def layout(db):
    return ui.page_fluid(
        ui.h3("Module Search Across Characterizations"),

        ui.div(
            ui.input_select("search_type", "Search by", choices=["module-id", "serial-number"], selected="module-id"),
            ui.input_text("search_value", "Enter Module ID(s) or Serial Number(s)", placeholder="FPCAL-0001 or F2405-0001"),
            ui.div(
                ui.input_action_button("search", "Search"),
                ui.download_button("download_all", "Download All as ZIP"),
                class_="d-flex gap-2"
            ),
            class_="mb-3"
        ),

        ui.navset_tab(
            ui.nav_panel("IV", ui.output_table("iv_table"), ui.download_button("download_iv", "Download IV CSV")),
            ui.nav_panel("DIV", ui.output_table("darkiv_table"), ui.download_button("download_darkiv", "Download DIV CSV")),
            ui.nav_panel("EL", ui.output_table("el_table"), ui.download_button("download_el", "Download EL CSV")),
            ui.nav_panel("IR", ui.output_table("ir_table"), ui.download_button("download_ir", "Download IR CSV")),
            ui.nav_panel("UVF", ui.output_table("uvf_table"), ui.download_button("download_uvf", "Download UVF CSV")),
            ui.nav_panel("Scan", ui.output_table("scanner_table"), ui.download_button("download_scanner", "Download Scanner CSV")),
            ui.nav_panel("Status", ui.output_table("status_table"), ui.download_button("download_status", "Download Status CSV"))
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
    @render.download(filename="all_results.zip")
    def download_all():
        with tempfile.TemporaryDirectory() as tmpdir:
            files = {
                "iv_results.csv": query_table("sinton-iv-metadata"),
                "darkiv_results.csv": query_table("dark-iv-metadata"),
                "el_results.csv": query_table("el-metadata"),
                "ir_results.csv": query_table("ir-indoor-metadata"),
                "uvf_results.csv": query_table("uvf-indoor-metadata"),
                "scanner_results.csv": query_table("scanner-nc-metadata"),
                "status_results.csv": query_table("module-status"),
            }

            metadata_df = query_table("module-metadata")

            # Write all CSVs
            zip_path = os.path.join(tmpdir, "all_results.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for name, df in files.items():
                    csv_path = os.path.join(tmpdir, name)
                    df.to_csv(csv_path, index=False)
                    zipf.write(csv_path, arcname=name)

                # Generate README.txt
                readme_lines = ["PVMCF PV Module Data Export\n======================\n"]
                if not metadata_df.empty:
                    for col in ["module-id", "serial-number", "technology", "manufacturer", "location"]:
                        if col in metadata_df.columns:
                            values = metadata_df[col].dropna().unique()
                            readme_lines.append(f"{col}: {', '.join(map(str, values))}")
                    readme_lines.append("")

                for name, df in files.items():
                    readme_lines.append(f"{name}: {len(df)} records")

                readme_path = os.path.join(tmpdir, "README.txt")
                with open(readme_path, "w") as f:
                    f.write("\n".join(readme_lines))
                zipf.write(readme_path, arcname="README.txt")

            with open(zip_path, "rb") as f:
                yield f.read()

    # Output tables (same as before)
    @output
    @render.table
    def iv_table(): return query_table("sinton-iv-metadata")

    @output
    @render.table
    def darkiv_table(): return query_table("dark-iv-metadata")

    @output
    @render.table
    def el_table(): return query_table("el-metadata")

    @output
    @render.table
    def ir_table(): return query_table("ir-indoor-metadata")

    @output
    @render.table
    def uvf_table(): return query_table("uvf-indoor-metadata")

    @output
    @render.table
    def scanner_table(): return query_table("scanner-nc-metadata")

    @output
    @render.table
    def status_table(): return query_table("module-status")
