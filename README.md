# DataPassport LatAm

DataPassport LatAm is an open-source project that transforms World Bank Data360 indicators into a verification-oriented tool for exploring AI readiness across Latin America.

The project began as an academic data visualization assignment and is now being extended into a public-facing MVP focused on information integrity, traceability, and evidence-based storytelling.

## Objective

The goal of this project is to help journalists, researchers, students, and policy analysts explore and verify structural claims about AI readiness in Latin America using transparent, reproducible, and well-documented indicators from the World Bank Data360 API.

Rather than presenting only a static dashboard, the project aims to provide:

- country-level evidence profiles
- transparent comparative views
- interactive visual stories
- shareable “fact passports” with source traceability and methodological notes

## Core Question

How structurally prepared are Latin American countries to adopt and develop AI-related capabilities?

## Data Source

This project uses the **World Bank Data360 API** as its main data source.

Primary dataset:
- **World Development Indicators (WDI)**

Initial indicator set:
- **WB_WDI_IT_NET_USER_ZS** — Individuals using the Internet (% of population)
- **WB_WDI_NY_GDP_PCAP_KD** — GDP per capita (constant 2015 US$)
- **WB_WDI_SE_TER_ENRR** — Tertiary school enrollment
- **WB_WDI_GB_XPD_RSDV_GD_ZS** — Research and development expenditure (% of GDP)
- **WB_WDI_SP_POP_SCIE_RD_P6** — Researchers in R&D (per million people)
- **WB_WDI_TX_VAL_TECH_MF_ZS** — High-technology exports (% of manufactured exports)

These indicators are used to model two interpretable dimensions:
- **AI adoption capacity**
- **AI development capacity**

## Project Status

This repository is currently under active development as an MVP for the Data 360 Global Challenge 2026.

The first public version will focus on:
- Latin America country comparison
- indicator harmonization and documentation
- interactive visualizations
- a country “fact passport” view
- reproducible methodology

## Repository Structure

- `notebooks/` — exploratory notebooks and early analyses
- `src/` — reusable API and data-processing functions
- `app/` — MVP application code
- `data/` — raw and processed datasets
- `docs/` — methodology, roadmap, and project notes

## MVP Roadmap

### Phase 1
- consolidate indicator selection
- build a reproducible ingestion pipeline from the Data360 API
- standardize country-level observations
- document metadata and assumptions

### Phase 2
- implement country comparison logic
- create interpretable evidence profiles
- design the “fact passport” output

### Phase 3
- develop the web-based MVP
- publish documentation and repository instructions
- prepare demo materials

## Academic Origin

This project builds on prior academic work developed in the Master’s program in Data Science at ITBA (Instituto Tecnológico de Buenos Aires), where the team explored the World Bank Data360 API and created interactive visualizations on Latin America’s structural preparedness for AI-related challenges.

## Installation

```bash
pip install -r requirements.txt
```

## Run

For notebooks:

```bash
jupyter notebook
```

Future MVP app:

```bash
streamlit run app/app.py
```

## Open-Source Commitment

The project is being developed as an open, documented, and reproducible resource. Core verification functionality, indicator definitions, and Data360 integration methodology will remain publicly accessible.

## License

To be defined.
