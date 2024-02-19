import base64
import os


def decode_csv_64(string, output_filename=None):
    data = eval(string)
    print(type(data), data)
    csv = eval(data["message"]["csv_file"])
    if output_filename:
        with open(f"{output_filename}.csv", "wb") as b:
            d = base64.b64decode(csv)
            b.write(d)
            b.close()
        return
    return csv
