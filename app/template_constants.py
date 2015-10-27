from flask.ext.babel import gettext as _

YN_CHOICES = [("", ""), ("Y", _("Yes")), ("N", _("No"))]
YN_NONULL_CHOICES = [("Y", _("Yes")), ("N", _("No"))]
YNN_CHOICES = [("", ""), ("Y", _("Yes")), ("N", _("No")), ("S", _("Not Sure"))]
YNN_NONULL_CHOICES = [("Y", _("Yes")), ("N", _("No")), ("", _("Not Sure"))]
YNNA_CHOICES = [("", ""), ("Y", _("Yes")), ("N", _("No")), ("A", _("N/A - Not Applicable"))]

GENDER_CHOICES = [("", ""), ("F", _("Female")), ("M", _("Male"))]
TRANSGENDER_CHOICES = [
    ("",    ""),
    ("No",  _("Not transgender")),
    ("FTM", _("Female to Male")),
    ("MTF", _("Male to Female"))
]

LANGUAGE_CHOICES = [
    ("EN",    _("English")),
    ("ES",    _("Spanish")),
    ("AR",    _("Arabic")),
    ("OTH",   _("Other"))
]

STATE_CHOICES = [
    ("AL", "AL - Alabama"), ("AK", "AK - Alaska"),
    ("AZ", "AZ - Arizona"), ("AR", "AR - Arkansas"),
    ("CA", "CA - California"), ("CO", "CO - Colorado"),
    ("CT", "CT - Connecticut"), ("DE", "DE - Delaware"),
    ("FL", "FL - Florida"), ("GA", "GA - Georgia"),
    ("HI", "HI - Hawaii"), ("ID", "ID - Idaho"),
    ("IL", "IL - Illinois"), ("IN", "IN - Indiana"),
    ("IA", "IA - Iowa"), ("KS", "KS - Kansas"),
    ("KY", "KY - Kentucky"), ("LA", "LA - Louisiana"),
    ("ME", "ME - Maine"), ("MD", "MD - Maryland"),
    ("MA", "MA - Massachusetts"), ("MI", "MI - Michigan"),
    ("MN", "MN - Minnesota"), ("MS", "MS - Mississippi"),
    ("MO", "MO - Missouri"), ("MT", "MT - Montana"),
    ("NE", "NE - Nebraska"), ("NV", "NV - Nevada"),
    ("NH", "NH - New Hampshire"), ("NJ", "NJ - New Jersey"),
    ("NM", "NM - New Mexico"), ("NY", "NY - New York"),
    ("NC", "NC - North Carolina"), ("ND", "ND - North Dakota"),
    ("OH", "OH - Ohio"), ("OK", "OK - Oklahoma"),
    ("OR", "OR - Oregon"), ("PA", "PA - Pennsylvania"),
    ("RI", "RI - Rhode Island"), ("SC", "SC - South Carolina"),
    ("SD", "SD - South DakotaND"), ("TN", "TN - Tennessee"),
    ("TX", "TX - Texas"), ("UT", "UT - Utah"),
    ("VT", "VT - Vermont"), ("VA", "VA - Virginia"),
    ("WA", "WA - Washington"), ("WV", "WV - West Virginia"),
    ("WI", "WI - Wisconsin"), ("WY", "WY - Wyoming"),
]

HOUSING_STATUS_CHOICES = [
    ("",      ""),
    ("REN",   _("Renting")),
    ("OWN",   _("Owns home (self or family)")),
    ("SOM",   _("Lives with someone")),
    ("TEM",   _("Lives temporarily with family or friends")),
    ("TRA",   _("Is in Transitional housing for the homeless")),
    ("EMR",   _("Emergency Shelter")),
    ("STR",   _("On the street (car, encampment, abandoned building)")),
    ("OTH", _("Other"))
]

EMPLOYMENT_STATUS_CHOICES = [
    ("",    ""),
    ("FT",  _("Full-time")),
    ("PT",  _("Part-time")),
    ("SEA", _("Seasonal")),
    ("DIS", _("Disabled")),
    ("RET", _("Retired")),
    ("DEP", _("Dependent")),
    ("UNE", _("Unemployed")),
]

EMPLOYEE_CHOICES = [
    ("Patient", _("Patient")),
    ("Spouse",  _("Spouse"))
]

STUDENT_STATUS_CHOICES = [
    ("",              ""),
    ("Not a student", _("Not a student")),
    ("Full-time",     _("Full-time")),
    ("Part-time",     _("Part-time"))
]

MARITAL_STATUS_CHOICES = [
    ("",    ""),
    ("SIM", _("Single")),
    ("MAR", _("Married")),
    ("DIV", _("Divorced")),
    ("WID", _("Widowed")),
    ("SEP", _("Legally Separated")),
    ("PAR", _("Partner"))
]

RACE_CHOICES = [
    ("AIAN",  _("American Indian/Alaskan Native")),
    ("A",     _("Asian")),
    ("AA",    _("Black or African-American")),
    ("NHPI",  _("Native Hawaiian/Pacific Islander")),
    ("W",     _("White")),
    ("OTH",   _("Other"))
]

ETHNICITY_CHOICES = [
    ("",    ""),
    ("HL",  _("Hispanic or Latino")),
    ("NHL", _("Not Hispanic or Latino"))
]

COVERAGE_ELIGIBILITY_CHOICES = [
    ("",    ""),
    ("JOB", _("Job")),
    ("PJOB", _("Parent's Job")),
    ("SJOB", _("Spouse's Job")),
    ("COB", _("COBRA")),
    ("OTH", _("Other")),
    ("NE", _("Not Eligible")),
]
COVERAGE_TYPE_CHOICES = [
    ("",      ""),
    ("PRIV",  _("Private Insurance")),
    ("MCAID", _("Medicaid")),
    ("MCARE", _("Medicare")),
    ("VA",    _("VA Healthcare")),
    ("VCC",   _("VCC")),
    ("VCUI",  _("VCU Indigent Care")),
    ("BSCC",  _("Bon Secours CareCard")),
    ("OTHER", _("Other")),
]

PHONE_DESCRIPTIONS = [
    ("",         ""),
    ("CELL",     _("Cell phone")),
    ("HOME",     _("Home phone / landline")),
    ("WORK",     _("Work number")),
    ("RELATIVE", _("Relative's phone number")),
    ("OTH",      _("Other"))
]

ADDRESS_DESCRIPTIONS = [
    ("",         ""),
    ("OWN",      _("Personal address / own or rent")),
    ("RELATIVE", _("Relative's address")),
    ("HOMELESS", _("Homeless shelter address")),
    ("OTH",      _("Other"))
]

TIME_AT_CURRENT_EMPLOYER = [
    ("",         ""),
    ("LESS",      _("Less than 1 year")),
    ("MIDDLE", _("1 to 2 years")),
    ("MORE", _("More than 2 years"))
]

TIME_IN_AREA = [
    ("",               ""),
    ("LESS THAN 6",    _("Less than 6 months")),
    ("GREATER THAN 6", _("More than 6 months")),
]
