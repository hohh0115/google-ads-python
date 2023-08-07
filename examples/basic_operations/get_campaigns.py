#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example illustrates how to get all campaigns.

To add campaigns, run add_campaigns.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf.json_format import MessageToDict

from my_settings import CUSTOMER_NAME, CUSTOMER_ID, compose_file_path


def main(
    customer_id: str = CUSTOMER_ID
):
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    client = GoogleAdsClient.load_from_storage(version="v11", path='google-ads.yaml')
    ga_service = client.get_service("GoogleAdsService")

    query = '''
        SELECT
            campaign.status,
            campaign.ad_serving_optimization_status,
            campaign.advertising_channel_type,
            campaign.advertising_channel_sub_type,
            campaign.network_settings.target_content_network,
            campaign.network_settings.target_google_search,
            campaign.network_settings.target_partner_search_network,
            campaign.network_settings.target_search_network,
            campaign.experiment_type,
            campaign.serving_status,
            campaign.bidding_strategy_type,
            campaign.maximize_conversion_value.target_roas,
            campaign.shopping_setting.merchant_id,
            campaign.shopping_setting.sales_country,
            campaign.shopping_setting.enable_local,
            campaign.shopping_setting.campaign_priority,
            campaign.targeting_setting.target_restrictions,
            campaign.geo_target_type_setting.negative_geo_target_type,
            campaign.geo_target_type_setting.positive_geo_target_type,
            campaign.payment_mode,
            campaign.optimization_goal_setting.optimization_goal_types,
            campaign.base_campaign,
            campaign.name,
            campaign.id,
            campaign.campaign_budget,
            campaign.start_date,
            campaign.end_date,
            campaign.final_url_suffix,
            campaign.performance_max_upgrade.performance_max_campaign,
            campaign.performance_max_upgrade.pre_upgrade_campaign,
            campaign.performance_max_upgrade.status
        FROM campaign
        # WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
    '''

    # Issues a search request using streaming.
    stream = ga_service.search_stream(
        customer_id=customer_id,
        query=query
    )
    output_file_path = compose_file_path(file_name='Customer_{}_campaign_infos.txt'.format(CUSTOMER_NAME))
    with open(
        output_file_path,
        'w'
    ) as f:
        for batch in stream:
            for row in batch.results:
                campaign: dict = MessageToDict(
                    row.campaign._pb,
                    preserving_proto_field_name=True
                )
                f.write(
                    f'''Campaign with ID {campaign['id']} and name "{campaign['name']}":\n'''
                )
                for key, value in campaign.items():
                    f.write(f'''\t{key}: {value}\n''')
    print('Done: {}'.format(output_file_path))


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v14")

    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(args.customer_id)
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
