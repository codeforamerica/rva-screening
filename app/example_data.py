from datetime import date

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
                "primary_yn": "y",
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
