from datetime import datetime
from elasticsearch import Elasticsearch
from collections import OrderedDict
import os
import logging
import json
import argparse

class KibanaAnalyzer():
    def __init__(self, args):
        self.es = Elasticsearch(args.host)
        abs_path = os.path.dirname(os.path.abspath(__file__))
        server_f_path =  abs_path + "/../kibana_lookup.json"
        self.data_dict = self.dump_config(server_f_path)
        #print("%s", self.es.info())

    def dump_config(self, filename):
        with open(filename) as json_data_file:
            data = json.load(json_data_file, object_pairs_hook=OrderedDict)
            return data

    def parse_log(self):
        val = self.es.search(body=self.data_dict)

        length = len(val['hits']['hits'])
        # print("*******************************************************")
        # print(val['hits']['hits'][0]['_source']['message'])
        # print("*******************************************************")
        for index in range(length):
            print("*******************************************************")
            print(val['hits']['hits'][0]['_source']['host'])
            print("*******************************************************")
            print(val['hits']['hits'][index]['_source']['message'])

if __name__ == '__main__':
    # get trace logger and set level
    tracer = logging.getLogger('kibana.trace')
    tracer.setLevel(logging.INFO)
    tracer.addHandler(logging.FileHandler('/tmp/kibana_trace.log'))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host",
        action="store",
        default="http://elastic1a.corp.ooma.com:9200",
        help="The elasticsearch host you wish to connect too. (Default: localhost:9200)")
    parser.add_argument(
        "-p", "--path",
        action="store",
        default=None,
        help="Path to Kibana Search Engine. Commits used as data to load into Elasticsearch. (Default: None")

    args = parser.parse_args()
    obj = KibanaAnalyzer(args)

    obj.parse_log()