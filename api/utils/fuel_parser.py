import csv
import os

def load_data():
    fuel_stations = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, 'fuel_data.csv')
    
    with open(csv_path , 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        
        for row in reader:
            try:
                city = row['City'].strip()
                state = row['State'].strip()
                name = row['Truckstop Name'].strip()
                price = float(row['Retail Price'].strip())
                
                key = f"{city}_{state}"
                
                if key not in fuel_stations:
                    fuel_stations[key] ={
                        'name' : name,
                        'city' : city,
                        'state' : state,
                        'price' : price
                    }
                else:
                    if price < fuel_stations[key]['price']:
                        fuel_stations[key]['price'] = price
            except(ValueError, KeyboardInterrupt):
                continue
    return list(fuel_stations.values())