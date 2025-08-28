#!/usr/bin/env python

# The notebook only uses a subset of published data; for efficiency
# pre-filter to the subset we want to work with so the full
# dataset does not have to be loaded.

import polars as pl

import datapackage
from dplib.plugins.polars.models import PolarsSchema

# load s&co data package file
sco_datapkg = datapackage.Package('public/SCoData_v2.0_2025_datapackage.json')
# get the schema for the events resource and convert to polars
sco_events_pl = PolarsSchema.from_dp(sco_datapkg.get_resource('events').schema)
# this is a PolarsSchema object with a dataframe, which has the schema

sco_events_df = pl.read_csv(
    "public/SCoData_events_v2.0_2025.csv", schema=sco_events_pl.df.schema
)
print(f"SCoData_events_v2.0_2025.csv : {sco_events_df.height:,} rows")

# filter just to borrows
sco_borrows_df = sco_events_df.filter(pl.col("event_type").eq("Borrow"))
print(f"Filtered to borrow events : {sco_borrows_df.height:,} rows")

sco_borrows_df = sco_borrows_df.filter(
    pl.col("start_date").is_not_null(),
    pl.col("end_date").is_not_null()
)
print(f"Borrow events with start/end dates : {sco_borrows_df.height:,} rows")

# limit the dataframe to relevant fields
sco_borrows_df = sco_borrows_df.select(
    ["start_date", "end_date", "member_names", "item_title", "item_authors"]
)
print("Writing filtered dataset to: public/SCoData_borrows_events.csv")
sco_borrows_df.write_csv("public/SCoData_borrows_events.csv")

