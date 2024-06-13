import numpy as np
import pandas as pd
import dask.dataframe as dd
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

def compute_lla(row):
    lon, lat, alt = ecef2lla(0, [row['px']], [row['py']], [row['pz']])
    return pd.Series([row['time'], lat, lon, alt], index=['time', 'lat', 'lon', 'alt'])

def is_within_region(row, region):
    return (region['min_lat'] <= row['lat'] <= region['max_lat'] and
            region['min_lon'] <= row['lon'] <= region['max_lon'])

if __name__ == "__main__":
    positions = np.load("positions.npy", allow_pickle=True)
    df = pd.DataFrame(positions, columns=['time', 'px', 'py', 'pz', 'vx', 'vy', 'vz'])
    ddf = dd.from_pandas(df, npartitions=10)

    # Specify the meta to avoid AttributeError
    meta = pd.DataFrame(columns=['time', 'lat', 'lon', 'alt'], dtype=object)
    
    # Convert ECEF to LLA
    lla_ddf = ddf.apply(compute_lla, axis=1, meta=meta)
    lla_ddf.to_csv("lla_positions.csv", single_file=True, index=False)

    # Define the region to filter
    region = {
        'min_lat': 16.66673,
        'max_lat': 69.74973,
        'min_lon': -120.64459,
        'max_lon': 103.58196
    }

    # Filter LLA data by region
    filtered_lla_ddf = lla_ddf[lla_ddf.apply(is_within_region, axis=1, region=region, meta=meta)]
    filtered_lla_ddf.to_csv("filtered_positions.csv", single_file=True, index=False)
