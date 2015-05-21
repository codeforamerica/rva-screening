from datetime import date

YN_CHOICES = [("Y", "Yes"), ("N", "No")]
YNN_CHOICES = [("Y", "Yes"), ("N", "No"), ("", "Not Sure")]

STATE_CHOICES =[ ("AL", "AL - Alabama"), ("AK", "AK - Alaska"),
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
            ("WA", "WA - Washington"), ("WV", "WV - West VirginiaVA"),
            ("WI", "WI - Wisconsin"), ("WY", "WY - Wyoming"),
      ]

HOUSING_STATUS_CHOICES = [
        ("REN", "Renting"), ("OWN", "Owns home (self or family)"),
        ("SOM", "Lives with someone"),
        ("TEM", "Lives temporarily with family or friends"),
        ("TRA", "Is in Transitional housing for the homeless"),
        ("EMR", "Emergency Shelter"),
        ("STR", "On the street (car, encampment, abandoned building)"),
        ("other", "Other")]

EMPLOYMENT_STATUS_CHOICES = [
        ("FT", "Full-time"), ("PT", "Part-time"), ("SEA", "Seasonal"),
        ("DIS", "Disabled"), ("RET", "Retired"), ("DEP", "Dependent"),
        ("UNE", "Unemployed"),
        ]

MARITAL_STATUS_CHOICES = [("SIM", "Single"), ("MAR", "Married"),
        ("DIV", "Divorced"), ("WID", "Widowed"), ("SEP", "Legally Separated"),
        ("PAR", "Partner")]

RACE_CHOICES = [("AIAN", "American Indian/Alaskan Native"), ("A", "Asian"),
        ("AA", "Black or African-American"),
        ("NHPI", "Native Hawaiian/Pacific Islander"), ("W", "White"),
        ("other", "Other")]

ETHNICITY_CHOICES = [("HL","Hispanic or Latino"),
        ("NHL","Not Hispanic or Latino")]

RELATIONSHIPS = (
        "brother", "mother", "sister", "aunt",
        "son", "daughter", "grandmother", "granddaughter",
        "grandfather", "grandson", "uncle", "nephew",
        "niece", "partner", "friend", "father" )

ADDRESS_TYPES = (
        "mailing", "home", "street", "temporary", "shelter")

PHONE_TYPES = (
        "cell phone", "home phone", "temporary cell phone",
        "work phone", "shelter phone" )

GENDER_CHOICES = ("M","F","")

services = [
        {"name": "Access Now", "likely_eligible": True },
        {"name": "Cross Over", "likely_eligible": False },
        {"name": "Daily Planet", "likely_eligible": True },
        {"name": "Resource centers", "likely_eligible": False },
        ]

example_patient = {
        "id": 432,
        "first_name": "Robert",
        "middle_name": "LOL",
        "last_name": "Loblobbleson",
        "full_name": "Robert Loblobbleson",
        "dob": date(1987, 12, 14),
        "gender": "male",
        "ssn": "333-33-3333",
        "insurances":[],
        "phone_numbers": [
            {
                "number": "408-484-8484",
                "description": "Main cell phone",
                "primary_yn": "Y",
            },
            {
                "number": "408-848-4848",
                "description": "Other cell phone",
                "primary_yn": "n",
            },
            {
                "number": "408-777-7777",
                "description": "Sister's cell phone",
                "primary_yn": "n",
            }
        ],
        "addresses": [
            {
                "description": "Mail",
                "address": "P.O. Box 45873",
                "city": "Richmond",
                "state": "VA",
                "zip": "23218"
            },
            {
                "description": "Home",
                "street_address": "5561 Newbourne St.",
                "apt_number": "Apt. C",
                "city": "Richmond",
                "state": "VA",
                "zip": "23227"
            }
        ],
        "emergency_contacts": [
            {
                "name": "Tulip Loblobbleson",
                "relationship": "Sister",
                "phone_number": "408-777-7777"
            }
        ],
        "document_images": [
            {
                "description": "W-2, 2014",
                "date_uploaded": "2015-01-16T00:00:00.000Z",
                "thumbnail_url": "https://github.com/codeforamerica/rva-screening/blob/templating/images/w2.jpg?raw=true"
            },
            {
                "description": "Paystubs, Jan 1st - Jan 14th, 2014",
                "date_uploaded": "2015-01-16T00:00:00.000Z",
                "thumbnail_url": "https://raw.githubusercontent.com/codeforamerica/rva-screening/0e43541aa40f6f1a4f55100c3d44b4d2565a344c/images/paystub.jpg"
            }
],
    "household_members": [
        {
            "full_name": "Hobert Hobobleson",
            "age": 7,
            "relationship": "Nephew",
        },
        {
            "full_name": "Tulip Loblobbleson",
            "age": 29,
            "relationship": "Sister",
        }
    ],
"income_sources": [
    {
        "source": "Wages",
        "annual_amount": 7296
    },
    {
        "source": "Food Stamps",
        "annual_amount": 6472.8
    }
]
}

patients = [
        { "id": 1, "first_name": "Mikhail", "middle_name": "Y", "last_name": "Gorbachev",
            "dob": date(1852, 03, 30) },
        example_patient,
        ]
