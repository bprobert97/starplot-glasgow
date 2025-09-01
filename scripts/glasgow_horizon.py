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

from datetime import datetime
from zoneinfo import ZoneInfo

from starplot import HorizonPlot, Observer, _
from starplot.styles import PlotStyle, extensions


# Select timezone, date and time
tz = ZoneInfo("Europe/London")
dt = datetime.now(tz).replace(hour=20, minute=29, second=0)  # or choose a specific time

# Set observer - in this case, Glasgow UK
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

# Create plot
p = HorizonPlot(
    altitude=(0, 60),
    azimuth=(135, 225),
    observer=observer,
    style=style,
    resolution=3200,
    scale=0.9,
)

# Add items to plot
p.constellations()
p.milky_way()

p.stars(
    where=[_.magnitude < 5],
    where_labels=[_.magnitude < 2],
    style__marker__symbol="star_4",
)

p.messier(where=[_.magnitude < 11], true_size=False, label_fn=lambda d: f"M{d.m}")

p.constellation_labels()
p.horizon(labels={180: "SOUTH"})

# Export image
p.export("images/glasgow_horizon.png", padding=0.1)