
import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v11.services.services.google_ads_service.client import GoogleAdsServiceClient
from google.protobuf.json_format import MessageToDict

from my_settings import CUSTOMER_NAME, CUSTOMER_ID, _DEFAULT_PAGE_SIZE, compose_file_path


def main(customer_id: str = CUSTOMER_ID, page_size: int = _DEFAULT_PAGE_SIZE):
    client = GoogleAdsClient.load_from_storage(
        version="v11", path="google-ads.yaml"
    )
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")

    query = """
        SELECT
            audience.status,
            audience.resource_name,
            audience.name,
            audience.id,
            audience.exclusion_dimension,
            audience.dimensions,
            audience.description
        FROM audience
    """
    results = getattr(
        ga_service.search(
            customer_id=customer_id,
            query=query
        ),
        'results'
    )

    output_file_path = compose_file_path(file_name='Customer_{}_Audience_infos.txt'.format(CUSTOMER_NAME))
    with open(
        output_file_path,
        'w'
    ) as f:
        for row in results:
            audience = MessageToDict(
                row.audience._pb,
                preserving_proto_field_name=True
            )
            dimension_names = sum(
                [list(i.keys()) for i in audience["dimensions"]],
                []
            )
            f.write(f'''Audience\n\tID: {audience['id']}, Name: {audience['name']}, types of Dimensions: {', '.join(dimension_names)}\n''')
            for dimension in audience["dimensions"]:
                for dimension_name, dimension_contents in dimension.items():
                    f.write(f'\t\tDimension: {dimension_name}\n')
                    for _, content in dimension_contents.items():
                        for i in content:
                            if isinstance(i, dict):
                                for key, value in i.items():
                                    f.write(f'''\t\t\t{key}: {value}\n''')
                            elif isinstance(i, str):
                                f.write(f'''\t\t\t{i}\n''')
                            else:
                                print('Something NOT PROCESS')
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
