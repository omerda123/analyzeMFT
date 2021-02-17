from analyzemft.mftsession import MftSession

if __name__ == '__main__':
    session = MftSession(mft_file_path="/Users/odaniel/Downloads/$MFT", allow_debug=False)
    session.open_mft_file()
    a = session.process_mft_file()

    for row in a:
        print(f"omerda row {row}")
