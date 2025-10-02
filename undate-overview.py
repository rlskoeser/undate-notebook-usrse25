import marimo

__generated_with = "0.16.5"
app = marimo.App(
    width="medium",
    app_title="Undate: computing with uncertain and partially-unknown dates",
    layout_file="layouts/undate-overview.slides.json",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd  # for min/max date range
    import altair as alt

    # path to public directory relative to this notebook
    NOTEBOOK_PUBLIC_DIR = mo.notebook_location() / "public"
    return NOTEBOOK_PUBLIC_DIR, alt, mo, pd


@app.cell(hide_code=True)
async def _():
    import sys

    # when running under WASM, use micropip to install necessary dependencies
    if sys.platform == "emscripten":
        import micropip

        await micropip.install("polars")
        # PyMeeus is a dependency of convertdate; for some reason micropip can't install it automatically
        await micropip.install(
            "https://www.piwheels.org/simple/pymeeus/PyMeeus-0.5.12-py3-none-any.whl#sha256=3fb4b35e1efa77bcde9c858f5749f2eb0b315a53caba7825d25b89cf24c1b47f"
        )
        await micropip.install("undate")

    import polars as pl

    from undate import __version__ as undate_version
    return pl, undate_version


@app.cell(hide_code=True)
def _(mo, undate_version):
    mo.vstack(
        [
            mo.md(
                f"""
    # Undate: computing with uncertain and partially-unknown dates

    `Undate` is an **ambitious, in-progress effort** to develop a **pragmatic Python library** for computation and analysis of temporal information in humanistic and cultural data, with a particular emphasis on **uncertain, incomplete, or imprecise dates** and with support for **multiple calendars**.

    Researchers in the humanities often work with historical or cultural data, and knowing when particular materials were created or events happened is important for understanding the context, interpreting correctly, and determining relationships and sequencing. However, these kind of materials rarely have full precision dates with known year, month, and day. In some contexts, scholars may be happy if they can determine even just a century based on handwriting or mentions of historic coins.

    Humanistic and cultural data also often includes dates in different calendars, or even a mix of calendars within the same project or system. It's important to preserve the original date and calendar information, but it's also valuable to convert dates to a standard calendar so they can be compared and sorted together. `Undate` objects are calendar aware and calendar explicit, with a default of the Gregorian calendar. Currently, we support parsing and calendar conversion for dates in the Hebrew _Anno Mundi_ calendar and Islamic _Hijri_ calendar.

    This notebook demonstrates current use and functionality of the core `Undate` and `UndateInterval` objects, along with some examples and use-cases from specific projects.


    ----"""
            ),
            mo.hstack(
                [
                    mo.md("""**Rebecca Sutton Koeser**<br/>
    Lead Research Software Engineer, Center for Digital Humanities @ Princeton</br>
    *US-RSE'25 notebook presentation* | available online: [https://rlskoeser.github.io/undate-notebook-usrse25/](https://rlskoeser.github.io/undate-notebook-usrse25/)
            """),
                    mo.md(f"""`undate` v{undate_version}                """),
                ],
                justify="space-between",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Basic functionality

    Like Python's builtin `datetime.date` object, an `Undate` can be initialized by specifying numeric values for **year**, **month**, and **day**.

    We can display them in a standard format (default serialization is **ISO8601**, or YYYY-MM-DD), and we can compare them. An `Undate` object also has information about date precision and duration.

    _Unlike_ Python's `datetime.date`, an `Undate` can be initialized without providing all values for year, month, and day.

    This means we can create `Undate` instances for the month of November in 2000, for the year 2000, or for November 7th in some unknown year or the month of February in an unknown year.

    `Undate` also has an optional `label` field, since it's sometimes useful to attach a label to date.

    ### Partially unknown values

    We can also intialize an `Undate` object with string values, when a date is only partially known. We use the character **X** to indicate an unknown digit, following the notation used in the [Extended Date Time Format (EDTF)](https://www.loc.gov/standards/datetime/).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    import datetime

    from undate import Undate

    # initialization options
    option_values = [
        {"year": 2000, "month": 11, "day": 7},
        {"year": 2000, "month": 11, "label": "November 2000"},
        {"year": 2000, "label": "Y2K"},
        {"year": 2001},
        {"month": 11, "day": 7, "label": "Some November 7"},
        {"month": 2, "label": "Some February"},
        {"year": 1916, "month": 4, "day": 23, "label": "Easter 1916"},
        {"year": "19XX", "label": "1900s"},
        {"year": 2022, "month": "1X", "label": "late 2022"},
    ]


    def display_opts(input_opts):
        # format dictionary input options for display
        opts = []
        for key, val in input_opts.items():
            # wrap strings in quotes to differentiate from numbers
            if isinstance(val, str):
                val = f'"{val}"'
            opts.append(f"{key}={val}")
        return ", ".join(opts)


    # generate a radio button input to try out the different input options
    options = {display_opts(val): val for val in option_values}
    first_option = list(options.keys())[
        0
    ]  # pre-select first option so following functionality always has a value

    init_options = mo.ui.radio(
        options=options,
        label="Initialization options",
        value=first_option,
    )
    return Undate, datetime, display_opts, init_options, option_values


@app.cell(hide_code=True)
def _(Undate, datetime, display_opts, init_options, mo):
    display_init_opts = display_opts(init_options.value)

    undate_obj = Undate(**init_options.value)

    dt_error_msg = ""
    try:
        dt_obj = datetime.date(**init_options.value)
    except TypeError as dt_err:
        dt_obj = None
        dt_error_msg = f"**{dt_err.__class__.__name__}**: {dt_err}"

    undate_output = mo.md(f"""
        {undate_obj}

        `{repr(undate_obj)}`
    """).callout("success")

    init_successful_callout = mo.callout(
        "Initalization succeeded.", kind="success"
    )
    dt_err_callout = mo.callout(mo.md(dt_error_msg), kind="warn")

    undate_display = mo.vstack(
        [
            mo.md("## `undate.Undate`"),
            mo.md(f"`undate.Undate({display_init_opts})`"),
            mo.md(str(undate_obj)),
            mo.md(f"`{repr(undate_obj)}`"),
            mo.md(f"Date precision: {undate_obj.precision}"),
            mo.md(f"Duration in days: `{undate_obj.duration().days}`"),
            init_successful_callout,
        ],
        align="center",
    )
    dt_display = mo.vstack(
        [
            mo.md("## `datetime.date`"),
            mo.md(f"`datetime.date({display_init_opts})`"),
            mo.md(str(dt_obj)),
            mo.md(f"`{repr(dt_obj)}`" if dt_obj else "-"),
            mo.md("Date precision: day" if dt_obj else "-"),
            mo.md("Duration in days: 1" if dt_obj else "-"),
            dt_err_callout if dt_error_msg else init_successful_callout,
        ],
        align="center",
    )


    mo.vstack(
        [
            mo.hstack([init_options], justify="center"),
            mo.md("-----------------------------"),
            mo.hstack(
                [undate_display, dt_display],
                justify="space-between",
                widths="equal",
            ),
        ],
        align="stretch",
    )
    return


@app.cell(hide_code=True)
def _(Undate, option_values, pl):
    # initialize data with some sample dates; display on next slide with text
    sample_dates = [Undate(**opts) for opts in option_values]
    # sample_dates.append(datetime.date(**option_values[0]))
    sample_date_df = pl.DataFrame(
        data={
            "undate": sample_dates,
            "year": [d.year for d in sample_dates],
            "month": [d.month for d in sample_dates],
            "day": [d.day for d in sample_dates],
        }
    )
    return sample_date_df, sample_dates


@app.cell(hide_code=True)
def _(mo, sample_date_df):
    mo.vstack(
        [
            mo.md("""### Date Comparisons


    We can also do some simple calculations, like checking whether one date falls within another date.

    When an `Undate` instance is initialized, internally the class calculates earliest and latest possible values for that date in the Gregorian calendar.

    This means that some comparisons are possible even without precise information.

    For instance, is a year sometime during the 1900s before a month in late 2022?

    Uncertain dates with the same initial values aren't equal, since they are uncertain.

    The `Undate` class has properties to return `year`, `month`, and `day` if they are known. They are returned as strings to allow for partially unknown dates, and return `None` when a value is unknown."""),
            sample_date_df,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    comparison_opts = {
        "equals : ==": "eq",
        "in": "in",
        "greater than : >": "gt",
        "less than : <": "lt",
    }

    cmp_opt = mo.ui.radio(
        options=comparison_opts,
        label="Comparison operator",
        value="equals : ==",
    )
    return (cmp_opt,)


@app.cell(hide_code=True)
def _(alt, cmp_opt, mo, pd, sample_dates):
    from itertools import combinations


    def compare(d1, d2):
        result = None
        result_text = None  # display version of result
        op_str = ""  # display version of comparison operator
        try:
            if cmp_opt.value == "eq":
                op_str = "=="
                result = d1 == d2
            elif cmp_opt.value == "in":
                op_str = "in"
                result = d1 in d2
            elif cmp_opt.value == "gt":
                op_str = ">"
                result = d1 > d2
            elif cmp_opt.value == "lt":
                op_str = "<"
                result = d1 < d2

        except (TypeError, NotImplementedError):
            result = None
            result_text = "error"

        if result_text is None:
            if result == True:
                result_text = "true"
            elif result == False:
                result_text = "false"
            elif result is None:
                result_text = "unknown"

        return {
            "date1": str(d1),
            "date2": str(d2),
            "result": result,
            "result_str": result_text,
            # construct a text version of the comparison so direction is clear,
            # for comparisons where it matters
            "text": f"{d1} {op_str} {d2} ? {result_text}",
        }


    results = []
    # compare each pair of dates
    for d1, d2 in combinations(sample_dates, 2):
        # compare both directions
        results.append(compare(d1, d2))
        results.append(compare(d2, d1))

    # also do self comparison
    for d1 in sample_dates:
        results.append(compare(d1, d1))

    date_comparison_df = pd.DataFrame(data=results)

    mo.vstack(
        [
            mo.md(
                "This chart shows the results for comparisons across a set of `Undate` objects with varying precision and known information."
            ),
            cmp_opt,
            mo.ui.altair_chart(
                alt.Chart(date_comparison_df)
                .mark_rect()
                .encode(
                    y=alt.Y("date1", title=""),
                    x=alt.X("date2", title=""),
                    color=alt.Color("result_str", title="Result").scale(
                        domain=["true", "false", "error", "unknown"],
                        # range=["#4c78a8", "#e45756", "#f58518", "#bab0ac"],
                    ),
                    tooltip="text",
                )
                .properties(
                    title=f"Date comparisions for: {cmp_opt.value}", width=900
                )
            ),
        ],
        align="center",
    )
    # NOTE: may need to adjust dates included to avoid undate bugs with unknown years
    return


@app.cell(hide_code=True)
def _(Undate, mo, pl):
    from undate import UndateInterval

    nineteenth_c = UndateInterval(Undate(1801), Undate(1900), label="19th century")
    before_2000 = UndateInterval(latest=Undate(2000), label="Before 2000")
    after_1900 = UndateInterval(Undate(1900), label="After 1900")

    # initialize data with some sample dates; display on next slide with text
    sample_intervals = [nineteenth_c, before_2000, after_1900]
    # sample_dates.append(datetime.date(**option_values[0]))
    sample_intervals_df = pl.DataFrame(
        data={
            "label": [i.label for i in sample_intervals],
            "interval": sample_intervals,
            "earliest": [i.earliest for i in sample_intervals],
            "latest": [i.latest for i in sample_intervals],
            "duration": [
                repr(i.duration()) if i.earliest and i.latest else None
                for i in sample_intervals
            ],
            "duration_days": [
                i.duration().days if i.earliest and i.latest else None
                for i in sample_intervals
            ],
        }
    )

    mo.vstack(
        [
            mo.md(
                r"""
    ## Date Intervals

    Like many other date libraries, `undate` includes support for intervals.  An `UndateInterval` is a date range between two `Undate` objects. Intervals can be open-ended, allow for optional labels, and can calculate duration if enough information is known.

    ```python
    from undate import UndateInterval

    nineteenth_c = UndateInterval(Undate(1801), Undate(1900), label="19th century")
    before_2000 = UndateInterval(latest=Undate(2000), label="Before 2000")
    after_1900 = UndateInterval(Undate(1900), label="After 1900")
    ```

    An `UndateInterval` has an earliest and a latest value for the start and end of the date range. Since those are `Undate` instances, they also have earliest and latest values. The duration of an interval is calculated based on the difference between the last day and first day in range.
    ```
    """
            ),
            sample_intervals_df,
        ]
    )
    return (UndateInterval,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Parsing dates in supported formats

    Initializing an `Undate` directly with year, month, day values is useful, but often we want to parse text dates in known formats directly and work with them as data.

    The `undate` library has an extensive converter class ([`BaseDateConverter`](https://undate-python.readthedocs.io/en/latest/undate/converters.html)), which can be extended for parsing dates in specific formats and also for parsing and converting dates from other calendars.  Parsing is implemented with the Python library [Lark](https://lark-parser.readthedocs.io/en/stable/).

    Currently, `undate` supports **ISO8601** and some portions of the **Extended Date Time Format (EDTF)**.
    """
    )
    return


@app.cell(hide_code=True)
def _(Undate, pl):
    from undate.date import DatePrecision
    from undate.converters.iso8601 import ISO8601DateFormat

    Undate.DEFAULT_CONVERTER = "ISO8601"

    parse_dates_txt = ["1985-04-12", "1985-04", "1985", "--04-12"]
    parse_dates = [Undate.parse(d, "ISO8601") for d in parse_dates_txt]

    # sample_dates.append(datetime.date(**option_values[0]))
    parse_examples_df = pl.DataFrame(
        data={
            "input": parse_dates_txt,
            "repr": [repr(d) for d in parse_dates],
            "str": [str(d) for d in parse_dates],
            "precision": [str(d.precision) for d in parse_dates],
        }
    )
    return ISO8601DateFormat, parse_examples_df


@app.cell(hide_code=True)
def _(mo, parse_examples_df):
    mo.vstack(
        [
            mo.md(
                r"""
    ### ISO8601

    **ISO 8601** is an international standard for dates (see [Wikipedia ISO 8601 entry](https://en.wikipedia.org/wiki/ISO_8601) for more details). For Calendar dates, this format uses the familiar **YYYY-MM-DD** notation for full dates, **YYYY-MM** for year and month. Some earlier versions of the specification allowed formats like **--MM-DD** for dates when month and day are known but the year is not. A converter can be used directly by the class, or can be parsed by the name of the converter.

    In these examples, we set the default converter to ISO8601 so that the string format will serialize the date back out to the original format. It is also possible to output in a different format.

    ```python
    from undate.date import DatePrecision
    from undate.converters.iso8601 import ISO8601DateFormat

    Undate.DEFAULT_CONVERTER = "ISO8601"
    parse_dates_txt = ["1985-04-12", "1985-04", "1985", "--04-12", "1984/1986"]
    parse_dates = [Undate.parse(d, "ISO8601") for d in parse_dates_txt]
    ```
    """
            ),
            parse_examples_df,
            mo.hstack(
                [
                    mo.md(r"""
    If you try to parse something that isn't supported by the format or the parser, the method raises a `ValueError` exception with the error message from the parser."""),
                    mo.md("""
    ```python
    try:
        Undate.parse("????-04-12", "ISO8601")
    except ValueError as err:
        print(err)
    ```
    `invalid literal for int() with base 10: '????'`
    """),
                ]
            ),
        ]
    )
    return


@app.cell
def _(Undate, UndateInterval, pl):
    Undate.DEFAULT_CONVERTER = "EDTF"

    parse_edtf_dates = [
        "1985-04-12",
        "1985-04",
        "1985",
        "XXXX-04-12",
        "1964/2008",
        "2004-02-01/2005-02",
        "2005/2006-02",
        "1985-04-12/..",
        "-1985",
        "Y170000002",
    ]
    parsed_edtf_dates = [Undate.parse(d, "EDTF") for d in parse_edtf_dates]


    def precision(date):
        # display date precision for undate or start/end of undate interval
        if isinstance(date, Undate):
            return str(date.precision)
        elif isinstance(date, UndateInterval):
            parts = []
            if date.earliest is not None:
                parts.append(str(date.earliest.precision))
            if date.latest is not None:
                parts.append(str(date.latest.precision))
            return " / ".join(parts)


    # sample_dates.append(datetime.date(**option_values[0]))
    parse_edtf_examples_df = pl.DataFrame(
        data={
            "input": parse_edtf_dates,
            "repr": [repr(d) for d in parsed_edtf_dates],
            "str": [str(d) for d in parsed_edtf_dates],
            "precision": [precision(d) for d in parsed_edtf_dates],
        }
    )
    return (parse_edtf_examples_df,)


@app.cell(hide_code=True)
def _(mo, parse_edtf_examples_df):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Extendend Date Time Format

    Since the EDTF format includes both dates and intervals, parsing an EDTF can return either an `Undate` or an `UndateInterval`.  

    EDTF and ISO8601 use the same format for full precision day, year-month, and year dates.

    EDTF uses **X** to indicate unspecified digits.  EDTF also supports negative years and years that are more than four digits; the **Y** prefix is used to indicate the number is a year.

    The EDTF format includes notation for intervals, including open intervals; parsing an EDTF interval returns an `UndateInterval`. Here are some examples from the Library of Congress documentation on EDTF. Note that the start and end date of the interval don't have to use the same date precision.
    ```python

    parse_edtf_dates = ["1985-04-12","1985-04","1985", "XXXX-04-12", "1964/2008",
        "2004-02-01/2005-02", "2005/2006-02", "1985-04-12/..", "-1985", "Y170000002"]
    parsed_edtf_dates = [Undate.parse(d, "EDTF") for d in parse_edtf_dates]
    ```


    """
            ),
            parse_edtf_examples_df,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Calendars

    `undate` includes a [BaseCalendarConverter](https://undate-python.readthedocs.io/en/latest/undate/converters.html#undate.converters.base.BaseCalendarConverter), as a special case of the `BaseDateConverter` for format parsing and conversion like ISO8601 and EDTF. In addition the `parse()` method that all converters must implement, calendar converters have logic for returning minimum and maximum month and day, first and last month as integers (since some calendars don't start the year on month 1), and a `to_gregorian()` method to convert into a standard Gregorian date. `undate` usees the [convertdate](https://github.com/fitnr/convertdate) Python library for the actual numeric conversion.

    Supported calendars:

    - Gregorian
    - Islamic Hijri
    - Hebrew Anno Mundi
    - Seleucid Hebrew calendar


    An `Undate` instance always has a calendar defined; it uses the Gregorian calendar if a calendar is not specified.  You may have noticed this in the output from `repr()` in the earlier examples.

    `undate` preserves the numeric values of the date in the original calendar, but internally converts to Gregorian calendar for comparison with other dates. `Undate` instances with different calendars can be used together.

    This means that two `Undate` objects with the same numeric day, month, and year values represent different dates if they use different calendars.  This also means that we can preserve the precision of the date in the original calendar (such as a month or a year), even when that doesn't neatly map to a month or year in the Gregorian calendar and even if a month or year has a different number of days than we're used to.
    """
    )
    return


@app.cell(hide_code=True)
def _(Undate, mo, pl):
    calendars = ["Gregorian", "Hebrew", "Islamic"]

    calendar_dates = {
        "label": [
            "21 Rajab 1023",
            "Rajab 1023",
            "1023",
            "3 Tishrei 5370",
            "Tishrei 5370",
            "5370",
            "2 June 1663",
            "June 1663",
            "1663",
        ],
        "calendar": [
            "Islamic",
            "Islamic",
            "Islamic",
            "Hebrew",
            "Hebrew",
            "Hebrew",
            "Gregorian",
            "Gregorian",
            "Gregorian",
        ],
        # we pre-supply the numeric values in this case, since we don't yet have a text parser for Gregorian dates
        "numeric": [
            (1023, 7, 21),
            (1023, 7),
            (1023,),
            (5370, 7, 3),
            (5370, 7),
            (5370,),
            (1663, 6, 2),
            (1663, 6),
            (1663,),
        ],
    }

    cal_dates_df = (
        pl.from_dict(calendar_dates)
        .with_columns(
            # initialize an undate by parsing text values with specified calendar
            undate=pl.struct("numeric", "calendar").map_elements(
                lambda row: Undate(*row["numeric"], calendar=row["calendar"]),
                return_dtype=pl.datatypes.Object,
            ),
            # string representation of how you would initialize an undate object with numbers and calendar
            undate_str=pl.struct("numeric", "calendar").map_elements(
                lambda row: f'Undate({", ".join([str(n) for n in row["numeric"]])}, calendar="{row["calendar"]}")',
                return_dtype=pl.datatypes.String,
            ),
        )
        .with_columns(
            # additional columns based on undate object
            precision=pl.col("undate").map_elements(
                lambda x: str(x.precision).lower(),
                return_dtype=pl.datatypes.String,
            ),
            earliest_gregorian=pl.col("undate").map_elements(
                lambda x: x.earliest, return_dtype=pl.datatypes.Object
            ),
            latest_gregorian=pl.col("undate").map_elements(
                lambda x: x.latest, return_dtype=pl.datatypes.Object
            ),
            duration=pl.col("undate").map_elements(
                lambda x: x.duration().days
                if isinstance(x.duration().days, int)
                # handle uninteger; choose minimal value for now
                else min(x.duration().days),
                return_dtype=pl.datatypes.Int32,
            ),
        )
    ).drop("numeric")

    mo.vstack(
        [
            mo.md(
                "This table shows dates with varying precision from three different calendars, with their numeric values in the original calendar and earliest and latest Gregorian dates."
            ),
            cal_dates_df,
        ]
    )
    return


@app.cell(hide_code=True)
def _(datetime, mo, pd):
    mo.md(
        f"""
    ## Implementation details 

    Internally, we use `numpy.datetime64` and `numpy.timedelta64` to store converted dates; we implemented shims to make these objects look a bit more like the builtin python `datetime.date` and `datetime.timedelta` objects, since they are easier to work with and the first version of `undate` used them.

    We switched to `numpy` for dates so that we could support a wider range of years.  

    Python `datetime.date` only supports four-digit positive years (1-9999).

    The popular data analysis library **Pandas** is much more limited - in spite of using `numpy.datetime64` internally, Pandas methods for parsing dates and converting to Timestamp objects don’t support dates before 1677AD.

    In contrast, `numpy.datetime64` supports a range of 2.5e16 BC, 2.5e16 AD (see [NumPy Datetime units documentation](https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units)).


    | Implementation | Minimum year (code) |  Maximum year (code) | Minimum year |  Maximum year |
    | -------------: | :----------: | :-----------: | :----------: | :-----------: |
    | `datetime.date` | `datetime.MINYEAR` | `datetime.MAXYEAR` | {datetime.MINYEAR} | {datetime.MAXYEAR} |
    | `pandas.Timestamp` | `pd.Timestamp.min.year` | `pd.Timestamp.max.year` | {pd.Timestamp.min.year} | {pd.Timestamp.max.year} |
    | `numpy.datetime64[D]` | - | - | 2.5e16 BC | 2.5e16 AD |
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Example use cases

    ### Shakespeare and Company Project 

    The [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/) is a research project based on records from Sylvia Beach’s famous 1920s and 1930s bookshop and lending library in Paris to reveal the reading practices of the influential writers, artists, intellectuals, and students who lived in Paris between the two world wars. Shakespeare and Company was an English-language lending library and bookshop, and Beach's papers include an incomplete set of lending library cards documenting what books members borrowed and when.

    This project is based on relatively recent materials, but in spite of that fact much of the infomration is imprecise and imperfect, as they were written by Beach and her assistants to run a business — they didn't always write full titles down because they knew what books they had available. And in some cases, they also didn't record the year for the borrowing records; for example, this portion of Gertrude Stein's borrowing history, which includes months and days but no years:"""
            ),
            # Render an local image
            mo.image(
                src="public/stein_lendingcard_unknownyear.jpg",
                alt="Detail from one of Gertrude Stein's lending library cards",
                width="70%",
                caption="Gertrude Stein borrowing activity, unknown year",
            ),
            mo.md(r"""This project provides an example of how partially unknown dates can still be computationally useful. If we make the reasonable assumption that for borrowing activity like this, with an unknown year, books were returned in the same or following year, then we can calculate how long the books were borrowed and include them in analysis of library member activities.

    Here I demonstrate this using borrowing events from the Shakespeare and Company Project 2.0 dataset.
    """),
        ],
        align="center",
    )
    return


@app.cell(hide_code=True)
def _(ISO8601DateFormat, NOTEBOOK_PUBLIC_DIR, Undate, UndateInterval, mo, pl):
    from undate.date import ONE_DAY

    # load a filtered set of data from 2.0 version of S&co events data from the public folder
    # NOTE: data has been prefiltered for efficiency; borrow events only, with start and end dates,
    # and a subset of relevant fields. See filter_data script for specifics.
    borrow_events = (
        pl.read_csv(str(NOTEBOOK_PUBLIC_DIR / "SCoData_borrows_events.csv"))
        .with_columns(
            start_undate=pl.col("start_date").map_elements(
                lambda x: Undate.parse(x, "ISO8601"),
                return_dtype=pl.datatypes.Object,
            ),
            end_undate=pl.col("end_date").map_elements(
                lambda x: Undate.parse(x, "ISO8601"),
                return_dtype=pl.datatypes.Object,
            ),
        )
        .with_columns(
            start_date_precision=pl.col("start_undate").map_elements(
                lambda x: str(x.precision), return_dtype=pl.datatypes.String
            ),
            end_date_precision=pl.col("end_undate").map_elements(
                lambda x: str(x.precision), return_dtype=pl.datatypes.String
            ),
        )
        .filter(
            # filter to day-level precision since that's currently needed to calculate duration
            pl.col("start_date_precision").eq("DAY"),
            pl.col("end_date_precision").eq("DAY"),
        )
    )


    def undate_duration(start_date, end_date):
        # treat a same-day return as a one day borrow
        if start_date == end_date:
            return ONE_DAY
        isoformat = ISO8601DateFormat()

        unstart = isoformat.parse(start_date)
        unend = isoformat.parse(end_date)
        # if start year is known but end is not, make them both unknown
        # (assume same/subsequent year)
        if unstart.known_year and (not unend.known_year):
            unstart = Undate(month=unstart.month, day=unstart.day)
        interval = UndateInterval(earliest=unstart, latest=unend)

        # borrow durations in Shakespeare and Company Project were defined as not including both ends (or half both ends)
        # to reconcile differences between duration logic with undate, which includes both endpoints, we subtract one day
        return (interval.duration() - ONE_DAY).days


    # calculate durations; returns a dataframe with one column
    duration_df = borrow_events.select("start_date", "end_date").map_rows(
        lambda x: undate_duration(x[0], x[1]), return_dtype=pl.datatypes.Int32
    )

    # add fields to the main dataframe for duration and whether year is known
    borrow_events = borrow_events.with_columns(
        undate_duration=duration_df["map"],
        known_year=borrow_events["start_undate"].map_elements(
            lambda x: "known" if x.known_year else "unknown",
            return_dtype=pl.datatypes.String,
        ),
    )

    mo.vstack(
        [
            mo.md(
                "This subset of the borrowing data shows events with dates but no known year."
            ),
            borrow_events.head(10),
        ]
    )
    return (borrow_events,)


@app.cell(hide_code=True)
def _(alt):
    def raincloud_plot(dataset, fieldname, field_label, color_opts=None):
        """Create a raincloud plot for the density of the specified field
        in the given dataset. Takes an optional tooltip for the strip plot.
        Returns an altair chart."""

        # create a density area plot of specified fieldname

        duration_density = (
            alt.Chart(dataset)
            .transform_density(
                fieldname,
                as_=[fieldname, "density"],
            )
            .mark_area(orient="vertical")
            .encode(
                x=alt.X(
                    fieldname, title=None, axis=alt.X(labels=False, ticks=False)
                ),
                y=alt.Y(
                    "density:Q",
                    # suppress labels and ticks because we're going to combine this
                    title=None,
                    axis=alt.Axis(
                        labels=False, values=[0], grid=False, ticks=False
                    ),
                ),
            )
            .properties(height=100, width=800)
        )

        # Now create jitter plot of the same field
        # jittering / stripplot adapted from https://stackoverflow.com/a/71902446/9706217

        chart_color_opts = {}
        if color_opts is not None:
            chart_color_opts = {"color": color_opts}

        stripplot = (
            alt.Chart(dataset)
            .mark_circle(size=50)
            .encode(
                x=alt.X(
                    fieldname,
                    title=field_label,
                    axis=alt.Axis(labels=True),
                ),
                y=alt.Y("jitter:Q", title=None, axis=None),
                **chart_color_opts,
                # color=alt.Color(color_by),  # .scale(**color_scale),
            )
            .transform_calculate(jitter="(random() / 200) - 0.0052")
            .properties(
                height=120,
                width=800,
            )
        )

        # use vertical concat to combine the two plots together
        raincloud_plot = alt.vconcat(duration_density, stripplot).configure_concat(
            spacing=0
        )
        return raincloud_plot
    return (raincloud_plot,)


@app.cell(hide_code=True)
def _(borrow_events, mo, pl):
    members_with_unknownyears = (
        borrow_events.filter(pl.col("known_year").eq("unknown"))
        .select("member_names")
        .unique()
    )
    # get counts and filter to members with at laest two borrows
    borrow_counts = borrow_events.group_by("member_names").len()
    members_with_unknownyears = members_with_unknownyears.join(
        borrow_counts, on="member_names"
    ).filter(pl.col("len").gt(2))

    members_with_unknowns = members_with_unknownyears["member_names"].to_list()


    member_opt = mo.ui.radio(
        options=members_with_unknowns,
        label="Library Member",
        value="Gertrude Stein",
    )
    return (member_opt,)


@app.cell(hide_code=True)
def _(alt, borrow_events, member_opt, mo, pl, raincloud_plot):
    mo.vstack(
        [
            mo.md("""### Library Member borrowing duration

            This raincloud plot showing the distribution of borrowing duration for members with borrow events without known years.  That is, how long did they typically keep the books that they borrowed?
            """),
            member_opt,
            mo.ui.altair_chart(
                raincloud_plot(
                    # filter to selected member
                    borrow_events.filter(
                        pl.col("member_names").eq(member_opt.value)
                    ).select("undate_duration", "known_year"),
                    "undate_duration",
                    "Borrow duration in days",
                    alt.Color("known_year", title="Year"),
                ).properties(title=f"Borrows for {member_opt.value}")
            ),
            mo.md(
                "The capability to calculate durations for partially known dates means this information can be included in analysis and interpretation of member borrowing activity, such as books that were borrowed and returned quickly or checked out for longer times, and included in broader analysis of borrowing behavior across all library members or specific individuals."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(NOTEBOOK_PUBLIC_DIR, pl):
    # load a copy of PGP document data from the assets folder
    # pre-filtered to documents with standardized format, supported calendars, and subset of fields
    # see filter script for specifics
    docs_with_docdate = pl.read_csv(
        str(NOTEBOOK_PUBLIC_DIR / "pgp_dated_documents.csv")
    )
    return (docs_with_docdate,)


@app.cell(hide_code=True)
def _(docs_with_docdate, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Princeton Geniza Project

    The [Princeton Geniza Project](https://geniza.princeton.edu/) is a database of texts that were preserved in a medieval synagogue in Cairo, Egypt.

    The texts are predominantly written in Hebrew script, are often fragmentary, and in many cases they are difficult to place in time. Because of the context of these materials, they use a mix of calendars.

    This part of the notebook demonstrate `undate` capabilities using the subset of documents with known dates.  The dataset fields include original date, calendar, and a standardized date (using Common Era dates; Julian calendar before 1583, Gregorian after).
    """
            ),
            docs_with_docdate.head(10),
            docs_with_docdate["doc_date_calendar"].value_counts(),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Undate, docs_with_docdate, pl):
    # Use undate to parse the original dates based on calendar

    from lark.exceptions import UnexpectedEOF, VisitError


    def parse_original_date(doc_date_calendar, doc_date_original):
        if doc_date_calendar == "Anno Mundi":
            undate_calendar = "Hebrew"
        elif doc_date_calendar == "Hijrī":
            undate_calendar = "Islamic"
        elif doc_date_calendar == "Seleucid":
            undate_calendar = "Seleucid"

        try:
            return Undate.parse(doc_date_original, undate_calendar)
        except (VisitError, ValueError, UnexpectedEOF):
            # we don't support parsing everything in this dataset, and some of them have errors
            # for demonstration purposes, ignore anything we can't parse
            pass


    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


    docs_with_undate = (
        docs_with_docdate.with_columns(
            undate_orig=pl.struct(
                "doc_date_calendar", "doc_date_original"
            ).map_elements(
                lambda x: parse_original_date(
                    x["doc_date_calendar"], x["doc_date_original"]
                ),
                return_dtype=pl.Object,
            )
        )
        .filter(
            # limit to the records that were successfully parsed
            pl.col("undate_orig").is_not_null()
        )
        .with_columns(
            # compare undate standardized earliest/latest values with the standardized dates in the dataset
            undate_earliest=pl.col("undate_orig").map_elements(
                lambda x: x.earliest, return_dtype=pl.datatypes.Object
            ),
            undate_latest=pl.col("undate_orig").map_elements(
                lambda x: x.latest, return_dtype=pl.datatypes.Object
            ),
            orig_date_precision=pl.col("undate_orig").map_elements(
                lambda x: str(x.precision).lower(),
                return_dtype=pl.datatypes.String,
            ),
            # determine weekday when possible
            undate_weekday=pl.col("undate_orig").map_elements(
                lambda x: days[x.earliest.weekday]
                if x.earliest == x.latest
                else None,
                return_dtype=pl.datatypes.String,
            ),
            # get numeric month in original calendar, when known
            undate_month=pl.col("undate_orig").map_elements(
                lambda x: int(x.month) if x.month else None,
                return_dtype=pl.datatypes.Int8,
            ),
        )
    )

    docs_with_undate
    return days, docs_with_undate


@app.cell(hide_code=True)
def _(docs_with_undate, mo):
    mo.vstack(
        [
            mo.md(
                r"""
    We can compare `undate` standardized earliest/latest values with the standardized dates provided in the dataset.

    For the dates before 1583 we expect to se a few days difference, due to the use of Julian calendar.
    """
            ),
            # limit and order fields to help make the comparison
            docs_with_undate[
                [
                    "doc_date_original",
                    "doc_date_calendar",
                    "undate_orig",
                    "doc_date_standard",
                    "undate_earliest",
                    "undate_latest",
                    "orig_date_precision",
                    "undate_weekday",
                ]
            ].head(10),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, docs_with_undate, pl):
    docs_with_month = docs_with_undate.filter(pl.col("undate_month").is_not_null())


    pgp_month_calendar_chart = (
        alt.Chart(
            docs_with_month.select("undate_month", "pgpid", "doc_date_calendar")
        )
        .mark_rect()
        .encode(
            alt.X("undate_month", title="month"),
            alt.Color("count(pgpid)", title="# of documents"),
        )
        .facet(row=alt.Facet("doc_date_calendar", title="Original Calendar"))
        .properties(title="Document frequency by month and calendar")
    )
    return (pgp_month_calendar_chart,)


@app.cell(hide_code=True)
def _(mo, pgp_month_calendar_chart, pgp_weekday_chart):
    mo.vstack(
        [
            mo.md(
                r"""
    Preserving calendar and date information, we can now do some analysis based on different aspects of these dates. 
    """
            ),
            mo.hstack(
                [
                    mo.md(
                        r""""For instance, how are the documents distributed over the different months?"

                There's a month 13 that doesn't exist in the Islamic calendar, shows up on the Hebrew calendar with much fewer documents — that's because the Hebrew calendar includes a leap _month_. Because that month doesn't happen every year, we would expect to see far fewer documents - as evidenced in the heatmap."""
                    ),
                    pgp_month_calendar_chart,
                ]
            ),
            mo.hstack(
                [
                    pgp_weekday_chart,
                    mo.md(
                        """We can also plot frequency by weekday, for documents with day-level precision.

    The results show that **Legal documents** are the most likely to be precisely dated. 

    Monday and Thursday are the other convening days for court sessions, which have noticeably more documents. Saturday is the Hebrew Shabbat, and as we would expect there are fewer documents.

                        """
                    ),
                ]
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(alt, days, docs_with_undate, pl):
    # filter to parsed dates with day-level precision
    # limit by document type for types with enough day-precision events to chart
    pgp_weekday_docs = docs_with_undate.filter(
        pl.col("orig_date_precision").eq("day")
    ).filter(
        pl.col("type").is_in(
            ["Letter", "Legal document", "State document", "List or table"]
        )
    )

    pgp_weekday_chart = (
        alt.Chart(pgp_weekday_docs.select("type", "undate_weekday", "pgpid"))
        .mark_rect()
        .encode(
            alt.X("undate_weekday", sort=days, title="weekday"),
            alt.Color("count(pgpid)", title="# of documents"),
        )
        .facet(
            row=alt.Facet(
                "type",
                title="",
                header=alt.Header(
                    labelAngle=0, labelAnchor="start", labelBaseline="bottom"
                ),
            )
        )
        .resolve_scale(color="independent")
        .properties(title="Document frequency by weekday")
    )
    return (pgp_weekday_chart,)


@app.cell
def _(NOTEBOOK_PUBLIC_DIR, pl):
    sf_time = pl.read_csv(str(NOTEBOOK_PUBLIC_DIR / "futuristic_fiction.csv"))
    sf_time_multiyear = sf_time.filter(pl.col("multiyears").is_not_null())
    return sf_time, sf_time_multiyear


@app.cell(hide_code=True)
def _(mo, sf_time, sf_time_multiyear):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Time Horizons of Futuristic Fiction.

    Humanities data exceeds the bounds of standard tooling in both directions (past and future). This dataset provides us a fun example to experiment with.  The authors use metadata on English language speculative fiction to look at the distance in time between a work was released and when it is set; that is, how far in the future are authors speculating.
    """
            ),
            mo.md(
                f"The data includes {sf_time.height:,} records; {sf_time_multiyear.height:,} of those ({(sf_time_multiyear.height / sf_time.height) * 100:.1f}%) have multiple years."
            ),
            sf_time,
            mo.md("""

    The essay published with this data explains how they handled multi-year works:        

    > If the work takes place over a wide range of years (e.g. time travel or multi-generational narratives), we generally entered the **median of the years** depicted in the work. ... Formatted as an integer rather than a date because the **Python datetime module doesn’t support years beyond 9999**. (A note to the AIs maintaining the world’s code in the distant future: beware the Y10K bug!)
    """),
        ]
    )
    return


@app.cell(hide_code=True)
def _(Undate, UndateInterval, mo, pl, sf_time_multiyear):
    # next... start parsing. interval? set of years? maybe start with min/max interval as a first pass


    def parse_multiyear(value):
        # print(value)
        if value == "20th century":
            value = "1901/2000"

        # TODO: range and comma: 1982/1983, 1988

        elif "-" in value:
            value = value.replace("-", "/")
        elif "," in value:
            try:
                # strip out non-numerics?
                years = [int(v.strip()) for v in value.split(",")]
                value = f"{min(years)}/{max(years)}"
            except ValueError as err:
                # print(err)
                return
        try:
            interval = Undate.parse(value, "EDTF")
            # it's possible that this returns an undate or an undate interval
            # convert to an interval so the structure is the same
            if isinstance(interval, Undate):
                interval = UndateInterval(interval.earliest, interval.latest)

            earliest = interval.earliest
            latest = interval.latest

            # debugging
            # print(
            #     f"{interval} {interval.__class__} earliest {interval.earliest} ({interval.earliest.__class__}) latest {interval.latest} ({interval.latest.__class__})"
            # )
            dictreturn = {
                # nested objects not allowed
                "undate_interval": str(interval),
                "interval_earliest": int(earliest.year),
                "interval_latest": int(latest.year),
            }
            # print(dictreturn)
            return dictreturn
        except ValueError as err:
            # print(err)
            return {
                "undate_interval": None,
                "interval_earliest": None,
                "interval_latest": None,
            }


    sf_time_multiyear_undate = (
        sf_time_multiyear.with_columns(
            undate_parsing=pl.col("multiyears").map_elements(
                parse_multiyear,  # return_dtype=pl.Struct #return_dtype=pl.datatypes.Object
                return_dtype=pl.Struct(
                    [
                        pl.Field(
                            "undate_interval", pl.datatypes.String
                        ),  # pl.datatypes.Object),
                        pl.Field("interval_earliest", pl.datatypes.Int64),
                        pl.Field("interval_latest", pl.datatypes.Int64),
                    ]
                ),
            )
        )
        .unnest("undate_parsing")
        .with_columns(
            years_distant_min=pl.col("interval_earliest").sub(pl.col("released")),
            years_distant_max=pl.col("interval_latest").sub(pl.col("released")),
            duration=pl.col("interval_latest").sub(pl.col("interval_earliest")),
        )
        .with_columns(
            # combined years distant for chart label
            pl.format(
                "{} ({}—{})",
                pl.col("years_distant").cast(pl.Int64),
                "years_distant_min",
                "years_distant_max",
            ).alias("years distant")
        )
    )

    mo.vstack(
        [
            mo.md(
                """In this filtered version of the data, we've used `undate` to parse the **multiyears** field in the data into intervals, and calculated min and max values for the **years_distant** betwen year of release and year the work is set.

                The data does include some non-sequential spans, but for simplicity in this case we treat it as the range covering of the earliest and latest dates.
                """
            ),
            sf_time_multiyear_undate.select(
                "title",
                "creator",
                "released",
                "year_set",
                "years_distant",
                "multiyears",
                "undate_interval",
                "interval_earliest",
                "interval_latest",
                "years_distant_min",
                "years_distant_max",
                "duration",
                "years distant",
            ),
        ]
    )
    return (sf_time_multiyear_undate,)


@app.cell
def _(alt, sf_time_multiyear_undate):
    base_chart = alt.Chart(sf_time_multiyear_undate)

    year_range_chart = base_chart.mark_bar(opacity=0.8, color="#7570b3").encode(
        x=alt.X(
            "interval_earliest", title="Years work set (multiyear works)"
        ).scale(type="log"),
        x2="interval_latest",
        y=alt.Y("released", title="Year Released").axis(format="r"),
        tooltip=["title", "creator", "multiyears"],
    )
    year_midpoint_chart = base_chart.mark_point(
        color="#17becf", opacity=0.7
    ).encode(x=alt.X("year_set").scale(type="log"), y="released")

    # (year_range_chart + year_midpoint_chart).interactive()
    return year_midpoint_chart, year_range_chart


@app.cell
def _(
    alt,
    mo,
    pl,
    sf_time_multiyear_undate,
    year_midpoint_chart,
    year_range_chart,
):
    # now graph years distant
    base_distance_chart = alt.Chart(
        sf_time_multiyear_undate.filter(pl.col("undate_interval").is_not_null())
    )

    # common configuration for x-axis
    x_axis_released = (
        alt.X("released", title="Year Released").axis(format="r").scale(nice=False)
    )

    years_distant_range_chart = base_distance_chart.mark_bar(
        color="#7570b3"
    ).encode(
        y=alt.Y("years_distant_min", title="Years in the future"),
        y2="years_distant_max",
        x=x_axis_released,
        tooltip=["title", "creator"],
    )

    # tableau orange #f58518

    years_distant_midpoint_chart = base_distance_chart.mark_circle(
        color="#17becf", opacity=0.3
    ).encode(
        y=alt.Y("years_distant"),
        x=x_axis_released,
    )


    mo.vstack(
        [
            mo.md(
                """This chart shows the range of years that works are set, organized by year of release. Because some works are so far in the future, this requires a logarithmic scale. 
                """
            ),
            (year_range_chart + year_midpoint_chart).interactive(),
            mo.md(
                """We can try to chart the full-scale of the difference in year of release and year a work is set, but this chart is dominated by a few outliers with very long time scale.
                """
            ),
            (
                years_distant_range_chart + years_distant_midpoint_chart
            ).interactive(),
        ]
    )
    return base_distance_chart, x_axis_released


@app.cell
def _(alt, base_distance_chart, mo, x_axis_released):
    # customize opacity based on the duration
    # wider span == less opacity
    opacity_condition = {
        "condition": [
            {"test": "datum.duration <= 100", "value": 1.0},
            {"test": "datum.duration <= 500", "value": 0.9},
            {"test": "datum.duration <= 1000", "value": 0.7},
            {"test": "datum.duration <= 10000", "value": 0.5},
        ],
        "value": 0.4,
    }

    years_distant_1k_chart = base_distance_chart.mark_bar(
        clip=True, color="#7570b3"
    ).encode(
        y=alt.Y("years_distant_min", title="Years in the future").scale(
            domain=(-50, 1000)
        ),
        y2="years_distant_max",
        x=x_axis_released,
        tooltip=[
            "title",
            "creator",
            "multiyears",
            "years distant",
        ],
        opacity=opacity_condition,
    )

    years_distant_1k_midpoint_chart = base_distance_chart.mark_circle(
        color="#17becf", opacity=0.3, clip=True
    ).encode(
        y=alt.Y("years_distant"),
        x=x_axis_released,
    )

    # chart works by year released
    # tableau red #e45756
    works_by_year_released = (
        base_distance_chart.mark_line(interpolate="monotone", color="#d62728")
        .encode(
            y=alt.Y("count(title)", title="# Works"), x=x_axis_released.axis(None)
        )  # don't display x-axis, since will be combined
        .properties(height=100, width=1000)
    )


    mo.vstack(
        [
            mo.md(
                """This chart shows how many years in the future works are set, with a cap of 1000 years. 

            The time difference for multiyear intervals is shown in purple, with decreasing opacity as the duration of the time gets larger.  The midpoint years distance chosen by the dataset authors is graphed as a point along the bar for the time range.

                The  upper line chart shows the number of works per year in the dataset, for context.
                """
            ),
            (
                works_by_year_released
                & (
                    years_distant_1k_chart + years_distant_1k_midpoint_chart
                ).properties(width=1000)
            ).interactive(),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Conclusion

    `undate` is still in beta, building on work from [Shakespeare and Company Project](https://shakespeareandco.princeton.edu/), [Princeton Geniza Project](https://geniza.princeton.edu/), and [Islamic Scientific Manuscripts Initiative](https://ismi.mpiwg-berlin.mpg.de/).

    We're still actively developing the library and expanding and improving functionality as we work towards a 1.0 release, but as you can see from this demo, the library is already quite useful. We would love to have new contributors join the project and add new datasets, share use cases, and maybe even contribute to code, documentation, and examples.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    from collections import namedtuple

    # use icons to help visually distinguish types of resources
    Icons = namedtuple("Icons", ["article", "dataset", "website", "code"])
    my_icons = Icons(
        article=mo.icon("material-symbols:article-outline"),
        dataset=mo.icon("material-symbols:dataset-outline"),
        website=mo.icon("material-symbols:web"),
        code=mo.icon("material-symbols:code-blocks"),
    )

    mo.vstack(
        [
            mo.hstack(
                [
                    mo.md("## Resources"),
                    mo.hstack(
                        [
                            mo.md(f"{my_icons.article} article"),
                            mo.md(f"{my_icons.dataset} dataset"),
                            mo.md(f"{my_icons.code} software"),
                            mo.md(f"{my_icons.website} website"),
                        ],
                        gap=1,
                        justify="start",
                    ),
                ],
                justify="space-between",
                align="center",
                widths=[2, 1],
            ),
            mo.md(f"""
    - _Shakespeare and Company Project_. 2020. Publisher: Center for Digital Humanities, Princeton University. https://shakespeareandco.princeton.edu/. {my_icons.website}
    - _Princeton Geniza Project_. 2022. Publisher: Center for Digital Humanities, Princeton University. https://geniza.princeton.edu/. {my_icons.website}
    - Library of Congress. 2019. Extended Date Time Format (EDTF) Specification. Library of Congress, February. Accessed March 30, 2025. https://www.loc.gov/standards/datetime/. {my_icons.article}
    - Koeser, Rebecca Sutton, Julia Damerow, Robert Casties, and Cole Crawford. “Undate: Humanistic Dates for Computation.” _Computational Humanities Research_, 2025, 1–10. https://doi.org/10.1017/chr.2025.10006. {my_icons.article}
    - Koeser, Rebecca Sutton, Cole Crawford, Julia Damerow, Malte Vogl, and Robert Casties. “Undate Python Library”. Zenodo, July 22, 2025. https://doi.org/10.5281/zenodo.16328670. {my_icons.code}
    - Koeser, Rebecca Sutton, and Zoe LeBlanc. 2024. Missing Data, Speculative Reading. _Journal of Cultural Analytics_ 9, no. 2 (May). https://doi.org/10.22148/001c.116926 {my_icons.article}
    - Koeser, Rebecca Sutton & Kotin, Joshua. (2025). Shakespeare and Company Project Datasets [Data set]. Version 2. Princeton University. https://doi.org/10.34770/kf6c-b079 {my_icons.dataset}
    - Kotin, Joshua and Rebecca Sutton Koeser. 2022. Shakespeare and Company Project Data Sets. _Journal of Cultural Analytics_ 7, no. 1 (February). https://doi.org/10.22148/001c.32551 {my_icons.article}
    - Rustow, Marina, Rebecca Sutton Koeser, Rachel Richman, Ksenia Ryzhova, Amel Bensalim, and Abdellatif Mohamed. “Princeton Geniza Project dataset”. Zenodo, July 8, 2025. https://doi.org/10.5281/zenodo.15839056 {my_icons.dataset}
    - Wythoff, Grant, and Theodore Leane. 2025. “Time Horizons of Futuristic Fiction.” Edited by Alexander Manshel, J.D. Porter, and Melanie Walsh. Post45 Data Collective, June. https://doi.org/10.18737/CNJV1733p4520221212. {my_icons.dataset}"""),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
