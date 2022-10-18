import argparse
from parser import get_page_parsed_data, save_to_file

parser = argparse.ArgumentParser()
parser.add_argument('--pages',
                    dest='pages_count',
                    type=int,
                    required=True,
                    help='Enter pages count')
parser.add_argument('--topic',
                    dest='topic',
                    type=str,
                    required=True,
                    help='Select the topic of interest')
args = parser.parse_args()

topic = args.topic
pages_count = args.pages_count
parse_result = {'topic': topic, 'pages': {}}

for page in range(0, pages_count):
    result = get_page_parsed_data(page, topic)
    parse_result['pages'][page + 1] = result

save_to_file(parse_result)