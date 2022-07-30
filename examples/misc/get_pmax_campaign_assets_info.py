
import argparse
from asyncio import constants
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v11.services.services.google_ads_service.client import GoogleAdsServiceClient
from google.protobuf.json_format import MessageToDict

from my_settings import CUSTOMER_NAME, CUSTOMER_ID, compose_file_path


def main(
    customer_id: str = CUSTOMER_ID
):
    client = GoogleAdsClient.load_from_storage(
        version="v11", path="google-ads.yaml"
    )
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    query = """
        SELECT
            asset_group_asset.status,
            asset_group_asset.resource_name,
            asset_group_asset.policy_summary.review_status,
            asset_group_asset.policy_summary.policy_topic_entries,
            asset_group_asset.policy_summary.approval_status,
            asset_group_asset.field_type,
            asset_group_asset.performance_label,
            asset_group_asset.asset_group,
            asset_group_asset.asset,
            asset_group.status,
            asset_group.resource_name,
            asset_group.path1,
            asset_group.path2,
            asset_group.name,
            asset_group.id,
            asset_group.final_urls,
            asset_group.final_mobile_urls,
            asset_group.campaign,
            asset.book_on_google_asset,
            asset.call_asset.ad_schedule_targets,
            asset.call_asset.call_conversion_action,
            asset.call_asset.call_conversion_reporting_state,
            asset.call_asset.country_code,
            asset.call_asset.phone_number,
            asset.call_to_action_asset.call_to_action,
            asset.callout_asset.ad_schedule_targets,
            asset.callout_asset.callout_text,
            asset.callout_asset.end_date,
            asset.callout_asset.start_date,
            asset.discovery_carousel_card_asset.call_to_action_text,
            asset.discovery_carousel_card_asset.headline,
            asset.discovery_carousel_card_asset.marketing_image_asset,
            asset.discovery_carousel_card_asset.portrait_marketing_image_asset,
            asset.discovery_carousel_card_asset.square_marketing_image_asset,
            asset.dynamic_custom_asset.android_app_link,
            asset.dynamic_custom_asset.contextual_keywords,
            asset.dynamic_custom_asset.formatted_price,
            asset.dynamic_custom_asset.formatted_sale_price,
            asset.dynamic_custom_asset.id,
            asset.dynamic_custom_asset.id2,
            asset.dynamic_custom_asset.image_url,
            asset.dynamic_custom_asset.ios_app_link,
            asset.dynamic_custom_asset.ios_app_store_id,
            asset.dynamic_custom_asset.item_address,
            asset.dynamic_custom_asset.item_category,
            asset.dynamic_custom_asset.item_description,
            asset.dynamic_custom_asset.item_subtitle,
            asset.dynamic_custom_asset.item_title,
            asset.dynamic_custom_asset.price,
            asset.dynamic_custom_asset.sale_price,
            asset.dynamic_custom_asset.similar_ids,
            asset.dynamic_education_asset.address,
            asset.dynamic_education_asset.android_app_link,
            asset.dynamic_education_asset.contextual_keywords,
            asset.dynamic_education_asset.image_url,
            asset.dynamic_education_asset.ios_app_link,
            asset.dynamic_education_asset.ios_app_store_id,
            asset.dynamic_education_asset.location_id,
            asset.dynamic_education_asset.program_description,
            asset.dynamic_education_asset.program_id,
            asset.dynamic_education_asset.program_name,
            asset.dynamic_education_asset.school_name,
            asset.dynamic_education_asset.similar_program_ids,
            asset.dynamic_education_asset.subject,
            asset.dynamic_education_asset.thumbnail_image_url,
            asset.dynamic_flights_asset.android_app_link,
            asset.dynamic_flights_asset.custom_mapping,
            asset.dynamic_flights_asset.destination_id,
            asset.dynamic_flights_asset.destination_name,
            asset.dynamic_flights_asset.flight_description,
            asset.dynamic_flights_asset.flight_price,
            asset.dynamic_flights_asset.flight_sale_price,
            asset.dynamic_flights_asset.formatted_price,
            asset.dynamic_flights_asset.formatted_sale_price,
            asset.dynamic_flights_asset.image_url,
            asset.dynamic_flights_asset.ios_app_link,
            asset.dynamic_flights_asset.ios_app_store_id,
            asset.dynamic_flights_asset.origin_id,
            asset.dynamic_flights_asset.origin_name,
            asset.dynamic_flights_asset.similar_destination_ids,
            asset.dynamic_hotels_and_rentals_asset.address,
            asset.dynamic_hotels_and_rentals_asset.android_app_link,
            asset.dynamic_hotels_and_rentals_asset.category,
            asset.dynamic_hotels_and_rentals_asset.contextual_keywords,
            asset.dynamic_hotels_and_rentals_asset.description,
            asset.dynamic_hotels_and_rentals_asset.destination_name,
            asset.dynamic_hotels_and_rentals_asset.formatted_price,
            asset.dynamic_hotels_and_rentals_asset.formatted_sale_price,
            asset.dynamic_hotels_and_rentals_asset.image_url,
            asset.dynamic_hotels_and_rentals_asset.ios_app_link,
            asset.dynamic_hotels_and_rentals_asset.ios_app_store_id,
            asset.dynamic_hotels_and_rentals_asset.price,
            asset.dynamic_hotels_and_rentals_asset.property_id,
            asset.dynamic_hotels_and_rentals_asset.property_name,
            asset.dynamic_hotels_and_rentals_asset.sale_price,
            asset.dynamic_hotels_and_rentals_asset.similar_property_ids,
            asset.dynamic_hotels_and_rentals_asset.star_rating,
            asset.dynamic_jobs_asset.address,
            asset.dynamic_jobs_asset.android_app_link,
            asset.dynamic_jobs_asset.contextual_keywords,
            asset.dynamic_jobs_asset.description,
            asset.dynamic_jobs_asset.image_url,
            asset.dynamic_jobs_asset.ios_app_link,
            asset.dynamic_jobs_asset.ios_app_store_id,
            asset.dynamic_jobs_asset.job_category,
            asset.dynamic_jobs_asset.job_id,
            asset.dynamic_jobs_asset.job_subtitle,
            asset.dynamic_jobs_asset.job_title,
            asset.dynamic_jobs_asset.location_id,
            asset.dynamic_jobs_asset.salary,
            asset.dynamic_jobs_asset.similar_job_ids,
            asset.dynamic_local_asset.address,
            asset.dynamic_local_asset.android_app_link,
            asset.dynamic_local_asset.category,
            asset.dynamic_local_asset.contextual_keywords,
            asset.dynamic_local_asset.deal_id,
            asset.dynamic_local_asset.deal_name,
            asset.dynamic_local_asset.description,
            asset.dynamic_local_asset.formatted_price,
            asset.dynamic_local_asset.formatted_sale_price,
            asset.dynamic_local_asset.image_url,
            asset.dynamic_local_asset.ios_app_link,
            asset.dynamic_local_asset.ios_app_store_id,
            asset.dynamic_local_asset.price,
            asset.dynamic_local_asset.sale_price,
            asset.dynamic_local_asset.similar_deal_ids,
            asset.dynamic_local_asset.subtitle,
            asset.dynamic_real_estate_asset.address,
            asset.dynamic_real_estate_asset.android_app_link,
            asset.dynamic_real_estate_asset.city_name,
            asset.dynamic_real_estate_asset.contextual_keywords,
            asset.dynamic_real_estate_asset.description,
            asset.dynamic_real_estate_asset.formatted_price,
            asset.dynamic_real_estate_asset.image_url,
            asset.dynamic_real_estate_asset.ios_app_link,
            asset.dynamic_real_estate_asset.ios_app_store_id,
            asset.dynamic_real_estate_asset.listing_id,
            asset.dynamic_real_estate_asset.listing_name,
            asset.dynamic_real_estate_asset.listing_type,
            asset.dynamic_real_estate_asset.price,
            asset.dynamic_real_estate_asset.property_type,
            asset.dynamic_real_estate_asset.similar_listing_ids,
            asset.dynamic_travel_asset.android_app_link,
            asset.dynamic_travel_asset.category,
            asset.dynamic_travel_asset.contextual_keywords,
            asset.dynamic_travel_asset.destination_address,
            asset.dynamic_travel_asset.destination_id,
            asset.dynamic_travel_asset.destination_name,
            asset.dynamic_travel_asset.formatted_price,
            asset.dynamic_travel_asset.formatted_sale_price,
            asset.dynamic_travel_asset.image_url,
            asset.dynamic_travel_asset.ios_app_link,
            asset.dynamic_travel_asset.ios_app_store_id,
            asset.dynamic_travel_asset.origin_id,
            asset.dynamic_travel_asset.origin_name,
            asset.dynamic_travel_asset.price,
            asset.dynamic_travel_asset.sale_price,
            asset.dynamic_travel_asset.similar_destination_ids,
            asset.dynamic_travel_asset.title,
            asset.final_mobile_urls,
            asset.final_url_suffix,
            asset.final_urls,
            asset.hotel_callout_asset.language_code,
            asset.hotel_callout_asset.text,
            asset.id,
            asset.image_asset.file_size,
            asset.image_asset.full_size.height_pixels,
            asset.image_asset.full_size.url,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.mime_type,
            asset.lead_form_asset.background_image_asset,
            asset.lead_form_asset.business_name,
            asset.lead_form_asset.call_to_action_description,
            asset.lead_form_asset.call_to_action_type,
            asset.lead_form_asset.custom_disclosure,
            asset.lead_form_asset.custom_question_fields,
            asset.lead_form_asset.delivery_methods,
            asset.lead_form_asset.description,
            asset.lead_form_asset.desired_intent,
            asset.lead_form_asset.fields,
            asset.lead_form_asset.headline,
            asset.lead_form_asset.post_submit_call_to_action_type,
            asset.lead_form_asset.post_submit_description,
            asset.lead_form_asset.post_submit_headline,
            asset.lead_form_asset.privacy_policy_url,
            asset.mobile_app_asset.app_id,
            asset.mobile_app_asset.app_store,
            asset.mobile_app_asset.end_date,
            asset.mobile_app_asset.link_text,
            asset.mobile_app_asset.start_date,
            asset.name,
            asset.page_feed_asset.labels,
            asset.page_feed_asset.page_url,
            asset.policy_summary.approval_status,
            asset.policy_summary.policy_topic_entries,
            asset.policy_summary.review_status,
            asset.price_asset.language_code,
            asset.price_asset.price_offerings,
            asset.price_asset.price_qualifier,
            asset.price_asset.type,
            asset.promotion_asset.ad_schedule_targets,
            asset.promotion_asset.discount_modifier,
            asset.promotion_asset.end_date,
            asset.promotion_asset.language_code,
            asset.promotion_asset.money_amount_off.amount_micros,
            asset.promotion_asset.money_amount_off.currency_code,
            asset.promotion_asset.occasion,
            asset.promotion_asset.orders_over_amount.amount_micros,
            asset.promotion_asset.orders_over_amount.currency_code,
            asset.promotion_asset.percent_off,
            asset.promotion_asset.promotion_code,
            asset.promotion_asset.promotion_target,
            asset.promotion_asset.redemption_end_date,
            asset.promotion_asset.redemption_start_date,
            asset.promotion_asset.start_date,
            asset.resource_name,
            asset.sitelink_asset.ad_schedule_targets,
            asset.sitelink_asset.description1,
            asset.sitelink_asset.description2,
            asset.sitelink_asset.end_date,
            asset.sitelink_asset.link_text,
            asset.sitelink_asset.start_date,
            asset.source,
            asset.structured_snippet_asset.header,
            asset.structured_snippet_asset.values,
            asset.text_asset.text,
            asset.tracking_url_template,
            asset.type,
            asset.url_custom_parameters,
            asset.youtube_video_asset.youtube_video_id,
            asset.youtube_video_asset.youtube_video_title,
            customer.id,
            customer.descriptive_name,
            customer.resource_name,
            campaign.status,
            campaign.resource_name,
            campaign.name,
            campaign.id
        FROM asset_group_asset
        # WHERE
            # campaign.id = {campaign_id}
        ORDER BY campaign.name ASC
    """
    results = getattr(
        ga_service.search(
            customer_id=customer_id,
            query=query
        ),
        'results'
    )

    contents = []
    campaigns = set()
    for row in results:
        campaign = f'''ID: {row.campaign.id}, Name: {row.campaign.name}'''
        campaigns.add(campaign)
        contents.append(campaign + '\n\n')

        asset_group = MessageToDict(
            row.asset_group._pb,
            preserving_proto_field_name=True
        )
        asset = MessageToDict(
            row.asset._pb,
            preserving_proto_field_name=True
        )
        asset_group_asset = MessageToDict(
            row.asset_group_asset._pb,
            preserving_proto_field_name=True
        )
        contents.append(f'''AssetGroup:\n''')
        for key, value in asset_group.items():
            contents.append(f'''\t{key}: {value}\n''')
        contents.append(f'''Asset:\n''')
        for key, value in asset.items():
            contents.append(f'''\t{key}: {value}\n''')
        contents.append(f'''AssetGroupAsset:\n''')
        for key, value in asset_group_asset.items():
            contents.append(f'''\t{key}: {value}\n''')
        contents.append(f'''\n# ==================================================== #\n\n''')

    customer = results[0].customer
    contents.insert(0, f'''# ==================================================== #\n\n''')
    # f-string expression part cannot include a backslash...
    contents.insert(0, 'All campaigns:\n\t{}\n\n'.format(',\n\t'.join(list(campaigns))))
    contents.insert(0, f'''Customer:\n\t{customer.id}, {customer.descriptive_name}.\n''')

    output_file_path = compose_file_path(file_name='Customer_{}_PMax_asset_infos.txt'.format(CUSTOMER_NAME))
    with open(output_file_path, 'w') as f:
        f.write(''.join(contents))
    print('Done: {}'.format(output_file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List all image assets for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=False,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-p",
        "--pmax_campaign_id",
        type=str,
        required=False,
        help="The Google Ads PMax campaign ID.",
    )
    args = parser.parse_args()

    try:
        main(args.customer_id, args.pmax_campaign_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
