from django.utils.translation import ugettext_lazy as _


UPDATE_FREQUENCIES = (
    ("sub_daily", _("Sub-daily")),
    ("daily", _("Daily")),
    ("monthly", _("Monthly (12x per year)")),
    ("quarterly", _("Quarterly (4x per year)")),
    ("twice_per_year", _("2x per year")),
    ("annually", _("1x per year")),
    ("every_2_to_5_years", _("1x every 2 to 5 years")),
    ("every_6_to_10_years", _("1x every 6 to 10 years")),
    ("every_10_years_or_more", _("1x every >10 years")),
    ("opportunistically", _("opportunistically/highly irregular intervals"))
)
