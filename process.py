import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import binascii
import json



data = pd.read_csv('hygdata_v3.csv')
print(f'all stars:  + {data.shape}')
data_ci = data[~data['ci'].isnull()] 
print(f'ci stars:  + {data_ci.shape}')
data_hip = data_ci[~data_ci['hip'].isnull()] 
data_hip.hip = data_hip.hip.apply(int).astype(str)
data_spect = data_hip[~data_hip['spect'].isnull()] 


data_spect['spectral_type'] = data_spect['spect'].str[:1]
data_spect.spectral_type.value_counts()




data_sorted = data_spect.sort_values(by=['dist'])[:1000]
print(f'hip 10k stars:  + {data_spect.shape}')


data_sorted['dist'].plot()

index_column = []
for index in range(0,1000):
	index_column.append(index)
data_sorted['token_id'] = index_column


sun_temperature = 5800
sun_abs_magnitude = 4.85

data_sorted['temperature'] = 5601/((data_sorted['ci'] + 0.4)**(2/3))
data_sorted['radius'] = (sun_temperature/data_sorted['temperature'])**2 * (2.51**(sun_abs_magnitude-data_sorted['absmag']))**(0.5)

data_sorted['name'] =  np.where(data_sorted['proper'].isnull(), 'HIP' + data_sorted['hip'], 'HIP' + data_sorted['hip'] + ' - ' + data_sorted['proper'])
data_sorted['con_text'] =  np.where(data_sorted['con'].isnull(), data_sorted['name'], data_sorted['name'] + " belongs to the " + data_sorted['con'] + " constellation.")
data_sorted['description'] =  data_sorted['con_text'] + " For more information, visit https://explorer.openstars.org/#view/hip-" + data_sorted['hip']
data_sorted['image'] =  "https://raw.githubusercontent.com/openstars-org/stars-database/main/images/hip" + data_sorted['hip'] + ".png"
data_sorted['external_url'] = "https://explorer.openstars.org/#view/hip-" + data_sorted['hip']

data_sorted = data_sorted.drop('con_text', 1)

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def round_to_05(n):
    return round_to(n, 0.005)



data_sorted['premium'] = np.where(data_sorted['proper'].isnull(), 0, 0.05)
max_absmag = 20
max_dist = 100
absmag_multiplier = 10
dist_multiplier = 2
data_sorted['price'] = ( absmag_multiplier * (max_absmag - data_sorted['absmag']) + dist_multiplier * (max_dist - data_sorted['dist']))
data_sorted['price']= data_sorted['price']/3000
data_sorted['price']= data_sorted['price'] + data_sorted['premium']
data_sorted['price'] = data_sorted['price'].apply(round_to_05)


# attributes_column = []
# for i in data_sorted.index:
# 	attri = {'trait_type': ['Apparent Magnitude'],
# 	'value': [data_sorted.loc[i]['absmag']]
# 	}
# 	attributes_df = pd.DataFrame(attri, columns = ['trait_type', 'value'])
# 	attributes_df_json = attributes_df.to_json(orient='records')
# 	attributes_column.append(attributes_df_json)
# data_sorted['attributes'] = attributes_column


# Special parameters for the sun
data_sorted['description'][0] = "Our main star. For more information, visit https://explorer.openstars.org/#view/hip-0"
data_sorted['price'][0] = 50


# restore hip data type
data_sorted.hip = data_hip.hip.astype(int)

# Create the big json
data_sorted.to_json(f'1k_stars_sorted_by_dist.json', orient='records', indent=2 )
data_sorted.to_csv(f'1k_stars_sorted_by_dist.csv')


# Cleanup data
try:
	os.system("rm -rf jsons")
except:
	print('jsons folder doesnt exist')

os.mkdir('jsons')

data_sorted = data_sorted.drop('price', 1)
data_sorted = data_sorted.drop('premium', 1)

# Create each start json
for index, i in enumerate(data_sorted.index):
	data_sorted.loc[i].to_json(f'jsons/{index}.json', indent=2 )



for index, i in enumerate(data_sorted.token_id):
  data = {}
  with open(f'jsons/{index}.json') as f:
    #print(f'jsons/{index}.json')
    data = json.load(f)
    data["attributes"] = [
      {
        "trait_type": "Absolute Magnitude",
        "value": data["absmag"]
      },
      {
        "trait_type": "Constellation",
        "value": data["con"]
      },
      {
        "trait_type": "Distance to the Sun",
        "value": data["dist"]
      },
    ]

  with open(f'jsons/{index}.json', "w") as f:
    json.dump(data, f)


