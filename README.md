# Undate: computing with uncertain and partially-unknown dates

by Rebecca Sutton Koeser

This notebook provides a demonstration of the functionality
[`Undate` python library](https://github.com/dh-tech/undate-python/).

Undate is an ambitious, in-progress effort to develop a pragmatic Python library for computation and analysis of temporal information in humanistic and cultural data, with a particular emphasis on uncertain, incomplete, or imprecise dates and with support for multiple calendars.

Researchers in the humanities often work with historical or cultural data, and knowing when particular materials were created or events happened is important for understanding the context, interpreting correctly, and determining relationships and sequencing. However, these kind of materials rarely have full precision dates with known year, month, and day. In some contexts, scholars may be happy if they can determine even just a century based on handwriting or mentions of historic coins.

Humanistic and cultural data also often includes dates in different calendars, or even a mix of calendars within the same project or system. It's important to preserve the original date and calendar information, but it's also valuable to convert dates to a standard calendar so they can be compared and sorted together. `Undate` objects are calendar aware and calendar explicit, with a default of the Gregorian calendar. Currently, we support parsing and calendar conversion for dates in the Hebrew `Anno Mundi` calendar and Islamic `Hijri` calendar.

This notebook demonstrates current use and functionality of the core `Undate` and `UndateInterval` objects, along with some examples showing use-cases from two projects that fed into development on `undate`: [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/), and [Princeton Geniza Project](https://geniza.princeton.edu/).

*This is a notebook submission for US-RSE'25.*

## Instructions

- Create a python virtual environment with python version 3.12
- Run `pip install -r requirements.txt` install python dependencies
- Run `jupyter notebook undate-overview.ipynb` to start the notebook.
