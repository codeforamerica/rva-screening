#!/usr/bin/env python
import sys

from app import create_app
from app.models import (
    db,
    Service,
    ServiceReferralEmail,
    SlidingScale,
    SlidingScaleFee,
    ServiceLocation
)


def main(app=create_app()):
    with app.app_context():
        db.metadata.create_all(db.engine)

        daily_planet = Service(
            name='Daily Planet',
            description='The Daily Planet is a Community Healthcare Center providing team-based \
            integrated healthcare. This includes: primary and behavioral health, as well as \
            dental and eye care.',
            website_url='http://www.dailyplanetva.org/',
            main_contact_name='Teresa Kimm',
            main_contact_phone='(804) 783-2505',
            has_screening_yn='Y',
            fpl_cutoff=None,
            uninsured_only_yn='N',
            medicaid_ineligible_only_yn='N',
            residence_requirement_yn='N',
            time_in_area_requirement_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="The Daily Planet",
                    address="517 W Grace St. Richmond, VA 23220",
                    latitude=37.547508,
                    longitude=-77.447895
                ),
                ServiceLocation(
                    name="Southside Community Health Center",
                    address="180 Belt Blvd. Richmond, VA 23225",
                    latitude=37.509781,
                    longitude=-77.487185
                ),
                ServiceLocation(
                    name="St. Joseph\s Villa",
                    address="8000 Brook Road, Richmond, VA 23227",
                    latitude=37.632248,
                    longitude=-77.459127
                )
            ],
            sliding_scales=[
                SlidingScale(
                    scale_name='Nominal',
                    fpl_low=0,
                    fpl_high=100,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='Dental services',
                            price_percentage=30
                        ),
                        SlidingScaleFee(
                            name='Medical services',
                            price_absolute=10
                        ),
                        SlidingScaleFee(
                            name='Mental health services, initial visit of calendar month',
                            price_absolute=10
                        ),
                        SlidingScaleFee(
                            name='Mental health services, other visits',
                            price_absolute=5
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='Slide A',
                    fpl_low=100,
                    fpl_high=125,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='Dental services',
                            price_percentage=45
                        ),
                        SlidingScaleFee(
                            name='Medical services',
                            price_absolute=15
                        ),
                        SlidingScaleFee(
                            name='Mental health services, initial visit of calendar month',
                            price_absolute=15
                        ),
                        SlidingScaleFee(
                            name='Mental health services, second visit of calendar month',
                            price_absolute=10
                        ),
                        SlidingScaleFee(
                            name='Mental health services, other visits',
                            price_absolute=5
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='Slide B',
                    fpl_low=125,
                    fpl_high=150,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='Dental services',
                            price_percentage=55
                        ),
                        SlidingScaleFee(
                            name='Medical services',
                            price_absolute=20
                        ),
                        SlidingScaleFee(
                            name='Mental health services, initial visit of calendar month',
                            price_absolute=20
                        ),
                        SlidingScaleFee(
                            name='Mental health services, second visit of calendar month',
                            price_absolute=15
                        ),
                        SlidingScaleFee(
                            name='Mental health services, other visits',
                            price_absolute=5
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='Slide C',
                    fpl_low=150,
                    fpl_high=200,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='Dental services',
                            price_percentage=65
                        ),
                        SlidingScaleFee(
                            name='Medical services',
                            price_absolute=30
                        ),
                        SlidingScaleFee(
                            name='Mental health services, initial visit of calendar month',
                            price_absolute=30
                        ),
                        SlidingScaleFee(
                            name='Mental health services, second visit of calendar month',
                            price_absolute=25
                        ),
                        SlidingScaleFee(
                            name='Mental health services, other visits',
                            price_absolute=5
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='Full fee',
                    fpl_low=200,
                    fpl_high=None
                )
            ]
        )

        crossover = Service(
            name='CrossOver',
            description='CrossOver Healthcare Ministry provides quality and compassionate \
            health care to the uninsured in the greater Richmond Metropolitan area. Our \
            mission is to provide health care, promote wellness, and connect the talents \
            and resources of the community with people in need in the name of Jesus Christ. \
            CrossOver is here to serve and empower patients by providing a comprehensive \
            approach to health care for the body, mind, and spirit!',
            website_url='http://www.crossoverministry.org/',
            main_contact_name='Alex Chamberlain',
            main_contact_phone='(804) 521-8263',
            has_screening_yn='Y',
            fpl_cutoff=200,
            uninsured_only_yn='Y',
            medicaid_ineligible_only_yn='N',
            residence_requirement_yn='N',
            time_in_area_requirement_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="Cowardin",
                    address="108 Cowardin Ave, Richmond, VA 23224",
                    latitude=37.519541,
                    longitude=-77.449814
                ),
                ServiceLocation(
                    name="Quioccasin",
                    address="8600 Quioccasin Road, Suite 105, Richmond, VA 23229",
                    latitude=37.602507,
                    longitude=-77.565325
                )
            ],
            sliding_scales=[
                SlidingScale(
                    scale_name='All',
                    fpl_low=0,
                    fpl_high=None,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='Medications',
                            price_absolute=4
                        ),
                        SlidingScaleFee(
                            name='Nurse/Labs',
                            price_absolute=10
                        ),
                        SlidingScaleFee(
                            name='Vaccine clinic',
                            price_absolute=10
                        ),
                        SlidingScaleFee(
                            name='Medical visit/mental health',
                            price_absolute=15
                        ),
                        SlidingScaleFee(
                            name='Eye',
                            price_absolute=15
                        ),
                        SlidingScaleFee(
                            name='Same day appointments',
                            price_absolute=20
                        ),
                        SlidingScaleFee(
                            name='Dental',
                            price_absolute=20
                        )
                    ]
                )
            ]
        )

        access_now = Service(
            name='Access Now',
            description='The greater Richmond area has a vast network of safety-net health \
            clinics serving the primary care needs of the uninsured. These patients often also \
            need the care of a specialist to diagnose and treat their complex health issues. \
            When directors of local safety net clinics approached the Richmond Academy of \
            Medicine with requests to expand their network of specialists to meet this need, \
            the response was the development of Access Now. In January 2008, Access Now began \
            operations, providing access to specialists so that no patient would go without care \
            for lack of a willing provider. More than 900 specialists and physician extenders \
            open their doors to treat patients referred by Access Now.',
            website_url='http://www.ramdocs.org/?page=AccessNow',
            main_contact_name='Elizabeth Wong',
            main_contact_phone='(804) 643-6631',
            has_screening_yn='Y',
            fpl_cutoff=200,
            uninsured_only_yn='Y',
            medicaid_ineligible_only_yn='Y',
            residence_requirement_yn='Y',
            time_in_area_requirement_yn='Y',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="RAM",
                    address="2821 Emerywood Pkwy #200, Richmond, VA 23294",
                    latitude=37.608142,
                    longitude=-77.525421
                )
            ]
        )

        resource_centers = Service(
            name='RCHD Resource Centers',
            description='Resource Centers provide family planning and STI services, \
            health screenings, wellness services, nutrition education, community resource \
            information, budget management, and health education.',
            website_url='http://www.vdh.virginia.gov/LHD/richmondcity/clinic.htm',
            main_contact_name='Amy Popovich',
            main_contact_phone='(804) 205-3733',
            has_screening_yn='Y',
            fpl_cutoff=None,
            uninsured_only_yn='N',
            medicaid_ineligible_only_yn='N',
            residence_requirement_yn='N',
            time_in_area_requirement_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="Bellemeade Community Center",
                    address="1800 Lynhaven Avenue, Richmond, VA",
                    latitude=37.496315,
                    longitude=-77.440993
                ),
                ServiceLocation(
                    name="Broad Rock Community Center",
                    address="4615 Ferguson Lane, Richmond, VA",
                    latitude=37.477709,
                    longitude=-77.479711
                ),
                ServiceLocation(
                    name="Creighton Resource Center",
                    address="2150 Creighton Road, Richmond, VA",
                    latitude=37.546839,
                    longitude=-77.397964
                ),
                ServiceLocation(
                    name="Fairfield Resource Center",
                    address="2311 North 25th Street, Richmond, VA",
                    latitude=37.549656,
                    longitude=-77.403191
                ),
                ServiceLocation(
                    name="Gilpin Community Center",
                    address="436 Calhoun St, Richmond, VA",
                    latitude=37.554103,
                    longitude=-77.440609
                ),
                ServiceLocation(
                    name="Hillside Resource Center",
                    address="1615 Glenfield Avenue, Richmond, VA",
                    latitude=37.506280,
                    longitude=-77.432616
                ),
                ServiceLocation(
                    name="Mosby Resource Center",
                    address="1536 Coalter Street, Richmond, VA",
                    latitude=37.547104,
                    longitude=-77.419123
                ),
                ServiceLocation(
                    name="Whitcomb Resource Center",
                    address="2106 Deforrest Street, Richmond, VA",
                    latitude=37.556742,
                    longitude=-77.415224
                )
            ],
            sliding_scales=[
                SlidingScale(
                    scale_name='A',
                    fpl_low=0,
                    fpl_high=100,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=0
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='B',
                    fpl_low=100,
                    fpl_high=110,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=10
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='C',
                    fpl_low=110,
                    fpl_high=133,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=25
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='D',
                    fpl_low=133,
                    fpl_high=167,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=50
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='E',
                    fpl_low=167,
                    fpl_high=200,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=75
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='F',
                    fpl_low=200,
                    fpl_high=250,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=95
                        )
                    ]
                ),
                SlidingScale(
                    scale_name='G',
                    fpl_low=250,
                    fpl_high=None,
                    sliding_scale_fees=[
                        SlidingScaleFee(
                            name='All services',
                            price_percentage=100
                        )
                    ]
                ),
            ]
        )

        oar = Service(
            name='OAR',
            description='OAR of Richmond is the leading reentry service provider for \
            former offenders returning to the Richmond, Virginia area. OAR provides \
            services in 5 local jails and Reentry Services in our downtown Richmond, \
            Virginia office.',
            website_url='http://www.oarric.org/',
            main_contact_name='Sara Conlon',
            main_contact_phone='(804) 643-2746',
            has_screening_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="Downtown Office",
                    address="1 North 3rd Street, Suite 200, Richmond, VA 23219",
                    latitude=37.541445,
                    longitude=-77.441671
                )
            ]
        )

        careavan = Service(
            name='Care-A-Van',
            description='The Bon Secours Care-A-Van is a free medical service that provides \
            primary care to uninsured adults and children the Greater Richmond community. \
            The Care-A-Van team is bilingual (Spanish/English) and composed of physicians, \
            nurse practitioners, registered nurses, patient care technicians, licensed \
            practical nurses, drivers, registrars, trained medical interpreters, registered \
            dieticians, licensed clinical social workers, and outreach workers.  Community \
            partners, including free clinics, local health agencies, and numerous faith-based \
            community organizations, collaborate with us.',
            website_url='http://richmond.bonsecours.com/about-us-mission-and-outreach-community-health-services-care-a-van.html',
            main_contact_name='Julie Bondy',
            main_contact_phone='(804) 545-1920',
            has_screening_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="St. Joseph's Outreach Clinic",
                    address="8000 Brook Road Richmond, VA 23227",
                    latitude=37.632279,
                    longitude=-77.459105
                )
            ]
        )

        bon_secours_ed = Service(
            name='Bon Secours Emergency Department',
            description='In 1824, the sisters of Bon Secours were founded in Paris. Bon \
            Secours means \'good help\' and it was in 1881 that the sisters expanded their \
            healing mission to the U.S., eventually establishing a non-profit Catholic \
            healthcare system. Our goal has always been to provide compassionate, quality \
            healthcare to those in need. This ambition is not only embraced by our doctors \
            and nurses, but by everyone. That\'s what we mean by Complete Health.',
            website_url='http://richmond.bonsecours.com/',
            main_contact_name='Kara Weiland',
            main_contact_phone='804-225-1704',
            has_screening_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="Richmond Community Hospital",
                    address="1500 N. 28th Street Richmond, VA 23223",
                    latitude=37.540270,
                    longitude=-77.406993
                )
            ]
        )

        rchbp = Service(
            name='Richmond Center for High Blood Pressure',
            description='We are a nurse-run, free clinic offering health care services to \
            the uninsured citizens of Greater Richmond. For more than 30 years, the Center \
            has been preventing Strokes, Heart Attacks and Kidney Failure by detecting and \
            helping to manage high blood pressure, diabetes, and high cholesterol among the \
            uninsured population of Greater Richmond. The Center serves as a model for \
            chronic disease management for adult patients.',
            website_url='http://www.rahbpc.org/',
            main_contact_name='Kim Lewis',
            main_contact_phone='804-359-9375',
            has_screening_yn='Y',
            fpl_cutoff=200,
            uninsured_only_yn='Y',
            medicaid_ineligible_only_yn='Y',
            residence_requirement_yn='N',
            time_in_area_requirement_yn='N',
            referral_emails=[
                ServiceReferralEmail(
                    email="richmond@codeforamerica.org"
                )
            ],
            locations=[
                ServiceLocation(
                    name="Main Office",
                    address="1200 West Cary Street Richmond, VA 23220",
                    latitude=37.544835,
                    longitude=-77.456712
                )
            ]
        )

        all_services = [
            daily_planet,
            crossover,
            access_now,
            resource_centers,
            oar,
            careavan,
            bon_secours_ed,
            rchbp
        ]

        db.session.add_all(all_services)

        # Set which services can refer to which
        for service in [s for s in all_services if s.name != 'Access Now']:
            service.accepts_referrals_from.extend(
                [s for s in all_services if s.name != service.name]
            )
        access_now.accepts_referrals_from.extend([
            daily_planet,
            crossover,
            careavan,
            rchbp
        ])

        db.session.commit()
        print 'Added service eligibility and sliding scale data'


if __name__ == '__main__':
    sys.exit(main())
