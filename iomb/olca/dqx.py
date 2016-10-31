"""
This module contains methods for writing data quality information to an JSON-LD
package.
"""

import json

import iomb.data as data
import iomb.refmap as ref


def append_data_quality(process: dict, sector: ref.Sector):
    process['dqSystem'] = {
        '@type': 'DQSystem',
        '@id': '70bf370f-9912-4ec1-baa3-fbd4eaf85a10'}
    process['exchangeDqSystem'] = {
        '@type': 'DQSystem',
        '@id': 'd13b2bc4-5e84-4cc8-a6be-9101ebb252ff'}
    if sector.data_quality_entry is not None:
        process['dqEntry'] = sector.data_quality_entry


def dq_process_system():
    path = data.data_dir + '/dq_system_processes.json'
    with open(path, 'r', encoding='utf-8', newline='\n') as f:
        obj = json.load(f)
        return obj


def dq_exchanges_system():
    path = data.data_dir + '/dq_system_exchanges.json'
    with open(path, 'r', encoding='utf-8', newline='\n') as f:
        obj = json.load(f)
        return obj
