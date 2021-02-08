#!/usr/bin/python

try:
    from analyzemft import mftsession
except:
    from .analyzemft import mftsession


class AnalyzeMFT:
    def __init__(self, file_path):
        self.session = mftsession.MftSession(file_path)

    def process_file(self):
        self.session.process_mft_file()


if __name__ == "__main__":
    parser = AnalyzeMFT("$MFT")
    parser.process_file()
