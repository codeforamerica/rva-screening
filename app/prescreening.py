from app.models import Service


def calculate_fpl(household_size, annual_income):
    """Calculate income as a percentage of the Federal Poverty Level."""
    fpl = 4160 * int(household_size) + 7610
    return float(annual_income) / fpl * 100


def calculate_pre_screen_results(
    fpl,
    has_health_insurance,
    is_eligible_for_medicaid,
    service_ids
):
    """Calculate a patient's potential service eligibility."""
    service_results = []
    for service_id in service_ids:
        service = Service.query.get(service_id)

        if (service.fpl_cutoff and fpl > service.fpl_cutoff):
            eligible = False
            fpl_eligible = False
        elif (
            (service.uninsured_only_yn == 'Y'
                and has_health_insurance == 'yes')
            or (
                service.medicaid_ineligible_only_yn == 'Y'
                and is_eligible_for_medicaid == 'yes'
            )
        ):
            eligible = False
            fpl_eligible = True
        else:
            eligible = True
            fpl_eligible = True

        sliding_scale_name = None
        sliding_scale_range = None
        sliding_scale_fees = None
        for sliding_scale in service.sliding_scales:
            if (
                (sliding_scale.fpl_low <= fpl < sliding_scale.fpl_high)
                or (
                    sliding_scale.fpl_low <= fpl
                    and sliding_scale.fpl_high is None
                )
            ):
                sliding_scale_name = sliding_scale.scale_name
                sliding_scale_fees = sliding_scale.sliding_scale_fees
                if sliding_scale.fpl_high:
                    sliding_scale_range = 'between %d%% and %d%%' % (
                        sliding_scale.fpl_low,
                        sliding_scale.fpl_high
                    )
                else:
                    sliding_scale_range = 'over %d%%' % sliding_scale.fpl_low

        service_results.append({
            'name': service.name,
            'eligible': eligible,
            'fpl_cutoff': service.fpl_cutoff,
            'fpl_eligible': fpl_eligible,
            'uninsured_only_yn': service.uninsured_only_yn,
            'medicaid_ineligible_only_yn': service.medicaid_ineligible_only_yn,
            'residence_requirement_yn': service.residence_requirement_yn,
            'time_in_area_requirement_yn': service.time_in_area_requirement_yn,
            'sliding_scale': sliding_scale_name,
            'sliding_scale_range': sliding_scale_range,
            'sliding_scale_fees': sliding_scale_fees,
            'id': service.id
        })

    return service_results
