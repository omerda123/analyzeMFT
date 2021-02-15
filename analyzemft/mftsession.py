#!/usr/bin/env python
# Author: David Kovar [dkovar <at> gmail [dot] com]
# Name: mftsession.py
#
# Copyright (c) 2010 David Kovar. All rights reserved.
# This software is distributed under the Common Public License 1.0
#
# Date: May 2013
#
VERSION = "v2.0.18"
import csv
import json
import os
import sys
from optparse import OptionParser
import mft

SIAttributeSizeXP = 72
SIAttributeSizeNT = 48


class MftSession:
    """Class to describe an entire MFT processing session"""

    def __init__(self, mft_file_path: str, allow_debug: bool, path_sep: str = '/'):
        self.mft_file_path = mft_file_path
        self.path_sep = path_sep
        self.debug = allow_debug
        self.num_records = 0
        self.mft = {}
        self.fullmft = {}
        self.folders = {}
        self.mftsize = self.get_mft_file_size()
        self.options = None
        self.mft_file = self.open_mft_file()

    def get_mft_file_size(self):
        return int(os.path.getsize(self.mft_file_path)) / 1024

    def open_mft_file(self):
        try:
            return open(self.mft_file_path, 'rb')
        except Exception:
            print(f"Unable to open file: {self.options.bodyfile}")
            sys.exit()

    @staticmethod
    def fmt_excel(date_str):
        return f'="{date_str}"'

    @staticmethod
    def fmt_norm(date_str):
        return date_str

    def process_mft_file(self):
        self.build_filepaths()
        # reset the file reading
        self.num_records = 0
        self.mft_file.seek(0)
        raw_record = self.mft_file.read(1024)
        while raw_record != "":
            record = mft.parse_record(raw_record=raw_record, debug=self.debug)
            record['filename'] = self.mft[self.num_records]['filename']
            if record['ads'] > 0:
                for i in range(0, record['ads']):
                    #                         print "ADS: %s" % (record['data_name', i])
                    record_ads = record.copy()
                    record_ads['filename'] = record['filename'] + ':' + record['data_name', i]
            self.num_records += 1
            raw_record = self.mft_file.read(1024)
            yield record

    def build_filepaths(self):
        # reset the file reading
        self.mft_file.seek(0)
        self.num_records = 0
        # 1024 is valid for current version of Windows but should really get this value from somewhere
        raw_record = self.mft_file.read(1024)
        while raw_record:
            minirec = {}
            record = mft.parse_record(raw_record, debug=self.debug)
            minirec['filename'] = record['filename']
            minirec['fncnt'] = record['fncnt']
            if record['fncnt'] == 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                minirec['name'] = record['fn', 0]['name']
            if record['fncnt'] > 1:
                minirec['par_ref'] = record['fn', 0]['par_ref']
                for i in (0, record['fncnt'] - 1):
                    # print record['fn',i]
                    if record['fn', i]['nspace'] == 0x1 or record['fn', i]['nspace'] == 0x3:
                        minirec['name'] = record['fn', i]['name']
                if minirec.get('name') is None:
                    minirec['name'] = record['fn', record['fncnt'] - 1]['name']
            self.mft[self.num_records] = minirec
            self.num_records += 1
            raw_record = self.mft_file.read(1024)
        self.gen_filepaths()

    def get_folder_path(self, seqnum):
        if self.debug:
            print(f"Building Folder For Record Number ({seqnum})")
        if seqnum not in self.mft:
            return 'Orphan'
        # If we've already figured out the path name, just return it
        if (self.mft[seqnum]['filename']) != '':
            return self.mft[seqnum]['filename']
        try:
            # if (self.mft[seqnum]['fn',0]['par_ref'] == 0) or
            # (self.mft[seqnum]['fn',0]['par_ref'] == 5):  # There should be no seq
            # number 0, not sure why I had that check in place.
            if self.mft[seqnum]['par_ref'] == 5:  # Seq number 5 is "/", root of the directory
                self.mft[seqnum]['filename'] = self.path_sep + self.mft[seqnum]['name']
                return self.mft[seqnum]['filename']
        except:  # If there was an error getting the parent's sequence number, then there is no FN record
            self.mft[seqnum]['filename'] = 'NoFNRecord'
            return self.mft[seqnum]['filename']
        # Self referential parent sequence number. The filename becomes a NoFNRecord note
        if (self.mft[seqnum]['par_ref']) == seqnum:
            if self.debug:
                print(f"Error, self-referential, while trying to determine path for seqnum {seqnum}")
            self.mft[seqnum]['filename'] = 'ORPHAN' + self.path_sep + self.mft[seqnum]['name']
            return self.mft[seqnum]['filename']
        # We're not at the top of the tree and we've not hit an error
        parentpath = self.get_folder_path((self.mft[seqnum]['par_ref']))
        self.mft[seqnum]['filename'] = parentpath + self.path_sep + self.mft[seqnum]['name']
        return self.mft[seqnum]['filename']

    def gen_filepaths(self):
        for i in self.mft:
            #            if filename starts with / or ORPHAN, we're done.
            #            else get filename of parent, add it to ours, and we're done.
            # If we've not already calculated the full path ....
            if (self.mft[i]['filename']) == '':
                if self.mft[i]['fncnt'] > 0:
                    self.get_folder_path(i)
                    # self.mft[i]['filename'] = self.mft[i]['filename'] + '/' +
                    #   self.mft[i]['fn',self.mft[i]['fncnt']-1]['name']
                    # self.mft[i]['filename'] = self.mft[i]['filename'].replace('//','/')
                    if self.debug:
                        print(f"Filename (with path): {self.mft[i]['filename']}")
                else:
                    self.mft[i]['filename'] = 'NoFNRecord'
