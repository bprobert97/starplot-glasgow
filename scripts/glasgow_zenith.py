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
from typing import Optional

from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import ZenithPlot, Observer, styles, _


def make_zenith_plot(
    output_path="images/glasgow_zenith.png",
    dt: Optional[datetime] = None,
    mag_limit: int = 5) -> str:
    """
    Generate a zenith star ploy

    Args:
    - output_path: The path the image will be exported to.
    - dt: The Datetime object representing the desired time for
    the star plot
    - mag_limit: The magitude limit for stars displayed on
    the star plot.

    Returns: The path for the created image.
    """

    # Ensure images folder exists
    os.makedirs("images", exist_ok=True)

    # Default: now in Glasgow timezone
    if dt is None:
        tz = ZoneInfo("Europe/London")
        dt = datetime.now(tz)

    # Set observer (Glasgow, UK)
    observer = Observer(
        dt=dt,
        lat=55.8642,
        lon=-4.2518,
    )

    # Select styles
    style = styles.PlotStyle().extend(
        styles.extensions.BLUE_NIGHT,
        styles.extensions.GRADIENT_PRE_DAWN
    )

    # Create Zenith plot
    p = ZenithPlot(
        observer=observer,
        resolution=1600,  # smaller for faster rendering
        scale=0.9,
        style=style
    )

    # Generate plot elements
    p.constellations()
    p.stars(where=[_.magnitude < mag_limit])
    p.horizon()
    p.constellation_labels()

    # Export image
    p.export(output_path, transparent=False)

    return output_path

