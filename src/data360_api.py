import json
import time
import requests
import pandas as pd
from tabulate import tabulate

BASE_URL = "https://data360api.worldbank.org"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "/*",
}

def get_databases(top: int = 100, verbose: bool = True) -> pd.DataFrame:
    """
    Busca todas las bases de datos (type == 'dataset') disponibles en Data360.
    Devuelve un DataFrame con id, nombre y descripción.
    """
    url = f"{BASE_URL}/data360/searchv2"
    payload = {
        "count": True,
        "filter": "type eq 'dataset'",
        "select": "series_description/idno, series_description/name, series_description/database_id",
        "search": "*",
        "top": top,
        "skip": 0,
    }

    resp = requests.post(url, headers=HEADERS, json=payload)

    resp.raise_for_status()
    data = resp.json()

    total = data.get("@odata.count", "?")
    records = data.get("value", [])

    rows = []
    for r in records:
        sd = r.get("series_description", {})
        rows.append({
            "database_id": sd.get("database_id", ""),
            "name":        sd.get("name", "")
        })

    df = pd.DataFrame(rows)

    if verbose:
        print(f"\n{'='*70}")
        print(f"  BASES DE DATOS DISPONIBLES  (total reportado: {total})")
        print(f"{'='*70}")
        print(tabulate(df[["database_id", "name"]], headers="keys",
                       tablefmt="rounded_outline", showindex=False))

    return df


def get_indicators(dataset_id: str, verbose: bool = True) -> pd.DataFrame:
    """
    Lista todos los indicadores disponibles en una base de datos concreta.
    Usa el endpoint /data360/indicators.
    """
    url = f"{BASE_URL}/data360/indicators"
    params = {"datasetId": dataset_id}

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    # El endpoint devuelve una lista de strings o dicts - manejamos ambos
    if isinstance(data, list):
        if data and isinstance(data[0], str):
            rows = [{"indicator_id": v} for v in data]
        else:
            rows = data
    elif isinstance(data, dict):
        rows = data.get("value", data.get("indicators", [data]))
    else:
        rows = []

    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["indicator_id"])

    if verbose:
        print(f"\n{'='*70}")
        print(f"  INDICADORES  →  base de datos: {dataset_id}  ({len(df)} encontrados)")
        print(f"{'='*70}")
        print(tabulate(df.head(30), headers="keys",
                       tablefmt="rounded_outline", showindex=False))
        if len(df) > 30:
            print(f"  ... y {len(df)-30} más.")

    return df


def search_indicators(keyword: str, top: int = 20, topic: str = None,
                      verbose: bool = True) -> pd.DataFrame:
    """
    Busca indicadores por palabra clave.
    Opcionalmente filtra por temática (topic).
    """
    url = f"{BASE_URL}/data360/searchv2"

    filter_parts = ["type eq 'indicator'"]
    if topic:
        filter_parts.append(
            f"series_description/topics/any(t: t/name eq '{topic}')"
        )

    payload = {
        "count": True,
        "filter": " and ".join(filter_parts),
        "select": (
            "series_description/idno, series_description/name, "
            "series_description/database_id, series_description/topics"
        ),
        "search": keyword,
        "top": top,
        "skip": 0,
    }

    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()

    total = data.get("@odata.count", "?")
    records = data.get("value", [])

    rows = []
    for r in records:
        sd = r.get("series_description", {})
        topics_raw = sd.get("topics") or []
        topic_names = ", ".join(t.get("name", "") for t in topics_raw if isinstance(t, dict))
        rows.append({
            "indicator_id": sd.get("idno", ""),
            "name":         sd.get("name", ""),
            "database_id":  sd.get("database_id", ""),
            "topics":       topic_names,
        })

    df = pd.DataFrame(rows)

    if verbose:
        print(f"\n{'='*70}")
        print(f"  BÚSQUEDA: '{keyword}'  |  total reportado: {total}")
        if topic:
            print(f"  Filtro temático: {topic}")
        print(f"{'='*70}")
        print(tabulate(df, headers="keys",
                       tablefmt="rounded_outline", showindex=False))

    return df

def get_indicator_structure(indicator_id: str, database_id: str,
                             sample_rows: int = 5, verbose: bool = True) -> dict:
    """
    Obtiene una muestra de datos para explorar la estructura real de un indicador:
    países disponibles, rango temporal, unidad, frecuencia, etc.
    """
    url = f"{BASE_URL}/data360/data"
    params = {
        "DATABASE_ID": database_id,
        "INDICATOR":   indicator_id,
        "skip":        0,
    }

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    total  = data.get("count", 0)
    values = data.get("value", [])

    if not values:
        if verbose:
            print(f"\n  Sin datos para {indicator_id}")
        return {}

    df = pd.DataFrame(values)

    structure = {
        "indicator_id":  indicator_id,
        "database_id":   database_id,
        "total_records": total,
        "countries":     sorted(df["REF_AREA"].dropna().unique().tolist()),
        "time_range":    (df["TIME_PERIOD"].min(), df["TIME_PERIOD"].max()),
        "frequencies":   df["FREQ"].dropna().unique().tolist(),
        "unit_measures": df["UNIT_MEASURE"].dropna().unique().tolist(),
        "sex_values":    df["SEX"].dropna().unique().tolist(),
        "age_values":    df["AGE"].dropna().unique().tolist(),
        "urbanisation":  df["URBANISATION"].dropna().unique().tolist(),
    }

    if verbose:
        print(f"\n{'='*70}")
        print(f"  ESTRUCTURA  →  {indicator_id}")
        print(f"{'='*70}")
        for k, v in structure.items():
            if isinstance(v, list):
                preview = v[:10]
                extra   = f" ... (+{len(v)-10} más)" if len(v) > 10 else ""
                print(f"  {k:<18}: {preview}{extra}")
            else:
                print(f"  {k:<18}: {v}")

        print(f"\n  Muestra de {sample_rows} registros:")
        print(tabulate(df.head(sample_rows), headers="keys",
                       tablefmt="rounded_outline", showindex=False))

    return structure

def get_indicator_metadata(indicator_id: str, verbose: bool = True) -> dict:
    """
    Recupera la metadata completa de un indicador específico.
    """
    url = f"{BASE_URL}/data360/metadata"
    payload = {
        "query": f"&$filter=series_description/idno eq '{indicator_id}'"
    }

    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()

    records = data.get("value", [data] if isinstance(data, dict) else [])
    meta = records[0] if records else {}

    if verbose:
        print(f"\n{'='*70}")
        print(f"  METADATA  →  {indicator_id}")
        print(f"{'='*70}")
        print(json.dumps(meta, indent=2, ensure_ascii=False)[:3000])

    return meta

def get_disaggregations(indicator_id: str, dataset_id: str,
                         verbose: bool = True) -> dict:
    """
    Devuelve todas las desagregaciones posibles para un indicador dado.
    """
    url = f"{BASE_URL}/data360/disaggregation"
    params = {
        "datasetId":   dataset_id,
        "indicatorId": indicator_id,
    }

    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    if verbose:
        print(f"\n{'='*70}")
        print(f"  DESAGREGACIONES  →  {indicator_id}")
        print(f"{'='*70}")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])

    return data

if __name__ == "__main__":
    databases_df = get_databases(top=50)

    DB = "WB_WDI"
    indicators_df = get_indicators(DB)

    search_indicators("poverty", top=10)
    time.sleep(0.5)

    search_indicators("health", top=10, topic="Health")
    time.sleep(0.5)

    IND = "WB_WDI_SP_POP_TOTL" 
    structure = get_indicator_structure(IND, DB, sample_rows=5)
    time.sleep(0.5)

    meta = get_indicator_metadata(IND)
    time.sleep(0.5)

    disagg = get_disaggregations(IND, DB)
