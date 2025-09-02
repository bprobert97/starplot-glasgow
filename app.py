"""
starplot-glasgow
Author: Beth Probert
Email: beth_probert@outlook.com

Copyright (C) 2025 Beth Probert

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import os
import pathlib
import starplot
import streamlit as st
from datetime import datetime, date
from zoneinfo import ZoneInfo

import starplot.data.constellations as condata
import starplot.data.stars as stardata

from scripts.glasgow_horizon import make_horizon_plot
from scripts.glasgow_zenith import make_zenith_plot

# ───────────────────────────────────────────────
# Setup Starplot writable library (DuckDB extensions etc.)
# ───────────────────────────────────────────────
starplot_writable = pathlib.Path("starplot_library")
os.makedirs(starplot_writable, exist_ok=True)
starplot.data.library_path = starplot_writable

# Preload datasets to avoid slow first-run
try:
    condata.table()
    stardata.table()
except Exception as e:
    print("Warning: preload failed:", e)

# ───────────────────────────────────────────────
# Streamlit App
# ───────────────────────────────────────────────
st.set_page_config(page_title="Glasgow Starplot Viewer", page_icon="🌌")

st.title("🌌 Glasgow Starplot Viewer")

# Sidebar: controls
plot_type = st.sidebar.radio("Select Plot Type", ["Horizon", "Zenith"])
obs_date = st.sidebar.date_input("Date", value=date.today())
obs_time = st.sidebar.time_input("Time", value=datetime.now().time())
mag_limit = st.sidebar.slider("Magnitude Limit", 1, 8, 5)

# Session state to persist chart path
if "chart_bytes" not in st.session_state:
    st.session_state.chart_bytes = None

# ───────────────────────────────────────────────
# Generate chart button
# ───────────────────────────────────────────────
# Generate chart
if st.sidebar.button("Generate Chart"):
    tz = ZoneInfo("Europe/London")
    dt = datetime.combine(obs_date, obs_time).replace(tzinfo=tz)

    with st.spinner("Generating chart, please wait..."):
        if plot_type == "Horizon":
            img_bytes = make_horizon_plot(dt=dt, mag_limit=mag_limit)
        else:
            img_bytes = make_zenith_plot(dt=dt, mag_limit=mag_limit)

    st.session_state.chart_bytes = img_bytes
    st.success("✅ Chart generated!")

# ───────────────────────────────────────────────
# Display chart + download button
# ───────────────────────────────────────────────
if st.session_state.chart_bytes:
    st.image(st.session_state.chart_bytes,
             caption=f"{plot_type} chart from Glasgow")

    st.download_button(
        label="⬇️ Download chart",
        data=st.session_state.chart_bytes,
        file_name=f"glasgow_{plot_type.lower()}.png",
        mime="image/png",
    )
