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
from starplot import ZenithPlot, Observer, styles, _

# Select timezone, date and time
tz = ZoneInfo("Europe/London")
dt = datetime.now(tz).replace(hour=23, minute=59, second=0)  # or choose a specific time

# Set observer - in this case, Glasgow UK
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

# Create the plot
p = ZenithPlot(
    observer=observer,
    resolution=4000,
    scale=0.9,
    style=style
)

# Generate items on the plot
p.constellations()
p.stars(where=[_.magnitude < 5])       # Limit magnitude as desired
p.horizon()
p.constellation_labels()

# Export image
p.export("images/glasgow_zenith.png", transparent=False)
