from analyzemft.mftsession import MftSession

parser = MftSession(mft_file_path="$MFT", debug=True)
parser.build_filepaths()
parser.process_mft_file()
