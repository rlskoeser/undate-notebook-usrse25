import marimo

__generated_with = "0.15.0"
app = marimo.App(
    width="medium",
    app_title="Undate: computing with uncertain and partially-unknown dates",
    layout_file="layouts/undate-overview.slides.json",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    from undate import __version__ as undate_version
    return mo, undate_version


@app.cell(hide_code=True)
def _(mo, undate_version):
    mo.md(f"""# Undate: computing with uncertain and partially-unknown dates

    `Undate` is an ambitious, in-progress effort to develop a pragmatic Python library for computation and analysis of temporal information in humanistic and cultural data, with a particular emphasis on uncertain, incomplete, or imprecise dates and with support for multiple calendars.

    Researchers in the humanities often work with historical or cultural data, and knowing when particular materials were created or events happened is important for understanding the context, interpreting correctly, and determining relationships and sequencing. However, these kind of materials rarely have full precision dates with known year, month, and day. In some contexts, scholars may be happy if they can determine even just a century based on handwriting or mentions of historic coins.

    Humanistic and cultural data also often includes dates in different calendars, or even a mix of calendars within the same project or system. It's important to preserve the original date and calendar information, but it's also valuable to convert dates to a standard calendar so they can be compared and sorted together. `Undate` objects are calendar aware and calendar explicit, with a default of the Gregorian calendar. Currently, we support parsing and calendar conversion for dates in the Hebrew _Anno Mundi_ calendar and Islamic _Hijri_ calendar.

    This notebook demonstrates current use and functionality of the core `Undate` and `UndateInterval` objects, along with some examples and use-cases from specific projects.

    This notebook is written with `undate` version {undate_version}.
    """)
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
    return Undate, datetime, init_options


@app.cell(hide_code=True)
def _(Undate, datetime, init_options, mo):
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
def _(mo):
    mo.md(r"""We can also compare them. Is this the same date?""")
    return


@app.cell
def _(dt_november7, november7):
    bool(november7 == dt_november7)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""We can also do some simple calculations, like checking whether one date falls within another date."""
    )
    return


@app.cell
def _(november, year2k):
    november in year2k
    return


@app.cell
def _(november7_1, year2k):
    november7_1 in year2k
    return


@app.cell
def _(november, november7_1):
    november7_1 in november
    return


@app.cell
def _(easter1916, year2k):
    easter1916 in year2k
    return


@app.cell
def _(november7_some_year, year2k):
    november7_some_year in year2k
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    When an `Undate` instance is initialized, internally the class calculates earliest and latest possible values for that date in the Gregorian calendar.

    This means that some comparisons are possible even without precise information.

    For instance, is a year sometime during the 1900s before a month in late 2022?
    """
    )
    return


@app.cell
def _(late2022, someyear_1900s):
    someyear_1900s < late2022
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""But uncertain dates with the same initial values aren't equal, since they are uncertain:"""
    )
    return


@app.cell
def _(Undate, late2022):
    late2022 == Undate(2022, "1X")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The `Undate` class has properties to return `year`, `month`, and `day` if they are known. They are returned as strings to allow for partially unknown dates, and return `None` when a value is unknown.

    Here are some examples from the dates we created earlier.
    """
    )
    return


@app.cell
def _(november7_1, someyear_1900s, year2k):
    assert november7_1.year == "2000"
    assert november7_1.month == "11"
    assert november7_1.day == "07"
    assert year2k.year == "2000"
    assert year2k.month is None
    assert year2k.day is None
    assert someyear_1900s.year == "19XX"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Date Intervals

    Like many other date libraries, `undate` includes support for intervals.  An `UndateInterval` is a date range between two `Undate` objects. Intervals can be open-ended, allow for optional labels, and can calculate duration if enough information is known.
    """
    )
    return


@app.cell
def _(Undate):
    from undate import UndateInterval

    nineteenth_c = UndateInterval(Undate(1801), Undate(1900), label="19th century")
    nineteenth_c
    return UndateInterval, nineteenth_c


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    An `UndateInterval` has an earliest and a latest value for the start and end of the date range. Since those are `Undate` instances, they also have earliest and latest values.

    The duration of an interval is calculated based on the difference between the last day and first day in range.
    """
    )
    return


@app.cell
def _(nineteenth_c):
    print(nineteenth_c.earliest.earliest)
    return


@app.cell
def _(nineteenth_c):
    print(nineteenth_c.latest.latest)
    return


@app.cell
def _(nineteenth_c):
    nineteenth_c.duration()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Intervals can also be open-ended.  Here are a couple of examples:""")
    return


@app.cell
def _(Undate, UndateInterval):
    UndateInterval(latest=Undate(2000))  # before 2000
    return


@app.cell
def _(Undate, UndateInterval):
    UndateInterval(Undate(1900))  # after 1900
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Parsing dates in supported formats

    Initializing an `Undate` directly with year, month, day values is useful, but often we want to parse text dates in known formats directly and work with them as data.

    The `undate` library has an extensive converter class ([`BaseDateConverter`](https://undate-python.readthedocs.io/en/latest/undate/converters.html)), which can be extended for parsing dates in specific formats and also for parsing and converting dates from other calendars.  Parsing is implemented with the Python library [Lark](https://lark-parser.readthedocs.io/en/stable/).

    Currently, we support ISO8601 and some portions of the Extended Date Time Format (EDTF).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### ISO8601

    **ISO 8601** is an international standard for dates (see [Wikipedia ISO 8601 entry](https://en.wikipedia.org/wiki/ISO_8601) for more details). For Calendar dates, this format uses the familiar **YYYY-MM-DD** notation for full dates, **YYYY-MM** for year and month. Some earlier versions of the specification allowed formats like **--MM-DD** for dates when month and day are known but the year is not.

    A converter can be used directly by the class, or can be parsed by the name of the converter.

    Here are some examples. In this case, we set the default converter to ISO8601 so that the string format will serialize the date back out to the original format.
    """
    )
    return


@app.cell
def _(Undate):
    from undate.date import DatePrecision
    from undate.converters.iso8601 import ISO8601DateFormat

    Undate.DEFAULT_CONVERTER = "ISO8601"
    _day = Undate.parse("1985-04-12", "ISO8601")
    assert str(_day) == "1985-04-12"
    assert _day.precision == DatePrecision.DAY
    _yearmonth = Undate.parse("1985-04", "ISO8601")
    assert str(_yearmonth) == "1985-04"
    assert _yearmonth.precision == DatePrecision.MONTH
    _year = Undate.parse("1985", "ISO8601")
    assert str(_year) == "1985"
    assert _year.precision == DatePrecision.YEAR
    _monthday = Undate.parse("--04-12", "ISO8601")
    assert str(_monthday) == "--04-12"
    assert _monthday.precision == DatePrecision.DAY
    return (DatePrecision,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""If you try to parse something that isn't supported by the format or the parser, the method raises a `ValueError` exception with the error message from the parser."""
    )
    return


@app.cell
def _(Undate):
    try:
        Undate.parse("????-04-12", "ISO8601")
    except ValueError as err:
        print(err)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Extendend Date Time Format

    Since the EDTF format includes both dates and intervals, parsing an EDTF can return either an `Undate` or an `UndateInterval`.  

    Here are some examples.   

    EDTF and ISO8601 use the same format for full precision day, year-month, and year dates.
    """
    )
    return


@app.cell
def _(DatePrecision, Undate):
    _day = Undate.parse("1985-04-12", "EDTF")
    assert _day.format("EDTF") == "1985-04-12"
    assert _day.precision == DatePrecision.DAY
    _yearmonth = Undate.parse("1985-04", "EDTF")
    assert _yearmonth.format("EDTF") == "1985-04"
    assert _yearmonth.precision == DatePrecision.MONTH
    _year = Undate.parse("1985", "EDTF")
    assert _year.format("EDTF") == "1985"
    assert _year.precision == DatePrecision.YEAR
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    EDTF uses **X** to indicate unspecified digits. Here's the example from above with an unknown year. 

    If we specify a different formatter, we can output the date in a different format than we used for parsing.
    """
    )
    return


@app.cell
def _(DatePrecision, Undate):
    _monthday = Undate.parse("XXXX-04-12", "EDTF")
    assert _monthday.format("EDTF") == "XXXX-04-12"
    assert _monthday.format("ISO8601") == "--04-12"
    assert _monthday.precision == DatePrecision.DAY
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""The EDTF format includes notation for intervals; parsing an EDTF interval returns an `UndateInterval`. Here are some examples from the Library of Congress documentation on EDTF. Note that the start and end date of the interval don't have to use the same date precision."""
    )
    return


@app.cell
def _(DatePrecision, Undate, UndateInterval):
    # Example 1
    year_range = Undate.parse("1964/2008", "EDTF")
    assert isinstance(year_range, UndateInterval)
    assert year_range.earliest == Undate(1964)
    assert year_range.latest == Undate(2008)
    # Example 2
    month_range = Undate.parse("2004-06/2006-08", "EDTF")
    assert isinstance(month_range, UndateInterval)
    assert month_range.earliest == Undate(2004, 6)
    assert month_range.latest == Undate(2006, 8)
    # Example 3
    day_range = Undate.parse("2004-02-01/2005-02-08", "EDTF")
    assert isinstance(day_range, UndateInterval)
    assert day_range.earliest == Undate(2004, 2, 1)
    assert day_range.latest == Undate(2005, 2, 8)
    # Example 4
    day_month_range = Undate.parse("2004-02-01/2005-02", "EDTF")
    assert isinstance(day_range, UndateInterval)
    assert day_month_range.earliest == Undate(2004, 2, 1)
    assert day_month_range.latest == Undate(2005, 2)
    assert day_month_range.earliest.precision == DatePrecision.DAY
    assert day_month_range.latest.precision == DatePrecision.MONTH
    # Example 5
    day_year_range = Undate.parse("2004-02-01/2005", "EDTF")
    assert isinstance(day_range, UndateInterval)
    assert day_year_range.earliest == Undate(2004, 2, 1)
    assert day_year_range.latest == Undate(2005)
    assert day_year_range.earliest.precision == DatePrecision.DAY
    assert day_year_range.latest.precision == DatePrecision.YEAR
    # Example 6
    year_month_range = Undate.parse("2005/2006-02", "EDTF")
    assert isinstance(year_month_range, UndateInterval)
    assert year_month_range.earliest == Undate(2005)
    assert year_month_range.latest == Undate(2006, 2)
    assert year_month_range.earliest.precision == DatePrecision.YEAR
    assert year_month_range.latest.precision == DatePrecision.MONTH
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""EDTF also supports open intervals. Here are some examples of those:"""
    )
    return


@app.cell
def _(DatePrecision, Undate, UndateInterval, datetime):
    interval = Undate.parse("1985-04-12/..", "EDTF")
    assert isinstance(interval, UndateInterval)
    assert interval.earliest == datetime.date(1985, 4, 12)
    assert interval.earliest.precision == DatePrecision.DAY
    assert interval.latest is None

    interval = Undate.parse("1985-04/..", "EDTF")
    assert isinstance(interval, UndateInterval)
    assert interval.earliest == Undate(1985, 4)
    assert interval.earliest.precision == DatePrecision.MONTH
    assert interval.latest is None

    interval = Undate.parse("1985/..", "EDTF")
    assert isinstance(interval, UndateInterval)
    assert interval.earliest == Undate(1985)
    assert interval.earliest.precision == DatePrecision.YEAR
    assert interval.latest is None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""EDTF also supports negative years and years that are more than four digits; the **Y** prefix is used to indicate the number is a year."""
    )
    return


@app.cell
def _(Undate):
    neg_year = Undate.parse("-1985", "EDTF")
    assert neg_year.year == "-1985"
    assert Undate(-1985).format("EDTF") == "-1985"

    assert Undate.parse("Y170000002", "EDTF").year == "170000002"
    assert Undate(170000002).format("EDTF") == "Y170000002"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Calendars

    `undate` includes a [BaseCalendarConverter](https://undate-python.readthedocs.io/en/latest/undate/converters.html#undate.converters.base.BaseCalendarConverter), as a special case of the `BaseDateConverter` for format parsing and conversion like ISO8601 and EDTF. In addition the `parse()` method that all converters must implement, calendar converters have logic for returning minimum and maximum month and day, first and last month as integers (since some calendars don't start the year on month 1), and a `to_gregorian()` method to convert into a standard Gregorian date. We use the [convertdate](https://github.com/fitnr/convertdate) Python library for the actual numeric conversion.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Gregorian calendar

    An `Undate` instance always has a calendar defined; we use the Gregorian calendar if a calendar is not specified.

    Here's an example from one of the `Undate` instances we defined earlier:
    """
    )
    return


@app.cell
def _(november7_1):
    november7_1.calendar
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Islamic Hijri calendar""")
    return


@app.cell
def _(DatePrecision, Undate):
    from undate import Calendar

    # Monday, 7 Jumādā I 1243 Hijrī (26 November, 1827 CE); Jumada I = month 5
    hijri_date = Undate.parse("7 Jumādā I 1243", "Islamic")
    assert hijri_date == Undate(1243, 5, 7, calendar="Islamic")
    assert hijri_date.calendar == Calendar.ISLAMIC
    assert hijri_date.precision == DatePrecision.DAY
    return Calendar, hijri_date


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""We preserve the numeric values of the date in the original calendar, but internally `Undate` converts to Gregorian calendar for comparison with other days."""
    )
    return


@app.cell
def _(hijri_date):
    assert hijri_date.year == "1243"
    assert hijri_date.month == "05"
    assert hijri_date.day == "07"
    print(hijri_date.earliest)  # Gregorian equivalent
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""By default, the original text value of the parsed date and the calendar are presreved in the label of the `Undate` object:"""
    )
    return


@app.cell
def _(hijri_date):
    print(hijri_date.label)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""As with other formats, we support different date precisions:""")
    return


@app.cell
def _(Calendar, DatePrecision, Undate):
    from undate.date import Date

    # month and year only
    hijri_yearmonth = Undate.parse("Rajab 495", "Islamic")
    assert hijri_yearmonth == Undate(
        495, 7, calendar="Islamic"
    )  # Rajab is month 7
    assert hijri_yearmonth.calendar == Calendar.ISLAMIC
    assert hijri_yearmonth.precision == DatePrecision.MONTH
    # Gregorian earliest/latest
    assert hijri_yearmonth.earliest == Date(1102, 4, 28)
    assert hijri_yearmonth.latest == Date(1102, 5, 27)
    print(
        f"{hijri_yearmonth.earliest}/{hijri_yearmonth.latest}"
    )  # Gregorian date range
    return (Date,)


@app.cell
def _(Calendar, Date, DatePrecision, Undate):
    # year only
    hijri_year = Undate.parse("441", "Islamic")
    assert hijri_year == Undate(441, calendar="Islamic")
    assert hijri_year.calendar == Calendar.ISLAMIC
    assert hijri_year.precision == DatePrecision.YEAR
    # Gregorian earliest/ latest
    assert hijri_year.earliest == Date(1049, 6, 11)
    assert hijri_year.latest == Date(1050, 5, 31)
    print(f"{hijri_year.earliest}/{hijri_year.latest}")  # Gregorian date range
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Hebrew Anno Mundi calendar

    Support for the Hebrew calendar is similar to the Islamic.
    """
    )
    return


@app.cell
def _(Calendar, DatePrecision, Undate):
    # 26 Tammuz 4816: Tammuz = month 4 (17 July, 1056 Gregorian)
    hebrew_date = Undate.parse("26 Tammuz 4816", "Hebrew")
    assert hebrew_date == Undate(4816, 4, 26, calendar="Hebrew")
    assert hebrew_date.calendar == Calendar.HEBREW
    assert hebrew_date.precision == DatePrecision.DAY
    print(hebrew_date.earliest)  # Gregorian equivalent
    print(hebrew_date.label)
    return


@app.cell
def _(Calendar, DatePrecision, Undate):
    # year month
    hebrew_yearmonth = Undate.parse("Ṭevet 5362", "Hebrew")
    assert hebrew_yearmonth == Undate(
        5362, 10, calendar="Hebrew"
    )  # Teveth = month 10
    assert hebrew_yearmonth.calendar == Calendar.HEBREW
    assert hebrew_yearmonth.precision == DatePrecision.MONTH
    print(
        f"{hebrew_yearmonth.earliest}/{hebrew_yearmonth.latest}"
    )  # Gregorian date range
    return


@app.cell
def _(Calendar, DatePrecision, Undate):
    # year
    hebrew_year = Undate.parse("4932", "Hebrew")
    assert hebrew_year == Undate(4932, calendar="Hebrew")
    assert hebrew_year.calendar == Calendar.HEBREW
    assert hebrew_year.precision == DatePrecision.YEAR
    print(f"{hebrew_year.earliest}/{hebrew_year.latest}")  # Gregorian date range
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Because we preserve the numeric date values in the original calendar, this means that two `Undate` objects with the same numeric day, month, and year values represent different dates if they use different calendars.  This also means that we can preserve the precision of the date in the original calendar (such as a month or a year), even when that doesnn't neatly map to a month or year in the Gregorian calendar, since they may have a different number of days.

    Since `Undate` converts to the common Gregorian calendar for comparison and determines earliest and latest possible dates, `Undate` instances with different calendars can be used together.
    """
    )
    return


@app.cell
def _(Undate):
    # 21 Rajab 1023 Hijrī (27 August 1614 CE)
    rajab21 = Undate.parse("21 Rajab 1023", "Islamic")
    # 3 Tishrei 5370 Anno Mundi (1 October 1609 CE)
    tishrei3 = Undate.parse("3 Tishrei 5370", "Hebrew")
    return rajab21, tishrei3


@app.cell
def _(rajab21):
    rajab21
    return


@app.cell
def _(tishrei3):
    tishrei3
    return


@app.cell
def _(Undate):
    import pandas as pd

    calendars = ["Gregorian", "Hebrew", "Islamic"]

    calendar_dates = {
        "text": [
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
        # we pre-supply the numeric values int his case, since we don't yet have a text parser for Gregorian dates
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

    cal_dates_df = pd.DataFrame.from_dict(calendar_dates)
    # initialize an undate by parsing text values with specified calendar
    cal_dates_df["undate"] = cal_dates_df.apply(
        lambda row: Undate(*row.numeric, calendar=row.calendar), axis=1
    )
    # string representation of how you would intiialize an undate object with numbers and calendar
    cal_dates_df["undate_str"] = cal_dates_df.apply(
        lambda row: f"Undate({', '.join([str(n) for n in row.numeric])}, calendar='{row.calendar}')",
        axis=1,
    )
    cal_dates_df["precision"] = cal_dates_df.undate.apply(
        lambda x: str(x.precision).lower()
    )
    cal_dates_df["earliest_gregorian"] = cal_dates_df.undate.apply(
        lambda x: x.earliest
    )
    cal_dates_df["latest_gregorian"] = cal_dates_df.undate.apply(
        lambda x: x.latest
    )
    cal_dates_df["duration"] = cal_dates_df.undate.apply(
        lambda x: x.duration().days
    )
    cal_dates_df
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""This table shows dates with varying precision from three different calendars, with their numeric values in the original calendar and earliest and latest Gregorian dates."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    * * *

    Because internally we convert to a common calendar, these dates can be used together.
    """
    )
    return


@app.cell
def _(Undate, rajab21, tishrei3):
    june1663 = Undate(1663, 6)

    sorted_mix = sorted([rajab21, tishrei3, june1663])
    sorted_mix
    return (sorted_mix,)


@app.cell
def _(sorted_mix):
    print([d.earliest for d in sorted_mix])
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
                src="assets/stein_lendingcard_unknownyear.jpg",
                alt="Detail from one of Gertrude Stein's lending library cards",
                width="70%",
                caption="Gertrude Stein borrowing activity, unknown year",
            ),
            mo.md(r"""This project provides an example of how partially unknown dates can still be computationally useful. If we make the reasonable assumption that for borrowing activity like this, with an unknown year, books were returned in the same or following year, then we can calculate how long the books were borrowed and include them in analysis of library member activities.

    Here we demonstrate this using the borrowing events from the Shakespeare and Company Project 2.0 dataset.
    """),
        ],
        align="center",
    )
    return


@app.cell
def _(pd):
    # load the 2.0 version of S&co events data from the assets folder
    events_df = pd.read_csv(
        "assets/SCoData_events_v2.0_2025.csv", low_memory=False
    )

    # filter the full dataset to just borrowing events
    borrow_events = events_df[events_df.event_type == "Borrow"]
    # limit the dataframe to relevant fields
    borrow_events = borrow_events[
        ["start_date", "end_date", "member_names", "item_title", "item_authors"]
    ]
    # for convenience, filter to rows that have both start and end date
    borrow_events = borrow_events[
        borrow_events.start_date.notna() & borrow_events.end_date.notna()
    ]
    borrow_events.head(10)
    return (borrow_events,)


@app.cell
def _(Undate, borrow_events):
    borrow_events["start_undate"] = borrow_events.start_date.apply(
        lambda x: Undate.parse(x, "ISO8601")
    )
    borrow_events["end_undate"] = borrow_events.end_date.apply(
        lambda x: Undate.parse(x, "ISO8601")
    )
    borrow_events["start_date_precision"] = borrow_events.start_undate.apply(
        lambda x: str(x.precision)
    )
    borrow_events["end_date_precision"] = borrow_events.end_undate.apply(
        lambda x: str(x.precision)
    )
    borrow_events_1 = borrow_events[
        (borrow_events.start_date_precision == "DAY")
        & (borrow_events.end_date_precision == "DAY")
    ]
    borrow_events_1 = borrow_events_1.drop(
        columns=["start_date_precision", "end_date_precision"]
    )
    borrow_events_1.head(10)
    return (borrow_events_1,)


@app.cell
def _(borrow_events_1):
    borrow_events_1[borrow_events_1.start_date == borrow_events_1.end_date]
    return


@app.cell
def _(Undate, UndateInterval, borrow_events_1):
    def undate_duration(start, end):
        if start.known_year and (not end.known_year):
            start = Undate(month=start.month, day=start.day)
        try:
            return UndateInterval(earliest=start, latest=end).duration().days
        except ValueError as err:
            if str(start) == str(end):
                return 1


    borrow_events_1["duration_days"] = borrow_events_1.apply(
        lambda row: undate_duration(row.start_undate, row.end_undate), axis=1
    )
    borrow_events_1[
        [
            "start_undate",
            "end_undate",
            "member_names",
            "item_title",
            "item_authors",
            "duration_days",
        ]
    ].head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Being able to calculate durations for partially known dates means they can be included in analysis and interpretation of member borrowing activity, such as books that were borrowed and returned quickly or checked out for longer times, and included in broader analysis of borrowing behavior across all library members or specific individuals."""
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Princeton Geniza Project""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The [Princeton Geniza Project](https://geniza.princeton.edu/) is a database of texts that were preserved in a medieval synagogue in Cairo, Egypt.

    The texts are predominantly written in Hebrew script, are often fragmentary, and in many cases they are difficult to place in time. Because of the context of these materials, they use a mix of calendars.

    Here we demonstrate undate capabilities using the set of documents with known dates set in the metadata.  The dataset includes original dates and calendars and standardized dates (using Common Era dates; Julian before 1583, Gregorian after).
    """
    )
    return


@app.cell
def _(pd):
    # load a copy of PGP document data from the assets folder
    pgp_documents = pd.read_csv("assets/pgp_documents.csv")

    # limit to document dates with standardized format, so we have a comparison point
    docs_with_docdate = pgp_documents[
        pgp_documents.doc_date_standard.notna()
    ].copy()
    # limit to a subset of fields
    docs_with_docdate = docs_with_docdate[
        [
            "pgpid",
            "shelfmark",
            "type",
            "doc_date_original",
            "doc_date_calendar",
            "doc_date_standard",
        ]
    ]
    # limit to the calendars undate currently supports
    docs_with_docdate = docs_with_docdate[
        docs_with_docdate.doc_date_calendar.isin(
            ["Anno Mundi", "Hijrī", "Seleucid"]
        )
    ]

    docs_with_docdate.head()
    return (docs_with_docdate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Limiting to just the Hebrew and Islamic calendar dates still gives us a nice mix of content to work with."""
    )
    return


@app.cell
def _(docs_with_docdate):
    docs_with_docdate.doc_date_calendar.value_counts()
    return


@app.cell
def _(Undate, docs_with_docdate):
    # Use undate to parse the original dates based on calendar

    from lark.exceptions import UnexpectedEOF, VisitError


    def parse_original_date(row):
        if row.doc_date_calendar == "Anno Mundi":
            undate_calendar = "Hebrew"
        elif row.doc_date_calendar == "Hijrī":
            undate_calendar = "Islamic"
        elif row.doc_date_calendar == "Seleucid":
            undate_calendar = "Seleucid"

        try:
            return Undate.parse(row.doc_date_original, undate_calendar)
        except (VisitError, ValueError, UnexpectedEOF):
            # we don't support parsing everything in this dataset, and some of them have errors
            # for demonstration purposes, ignore anything we can't parse
            pass


    docs_with_docdate["undate_orig"] = docs_with_docdate.apply(
        parse_original_date, axis=1
    )
    return


@app.cell
def _(docs_with_docdate):
    # limit to the records that were successfully parsed
    docs_with_undate = docs_with_docdate[
        docs_with_docdate.undate_orig.notna()
    ].copy()

    docs_with_undate.head(10)
    return (docs_with_undate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We can compare `undate` standardized earliest/latest values with the standardized dates provided in the dataset.

    For the dates before 1583 we expect to se a few days difference, due to the use of Julian calendar.
    """
    )
    return


@app.cell
def _(docs_with_undate):
    # compare undate standardized earliest/latest values with the standardized dates in the dataset

    docs_with_undate["undate_earliest"] = docs_with_undate.undate_orig.apply(
        lambda x: x.earliest
    ).astype("datetime64[s]")
    docs_with_undate["undate_latest"] = docs_with_undate.undate_orig.apply(
        lambda x: x.latest
    ).astype("datetime64[s]")
    # limit and order fields to help make the comparison
    docs_with_undate[
        [
            "doc_date_original",
            "doc_date_calendar",
            "undate_orig",
            "doc_date_standard",
            "undate_earliest",
            "undate_latest",
        ]
    ].head(10)
    return


@app.cell
def _(docs_with_undate):
    # we still have a mix of calendars
    docs_with_undate.doc_date_calendar.value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Preserving calendar and date information, we can now do some analysis based on different aspects of these dates. 

    For instance, how are the documents distributed over the different months?
    """
    )
    return


@app.cell
def _(docs_with_undate):
    import altair as alt

    # get numeric month
    docs_with_undate["undate_month"] = docs_with_undate.undate_orig.apply(
        lambda x: x.month
    )

    docs_with_month = docs_with_undate[docs_with_undate.undate_month.notna()]


    alt.Chart(
        docs_with_month[["undate_month", "pgpid", "doc_date_calendar"]]
    ).mark_rect().encode(
        alt.X("undate_month", title="month"),
        alt.Color("count(pgpid)", title="# of documents"),
    ).facet(
        row=alt.Facet("doc_date_calendar", title="Original Calendar")
    ).properties(title="Document frequency by month and calendar")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""There's a month 13 that doesn't exist in the Islamic calendar, shows up on the Hebrew calendar with much fewer documents — that's because the Hebrew calendar includes a leap _month_. Because that month doesn't happen every year, we would expect to see far fewer documents - as evidenced in the heatmap."""
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

    mo.md(
        f"""
    ## Resources 


    - _Shakespeare and Company Project_. 2020. Publisher: Center for Digital Humanities, Princeton University. https://shakespeareandco.princeton.edu/. {my_icons.website}
    - _Princeton Geniza Project_. 2022. Publisher: Center for Digital Humanities, Princeton University. https://geniza.princeton.edu/. {my_icons.website}
    - Library of Congress. 2019. Extended Date Time Format (EDTF) Specification. Library of Congress, February. Accessed March 30, 2025. https://www.loc.gov/standards/datetime/. {my_icons.article}
    - Koeser, Rebecca Sutton, Cole Crawford, Julia Damerow, Malte Vogl, and Robert Casties. “Undate Python Library”. Zenodo, July 22, 2025. https://doi.org/10.5281/zenodo.16328670. {my_icons.code}
    - Koeser, Rebecca Sutton, and Zoe LeBlanc. 2024. Missing Data, Speculative Reading. _Journal of Cultural Analytics_ 9, no. 2 (May). https://doi.org/10.22148/001c.116926 {my_icons.article}
    - Koeser, Rebecca Sutton & Kotin, Joshua. (2025). Shakespeare and Company Project Datasets [Data set]. Version 2. Princeton University. https://doi.org/10.34770/kf6c-b079 {my_icons.dataset}
    - Kotin, Joshua and Rebecca Sutton Koeser. 2022. Shakespeare and Company Project Data Sets. _Journal of Cultural Analytics_ 7, no. 1 (February). https://doi.org/10.22148/001c.32551 {my_icons.article}
    """
    )
    return


if __name__ == "__main__":
    app.run()
