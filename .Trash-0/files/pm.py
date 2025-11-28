import os

import pm4py  # version 2.7.4
from pprint import pprint  # pretty printing
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation import algorithm as evaluation
from pm4py.objects.conversion.log import converter as stream_converter
from pm4py.objects.log.importer.xes import importer as xes_import
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay


def main():
    # join current file path and log file path
    # returns path to event log file
    # event log file needs to be in the same directory as python file
    file_path = os.path.join(os.path.dirname(__file__), "edited_hh104_labour.xes")

    # 1. read event log
    log = xes_import.apply(file_path)
    log_df = pm4py.convert.convert_to_dataframe(log) #convert log to type DataFrame
    log = pm4py.convert_to_event_log(log)  # convert log to type EventLog

    # 2. print trace structure and event structure
    print("\n2.\n")
    print("TRACE KEYS:")
    print(list(log[0].attributes.keys()))
    print("EVENT KEYS:")
    print(list(log[0][0].keys()))

    # 3. print number of traces
    print("\n3.\n")
    print("Number of traces:", len(log))

    # 4. print number of events
    print("\n4.\n")
    event_stream = stream_converter.apply(
        log, variant=stream_converter.Variants.TO_EVENT_STREAM
    )
    print("Number of events:", len(event_stream))

    # 5. print all the events
    print("\n5.\n")
    events = log_df.drop_duplicates(subset='concept:name')
    print(events['concept:name'].tolist())

    # 6. print start and end activities of traces, with frequency for each
    print("\n6.\n")
    print("Start activities: ", pm4py.get_start_activities(log))
    print("End activities: ", pm4py.get_end_activities(log))

    # 7. print array
    print("\n7.\n")

    print(log_df[['case:concept:name', 'concept:name', 'lifecycle:transition', 'time:timestamp']])

    # or
    '''for trace in log:
        for event in trace:
            print(
                trace.attributes["concept:name"],
                "\t",
                event["concept:name"],
                "\t",
                event["lifecycle:transition"],
                "\t",
                event["time:timestamp"],
            )'''


