import numpy as np
import pyproj

def ecef2lla(i, pos_x, pos_y, pos_z):
    # Define the coordinate transformation
    transformer = pyproj.Transformer.from_proj(
        pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84'),
        pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84'),
        always_xy=True
    )
    lona, lata, alta = transformer.transform(pos_x[i], pos_y[i], pos_z[i])
    return lona, lata, alta

def convert_to_lla(positions):
    lla_positions = []
    for pos in positions:
        time, px, py, pz, vx, vy, vz = pos
        lon, lat, alt = ecef2lla(0, [px], [py], [pz])
        lla_positions.append([time, lat, lon, alt])
    return lla_positions

if __name__ == "__main__":
    # Ensure that 'positions.npy' file is in the current directory
    positions = np.load("positions.npy", allow_pickle=True)
    lla_positions = convert_to_lla(positions)
    np.save("lla_positions.npy", lla_positions)
