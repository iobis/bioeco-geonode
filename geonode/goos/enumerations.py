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

READINESS_LEVELS = (
    ("1", _("Level 1 - Idea")),
    ("2", _("Level 2 - Documentation")),
    ("3", _("Level 3 - Proof of concept")),
    ("4", _("Level 4 - Trial")),
    ("5", _("Level 5 - Verification")),
    ("6", _("Level 6 - Operational")),
    ("7", _("Level 7 - Fitness for purpose")),
    ("8", _("Level 8 - Mission qualified")),
    ("9", _("Level 9 - Sustained"))
)
