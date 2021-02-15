from analyzemft.mftsession import MftSession

if __name__ == '__main__':
    parser = MftSession(mft_file_path="$MFT", allow_debug=False)
    # parser.build_filepaths()
    a = parser.process_mft_file()

    # for row in a:
    #     print(f"omerda row {row}")
