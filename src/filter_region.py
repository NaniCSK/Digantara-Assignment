import numpy as np

def filter_by_region(lla_positions, region):
    filtered_positions = []
    for pos in lla_positions:
        time, lat, lon, alt = pos
        if (region['min_lat'] <= lat <= region['max_lat'] and
            region['min_lon'] <= lon <= region['max_lon']):
            filtered_positions.append(pos)
    return filtered_positions

if __name__ == "__main__":
    lla_positions = np.load("lla_positions.npy", allow_pickle=True)
    
    # Example region
    region = {
        'min_lat': 16.66673, 'max_lat': 69.74973,
        'min_lon': -120.64459, 'max_lon': 103.58196
    }
    
    filtered_positions = filter_by_region(lla_positions, region)
    np.save("filtered_positions.npy", filtered_positions)
