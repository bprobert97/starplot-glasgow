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
from datetime import datetime, date
from zoneinfo import ZoneInfo

import streamlit as st

import starplot
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
except Exception as e: # pylint: disable=broad-exception-caught
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

# Extra option: fast vs HD
quality = st.sidebar.radio("Quality", ["Fast (preview)", "HD (slower)"])
RESOLUTION = 1200 if quality == "Fast (preview)" else 2400

# Session state
if "chart_bytes" not in st.session_state:
    st.session_state.chart_bytes = None


# ───────────────────────────────────────────────
# Cached chart generator
# ───────────────────────────────────────────────
@st.cache_data
def generate_chart(plt_type: str,
                   date_time: datetime,
                   mag_lim: int,
                   res: int) -> bytes:
    """
    Generate chart and cache for performance

    Args:
    - plt_type: Either Horizon or Zenith
    - date_time: Datetime for the star plot
    - mag_lim: The maximum magnitude for stars in the plot
    - res: Resolution of the image

    Returns:
    - The image in bytes
    """
    if plt_type == "Horizon":
        return make_horizon_plot(dt=date_time, mag_limit=mag_lim, resolution=res)

    return make_zenith_plot(dt=date_time, mag_limit=mag_lim, resolution=res)


# ───────────────────────────────────────────────
# Generate chart button
# ───────────────────────────────────────────────
if st.sidebar.button("Generate Chart"):
    tz = ZoneInfo("Europe/London")
    dt = datetime.combine(obs_date, obs_time).replace(tzinfo=tz)

    with st.spinner("Generating chart, please wait..."):
        img_bytes = generate_chart(plot_type, dt, mag_limit, RESOLUTION)

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
