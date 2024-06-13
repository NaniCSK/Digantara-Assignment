import numpy as np
from sgp4.api import Satrec, jday
import datetime
import os

def read_tle(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    sats = []
    for i in range(0, len(lines), 3):
        line1, line2 = lines[i+1], lines[i+2]
        sats.append(Satrec.twoline2rv(line1, line2))
    return sats

def get_positions(sats):
    results = []
    for sat in sats:
        for minute in range(1440):  # 1440 minutes in a day
            time = datetime.datetime(2024, 1, 1, 0, 0) + datetime.timedelta(minutes=minute)
            jd, fr = jday(time.year, time.month, time.day, time.hour, time.minute, time.second)
            e, r, v = sat.sgp4(jd, fr)
            if e == 0:  # 0 means no error
                results.append([time, *r, *v])
    return results

if __name__ == "__main__":
    file_path = os.path.join("data", "30sats.txt")
    sats = read_tle(file_path)
    positions = get_positions(sats)
    np.save("positions.npy", positions)  # Save positions to a file for the next steps
