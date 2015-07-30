#!/usr/bin/env python
import sys

from flask import current_app
from app import create_app
from app.models import db, Service, SlidingScale, SlidingScaleFee

def main(app=create_app()):
  with app.app_context():
    db.metadata.create_all(db.engine)

    daily_planet = Service(
      name = 'Daily Planet',
      description = 'The Daily Planet is a Community Healthcare Center providing team-based \
      integrated healthcare. This includes: primary and behavioral health, as well as dental \
      and eye care.',
      website_url = 'http://www.dailyplanetva.org/',
      main_contact_name = 'Teresa Kimm',
      main_contact_phone = '(804) 783-2505',
      fpl_cutoff = None,
      uninsured_only_yn = 'N',
      medicaid_ineligible_only_yn = 'N',
      residence_requirement_yn = 'N',
      time_in_area_requirement_yn = 'N',
      sliding_scales = [
        SlidingScale(
          scale_name = 'Nominal',
          fpl_low = 0,
          fpl_high = 100,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'Dental services',
              price_percentage = 30
            ),
            SlidingScaleFee(
              name = 'Medical services',
              price_absolute = 10
            ),
            SlidingScaleFee(
              name = 'Mental health services, initial visit of calendar month',
              price_absolute = 10
            ),
            SlidingScaleFee(
              name = 'Mental health services, other visits',
              price_absolute = 5
            )
          ]
        ),
        SlidingScale(
          scale_name = 'Slide A',
          fpl_low = 100,
          fpl_high = 125,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'Dental services',
              price_percentage = 45
            ),
            SlidingScaleFee(
              name = 'Medical services',
              price_absolute = 15
            ),
            SlidingScaleFee(
              name = 'Mental health services, initial visit of calendar month',
              price_absolute = 15
            ),
            SlidingScaleFee(
              name = 'Mental health services, second visit of calendar month',
              price_absolute = 10
            ),
            SlidingScaleFee(
              name = 'Mental health services, other visits',
              price_absolute = 5
            )
          ]
        ),
        SlidingScale(
          scale_name = 'Slide B',
          fpl_low = 125,
          fpl_high = 150,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'Dental services',
              price_percentage = 55
            ),
            SlidingScaleFee(
              name = 'Medical services',
              price_absolute = 20
            ),
            SlidingScaleFee(
              name = 'Mental health services, initial visit of calendar month',
              price_absolute = 20
            ),
            SlidingScaleFee(
              name = 'Mental health services, second visit of calendar month',
              price_absolute = 15
            ),
            SlidingScaleFee(
              name = 'Mental health services, other visits',
              price_absolute = 5
            )
          ]
        ),
        SlidingScale(
          scale_name = 'Slide C',
          fpl_low = 150,
          fpl_high = 200,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'Dental services',
              price_percentage = 65
            ),
            SlidingScaleFee(
              name = 'Medical services',
              price_absolute = 30
            ),
            SlidingScaleFee(
              name = 'Mental health services, initial visit of calendar month',
              price_absolute = 30
            ),
            SlidingScaleFee(
              name = 'Mental health services, second visit of calendar month',
              price_absolute = 25
            ),
            SlidingScaleFee(
              name = 'Mental health services, other visits',
              price_absolute = 5
            )
          ]
        ),
        SlidingScale(
          scale_name = 'Full fee',
          fpl_low = 200,
          fpl_high = None
        )
      ]
    )

    crossover = Service(
      name = 'CrossOver',
      description = 'CrossOver Healthcare Ministry provides quality and compassionate \
      health care to the uninsured in the greater Richmond Metropolitan area.  Our mission \
      is to provide health care, promote wellness, and connect the talents and resources \
      of the community with people in need in the name of Jesus Christ. CrossOver is here \
      to serve and empower patients by providing a comprehensive approach to health care \
      for the body, mind, and spirit!',
      website_url = 'http://www.crossoverministry.org/',
      main_contact_name = 'Alex Chamberlain',
      main_contact_phone = '(804) 521-8263',
      fpl_cutoff = 200,
      uninsured_only_yn = 'Y',
      medicaid_ineligible_only_yn = 'N',
      residence_requirement_yn = 'N',
      time_in_area_requirement_yn = 'N',
      sliding_scales = [
        SlidingScale(
          scale_name = 'All',
          fpl_low = 0,
          fpl_high = None,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'Medications',
              price_absolute = 4
            ),
            SlidingScaleFee(
              name = 'Nurse/Labs',
              price_absolute = 10
            ),
            SlidingScaleFee(
              name = 'Vaccine clinic',
              price_absolute = 10
            ),
            SlidingScaleFee(
              name = 'Medical visit/mental health',
              price_absolute = 15
            ),
            SlidingScaleFee(
              name = 'Eye',
              price_absolute = 15
            ),
            SlidingScaleFee(
              name = 'Same day appointments',
              price_absolute = 20
            ),
            SlidingScaleFee(
              name = 'Dental',
              price_absolute = 20
            )
          ]
        )
      ]
    )

    access_now = Service(
      name = 'Access Now',
      description = 'The greater Richmond area has a vast network of safety-net health \
      clinics serving the primary care needs of the uninsured. These patients often also \
      need the care of a specialist to diagnose and treat their complex health issues. \
      When directors of local safety net clinics approached the Richmond Academy of \
      Medicine with requests to expand their network of specialists to meet this need, \
      the response was the development of Access Now. In January 2008, Access Now began \
      operations, providing access to specialists so that no patient would go without care \
      for lack of a willing provider. More than 900 specialists and physician extenders \
      open their doors to treat patients referred by Access Now.',
      website_url = 'http://www.ramdocs.org/?page=AccessNow',
      main_contact_name = 'Elizabeth Wong',
      main_contact_phone = '(804) 643-6631',
      fpl_cutoff = 200,
      uninsured_only_yn = 'Y',
      medicaid_ineligible_only_yn = 'Y',
      residence_requirement_yn = 'Y',
      time_in_area_requirement_yn = 'Y',
    )

    resource_centers = Service(
      name = 'RCHD Resource Centers',
      description = 'Resource Centers provide family planning and STI services, \
      health screenings, wellness services, nutrition education, community resource \
      information, budget management, and health education.',
      website_url = 'http://www.vdh.virginia.gov/LHD/richmondcity/clinic.htm',
      main_contact_name = 'Amy Popovich',
      main_contact_phone = '(804) 205-3733',
      fpl_cutoff = None,
      uninsured_only_yn = 'N',
      medicaid_ineligible_only_yn = 'N',
      residence_requirement_yn = 'N',
      time_in_area_requirement_yn = 'N',
      sliding_scales = [
        SlidingScale(
          scale_name = 'A',
          fpl_low = 0,
          fpl_high = 100,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 0
            )
          ]
        ),
        SlidingScale(
          scale_name = 'B',
          fpl_low = 100,
          fpl_high = 110,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 10
            )
          ]
        ),
        SlidingScale(
          scale_name = 'C',
          fpl_low = 110,
          fpl_high = 133,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 25
            )
          ]
        ),  
        SlidingScale(
          scale_name = 'D',
          fpl_low = 133,
          fpl_high = 167,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 50
            )
          ]
        ),  
        SlidingScale(
          scale_name = 'E',
          fpl_low = 167,
          fpl_high = 200,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 75
            )
          ]
        ),  
        SlidingScale(
          scale_name = 'F',
          fpl_low = 200,
          fpl_high = 250,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 95
            )
          ]
        ),  
        SlidingScale(
          scale_name = 'G',
          fpl_low = 250,
          fpl_high = None,
          sliding_scale_fees = [
            SlidingScaleFee(
              name = 'All services',
              price_percentage = 100
            )
          ]
        ),               
      ]
    )

    db.session.add_all([daily_planet, crossover, access_now, resource_centers])
    db.session.commit()
    print 'Added service eligibility and sliding scale data'


if __name__ == '__main__':
    sys.exit(main())