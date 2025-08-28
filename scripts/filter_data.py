#!/usr/bin/env python

# The notebook only uses a subset of published data; for efficiency
# pre-filter to the subset we want to work with so the full
# dataset does not have to be loaded.

import datapackage
import polars as pl
from dplib.plugins.polars.models import PolarsSchema

# load s&co data package file
sco_datapkg = datapackage.Package("public/SCoData_v2.0_2025_datapackage.json")
# get the schema for the events resource and convert to polars
sco_events_pl = PolarsSchema.from_dp(sco_datapkg.get_resource("events").schema)
# this is a PolarsSchema object with a dataframe, which has the schema

sco_events_df = pl.read_csv(
    "public/SCoData_events_v2.0_2025.csv", schema=sco_events_pl.df.schema
)
print(f"SCoData_events_v2.0_2025.csv : {sco_events_df.height:,} rows")

# filter just to borrows
sco_borrows_df = sco_events_df.filter(pl.col("event_type").eq("Borrow"))
print(f"Filtered to borrow events : {sco_borrows_df.height:,} rows")

sco_borrows_df = sco_borrows_df.filter(
    pl.col("start_date").is_not_null(), pl.col("end_date").is_not_null()
)
print(f"Borrow events with start/end dates : {sco_borrows_df.height:,} rows")

# limit the dataframe to relevant fields
sco_borrows_df = sco_borrows_df.select(
    ["start_date", "end_date", "member_names", "item_title", "item_authors"]
)
print("Writing filtered dataset to: public/SCoData_borrows_events.csv")
sco_borrows_df.write_csv("public/SCoData_borrows_events.csv")


pgp_doc_df = pl.read_csv("public/pgp_documents.csv")

print(f"\nPGP documents : {pgp_doc_df.height:,} rows")
# filter just to subset with doc_date_standard
pgp_doc_df = pgp_doc_df.filter(pl.col("doc_date_standard").is_not_null())
print(f"PGP dated documents : {pgp_doc_df.height:,} rows")
# filter by calendar
pgp_doc_df = pgp_doc_df.filter(pl.col("doc_date_calendar").is_in(["Anno Mundi", "Hijrī", "Seleucid"]))
print(f"PGP filtered by calendar : {pgp_doc_df.height:,} rows")

# limit to relevant fields
pgp_doc_df = pgp_doc_df.select(
    "pgpid",
    "shelfmark",
    "type",
    "doc_date_original",
    "doc_date_calendar",
    "doc_date_standard")

print("Writing filtered dataset to: public/pgp_dated_documents.csv")
pgp_doc_df.write_csv("public/pgp_dated_documents.csv")