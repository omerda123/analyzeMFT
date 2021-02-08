from analyzeMFT import AnalyzeMFT

parser = AnalyzeMFT(mft_file_path="$MFT", debug=True)
res = parser.process_file()
