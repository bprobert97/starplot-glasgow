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
import tempfile
import starplot
import streamlit as st
from datetime import datetime, date
from zoneinfo import ZoneInfo
from scripts.glasgow_horizon import make_horizon_plot
from scripts.glasgow_zenith import make_zenith_plot

# Override the library path
starplot_library_dir = pathlib.Path(tempfile.gettempdir()) / "starplot_library"
os.makedirs(starplot_library_dir, exist_ok=True)
starplot.data.library_path = starplot_library_dir


st.title("🌌 Glasgow Starplot Viewer")

# Sidebar: Plot type
plot_type = st.sidebar.radio("Select Plot Type", ["Horizon", "Zenith"])

# Sidebar: Date and time
obs_date = st.sidebar.date_input("Date", value=date.today())
obs_time = st.sidebar.time_input("Time", value=datetime.now().time())

# Magnitude limit (stars)
mag_limit = st.sidebar.slider("Magnitude Limit", 1, 8, 5)

# Ensure image remains displayed when download button pressed
if "chart_path" not in st.session_state:
    st.session_state.chart_path = None

# Generate chart
if st.sidebar.button("Generate Chart"):
    tz = ZoneInfo("Europe/London")
    dt = datetime.combine(obs_date, obs_time).replace(tzinfo=tz)

    with st.spinner("Generating chart, please wait..."):
        if plot_type == "Horizon":
            path = make_horizon_plot(output_path="images/glasgow_horizon.png", dt=dt, mag_limit=mag_limit)
        else:
            path = make_zenith_plot(output_path="images/glasgow_zenith.png", dt=dt, mag_limit=mag_limit)

    st.session_state.chart_path = path  # store path in session state
    st.success("Chart generated!")

# Display the image if it exists in session state
if st.session_state.chart_path:
    st.image(st.session_state.chart_path, caption=f"{plot_type} chart from Glasgow", width="content")

    with open(st.session_state.chart_path, "rb") as f:
        st.download_button(
            label="Download chart",
            data=f,
            file_name=f"glasgow_{plot_type.lower()}.png",
            mime="image/png"
        )
