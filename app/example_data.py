from datetime import date
services = [
        {"name": "Access Now", "likely_eligible": True },
        {"name": "Cross Over", "likely_eligible": False },
        {"name": "Daily Planet", "likely_eligible": True },
        {"name": "Resource centers", "likely_eligible": False },
        ]


example_patient = {
        "id": 432,
        "firstname": "Robert",
        "mi": "L",
        "middlename": "LOL",
        "lastname": "Loblobbleson",
        "full_name": "Robert Loblobbleson",
        "age": 28,
        "dob": date(1987, 12, 14),
        "gender": "male",
        "main_phone": {
          "number": "408-484-8484",
          "name": "Main cell phone"
        },
        "ssn": "333-33-3333",
        "phone_numbers": [
          {
            "number": "408-848-4848",
            "name": "Other cell phone"
          },
          {
            "number": "408-777-7777",
            "name": "Sister's cell phone"
          }
        ],
        "addresses": [
          {
            "type": "Mail",
            "street_address": "P.O. Box 45873",
            "city": "Richmond",
            "state": "VA",
            "zip": 23218
          },
          {
            "type": "Home",
            "street_address": "5561 Newbourne St.",
            "apt_number": "Apt. C",
            "city": "Richmond",
            "state": "VA",
            "zip": 23227
          }
        ],
        "emergency_contact": {
          "name": "Tulip Loblobbleson",
          "relation": "Sister",
          "phone": "408-777-7777"
        },
        "documents": [
          {
            "title": "W-2, 2014",
            "date_added": "2015-01-16T00:00:00.000Z",
            "thumbnail_url": "https://github.com/codeforamerica/rva-screening/blob/templating/images/w2.jpg?raw=true"
          },
          {
            "title": "Paystubs, Jan 1st - Jan 14th, 2014",
            "date_added": "2015-01-16T00:00:00.000Z",
            "thumbnail_url": "https://raw.githubusercontent.com/codeforamerica/rva-screening/0e43541aa40f6f1a4f55100c3d44b4d2565a344c/images/paystub.jpg"
          }
        ],
        "hh_members": [
          {
            "full_name": "Hobert Hobobleson",
            "age": 7,
            "relation": "Nephew",
            "number": 2
          },
          {
            "full_name": "Tulip Loblobbleson",
            "age": 29,
            "relation": "Sister",
            "number": 3
          }
        ],
        "income_sources": [
          {
            "source_type": "Wages",
            "amount_per_month": 608
          },
          {
            "source_type": "Food Stamps",
            "amount_per_month": 539.4
          }
        ]
      }

patients = [
        { "id": 1, "firstname": "Mikhail", "middlename": "Y", "lastname": "Gorbachev",
            "dob": date(1852, 03, 30) },
        example_patient,
        ]
