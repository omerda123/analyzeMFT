#!/usr/bin/python

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession


class AnalyzeMFT:
    def __init__(self, mft_file_path, debug: bool = False):
        self.session = mftsession.MftSession(mft_file_path=mft_file_path, debug=debug)

    def process_file(self):
        self.session.process_mft_file()


if __name__ == "__main__":
    parser = AnalyzeMFT("$MFT")
    parser.process_file()
