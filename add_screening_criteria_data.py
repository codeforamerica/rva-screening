#!/usr/bin/env python
import sys

from flask import current_app
from app import app
from app.models import db, Service, SlidingScale, SlidingScaleFee

def main():
    with app.app_context():
        db.metadata.create_all(db.engine)

        daily_planet = Service(
            name = 'Daily Planet',
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
                            price_absolute = 55
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
            fpl_cutoff = 200,
            uninsured_only_yn = 'Y',
            medicaid_ineligible_only_yn = 'Y',
            residence_requirement_yn = 'Y',
            time_in_area_requirement_yn = 'Y',
        )

        resource_centers = Service(
            name = 'RCHD Resource Centers',
            fpl_cutoff = None,
            uninsured_only_yn = 'N',
            medicaid_ineligible_only_yn = 'N',
            residence_requirement_yn = 'N',
            time_in_area_requirement_yn = 'N',
            sliding_scales = [
                SlidingScale(
                    scale_name = 'A',
                    fpl_low = 0,
                    fpl_high = 80,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 0
                        )
                    ]
                ),
                SlidingScale(
                    scale_name = 'B',
                    fpl_low = 80,
                    fpl_high = 88,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 10
                        )
                    ]
                ),
                SlidingScale(
                    scale_name = 'C',
                    fpl_low = 88,
                    fpl_high = 106.6,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 25
                        )
                    ]
                ),  
                SlidingScale(
                    scale_name = 'D',
                    fpl_low = 106.6,
                    fpl_high = 133.2,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 50
                        )
                    ]
                ),  
                SlidingScale(
                    scale_name = 'E',
                    fpl_low = 133.2,
                    fpl_high = 160,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 75
                        )
                    ]
                ),  
                SlidingScale(
                    scale_name = 'F',
                    fpl_low = 160,
                    fpl_high = 200,
                    sliding_scale_fees = [
                        SlidingScaleFee(
                            name = 'All services',
                            price_percentage = 95
                        )
                    ]
                ),  
                SlidingScale(
                    scale_name = 'G',
                    fpl_low = 200,
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
        print 'Service eligibility and sliding scale data added.'


if __name__ == '__main__':
    sys.exit(main())