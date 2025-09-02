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

import io
from typing import Optional

from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import HorizonPlot, Observer, _
from starplot.styles import PlotStyle, extensions

def make_horizon_plot(
    dt: Optional[datetime] = None,
    mag_limit: int = 5,
    resolution: int = 1600) -> bytes:
    """
    Generate a horizon star plot.

    Args:
    - dt: The Datetime object representing the desired time for
    the star plot
    - mag_limit: The magitude limit for stars displayed on
    the star plot.
    - resolution: image resolution

    Returns: The image in bytes
    """

    # Default: In Glasgow timezone
    if dt is None:
        tz = ZoneInfo("Europe/London")
        dt = datetime.now(tz)

    # Set observer (Glasgow, UK)
    observer = Observer(
        lat=55.8642,
        lon=-4.2518,
        dt=dt,
    )

    # Select styles
    style = PlotStyle().extend(
        extensions.BLUE_GOLD,
        extensions.MAP,
        extensions.GRADIENT_BOLD_SUNSET,
    )

    # Create horizon plot
    p = HorizonPlot(
        altitude=(0, 60),
        azimuth=(135, 225),
        observer=observer,
        style=style,
        resolution=1600,  # reduce size for faster rendering
        scale=0.9,
    )

    # Add plot elements
    p.constellations()
    p.milky_way()

    p.stars(
        where=[_.magnitude < mag_limit],
        where_labels=[_.magnitude < 2],
        style__marker__symbol="star_4",
    )

    p.messier(where=[_.magnitude < 11], true_size=False, label_fn=lambda d: f"M{d.m}")
    p.constellation_labels()
    p.horizon(labels={180: "SOUTH"})

    # Export to in-memory buffer
    buf = io.BytesIO()
    p.export(buf, format="png", dpi=resolution)
    buf.seek(0)

    return buf.getvalue()  # return PNG bytes
