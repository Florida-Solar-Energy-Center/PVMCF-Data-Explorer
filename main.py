# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 19:11:32 2025

@author: Doing
"""

# openapi_app/main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
import uvicorn
import tempfile
import os

from sqlite_operations import SQLiteDB
import zipfile

app = FastAPI(title="PVMCF OpenAPI", version="1.0")
db = SQLiteDB("C:/Users/Doing/University of Central Florida/UCF_Photovoltaics_GRP - module_databases/Complete_Dataset.db")  # Replace with your SQLite file path

tables = {
    "iv": "sinton-iv-metadata",
    "darkiv": "dark-iv-metadata",
    "el": "el-metadata",
    "ir": "ir-indoor-metadata",
    "uvf": "uvf-indoor-metadata",
    "scanner": "scanner-nc-metadata",
    "status": "module-status",
    "metadata": "module-metadata"
}

@app.get("/search", summary="Query module data across tables")
def search_modules(
    search_type: str = Query("module-id", enum=["module-id", "serial-number"]),
    values: List[str] = Query(...)
):
    try:
        results = {}
        quoted_values = ', '.join(f"'{v}'" for v in values)
        query = f'WHERE "{search_type}" IN ({quoted_values})'

        for key, table in tables.items():
            df = db.read_records(table, '*', query)
            results[key] = df.to_dict(orient="records")

        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download", summary="Download module data as ZIP")
def download_modules(
    search_type: str = Query("module-id", enum=["module-id", "serial-number"]),
    values: List[str] = Query(...)
):
    try:
        quoted_values = ', '.join(f"'{v}'" for v in values)
        query = f'WHERE "{search_type}" IN ({quoted_values})'

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "pv_results.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                readme_lines = ["PVMCF PV Module Data Export\n==========================\n"]
                for key, table in tables.items():
                    df = db.read_records(table, '*', query)
                    if df is not None and not df.empty:
                        csv_name = f"{key}_results.csv"
                        csv_path = os.path.join(tmpdir, csv_name)
                        df.to_csv(csv_path, index=False)
                        zipf.write(csv_path, arcname=csv_name)
                        readme_lines.append(f"{csv_name}: {len(df)} records")
                readme_path = os.path.join(tmpdir, "README.txt")
                with open(readme_path, "w") as f:
                    f.write('\n'.join(readme_lines))
                zipf.write(readme_path, arcname="README.txt")
            return FileResponse(zip_path, filename="pv_results.zip", media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional local run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
