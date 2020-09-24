import pandas as pd 
import json
from os import path
from math import isnan
from dateutil import parser

stateName = {
	'AL': 'Alabama', 'AK': "Alaska", 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
	'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
	'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
	'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
	'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 
	'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming', 'AS': 'American Samoa', 'DC': 'District of Columbia',
	'FM': 'Federated States of Micronesia', 'GU': 'Guam', 'MH': 'Marshall Islands', 'MP': 'Northern Mariana Islands', 'PW': 'Palau', 'PR': 'Puerto Rico', 'VI': 'Virgin Islands'
}

def getStateName(name):
	return stateName[name]

def readCSV(location='', filename=''):
	csv_filepath = path.join(location, filename)
	return pd.read_csv(csv_filepath)


def readJSON(location='', filename=''):
	json_filepath = path.join(location, filename)
	with open(json_filepath, 'r') as jsonFile:
		data = json.load(jsonFile)
	return data 


def writeJSON(data, location='', filename=''):
	json_filepath = path.join(location, filename)
	with open(json_filepath, 'w') as jsonData:
		json.dump(data, jsonData, indent=2)


def stateCounts(data):
	stateCount = dict()
	for i in range(data.shape[0]):
		code = data['state'][i].upper()
		stateName = getStateName(code)
		gender = data['gender'][i]
		ageGroup = str(data['ageGroup'][i])
		
		city = data['city'][i].strip()

		if stateName in stateCount :
			stateCount[stateName]['count'] += 1
		else :
			stateCount[stateName] = {
				'code': code,
				'count': 1,
				'genderMale': 0,
				'genderFemale': 0,
				'genderUnknown': 0,
				'ageGroup1': 0,
				'ageGroup2': 0,
				'ageGroup3': 0,
				'ageGroupUnknown': 0,
				'cities': {},
			}

		if type(gender) != type(1.0):
			if gender.lower() == 'm':
				stateCount[stateName]['genderMale'] += 1
			elif gender.lower() == 'f':
				stateCount[stateName]['genderFemale'] += 1
			else:
				stateCount[stateName]['genderUnknown'] += 1
		else:
			stateCount[stateName]['genderUnknown'] += 1

		if ageGroup == '1.0':
			stateCount[stateName]['ageGroup1'] += 1
		elif ageGroup == '2.0':
			stateCount[stateName]['ageGroup2'] += 1
		elif ageGroup == '3.0':
			stateCount[stateName]['ageGroup3'] += 1
		else:
			stateCount[stateName]['ageGroupUnknown'] += 1

		if city in stateCount[stateName]['cities']:
			stateCount[stateName]['cities'][city] += 1
		else:
			stateCount[stateName]['cities'][city] = 1

	return stateCount


def cityCounts(data):
	cityCount = dict()

	for i in range(data.shape[0]):

		stateName = getStateName(data['state'][i].upper())
		gender = data['gender'][i]
		ageGroup = str(data['ageGroup'][i])
		lat = str(data['lat'][i])
		lon = str(data['lng'][i])

		city = data['city'][i].strip()

		if stateName not in cityCount:
			cityCount[stateName] = {}

		state = cityCount[stateName]

		if city in state:
			state[city]['count'] += 1
		else:
			state[city] = {
				'count': 1,
				'lat': lat,
				'lon': lon,
				'ageGroup1': 0,
				'ageGroup2': 0,
				'ageGroup3': 0,
				'ageGroupUnknown': 0,
				'genderMale': 0,
				'genderFemale': 0,
				'genderMale': 0,
				'genderUnknown': 0,
			}

		if type(gender) != type(1.0):
			if gender.lower() == 'm':
				state[city]['genderMale'] += 1
			elif gender.lower() == 'f':
				state[city]['genderFemale'] += 1
			else:
				state[city]['genderUnknown'] += 1
		else:
			state[city]['genderUnknown'] += 1

		if ageGroup == '1.0':
			state[city]['ageGroup1'] += 1
		elif ageGroup == '2.0':
			state[city]['ageGroup2'] += 1
		elif ageGroup == '3.0':
			state[city]['ageGroup3'] += 1
		else:
			state[city]['ageGroupUnknown'] += 1

		cityCount[stateName] = state

	return cityCount


def getVictims(data):
	cityVictims = dict()

	for i in range(data.shape[0]):
		stateName = getStateName(data['state'][i].upper())

		city = data['city'][i].strip()
		victimID = data['victimID'][i]
		name = data['name'][i]
		age = data['age'][i]
		url = data['url'][i]
		ageGroup = data['ageGroup'][i]
		date = parser.parse(data['date'][i])
		gender = data['gender'][i]

		if stateName in cityVictims:
			state = cityVictims[stateName]
		else:
			state = {}

		if city in state:
			state[city]['count'] += 1
		else:
			state[city] = {
				'count': 1,
				'victims': []
			}

		victim = {
			'_id': str(victimID),
			'url': url,
			'name': name if type(name) != type(1.0) else 'Unknown',
			'age': str(int(age)) if not isnan(age) else 'Unknown',
			'ageGroup': str(int(ageGroup)) if not isnan(ageGroup) else 'Unknown',
			'date': date.strftime('%d %b %Y'),
			'gender': str(gender) if type(gender) is not type(1.0) else 'Unknown',
			'city': city,
			'state': stateName
		}

		state[city]['victims'].append(victim)

		cityVictims[stateName] = state

	return cityVictims

def getVictimsList(data):
	victims = {}

	counts = {
		'M': {
			'1.0':0,
			'2.0':0,
			'3.0':0,
			'total': 0,
		},
		'F': {
			'1.0':0,
			'2.0':0,
			'3.0':0,
			'total': 0
		}
	}

	for i in range(data.shape[0]):
		stateName = getStateName(data['state'][i].upper())

		city = data['city'][i].strip()
		victimID = data['victimID'][i]
		name = data['name'][i]
		age = data['age'][i]
		url = data['url'][i]
		ageGroup = data['ageGroup'][i]
		date = parser.parse(data['date'][i])
		gender = data['gender'][i]

		victims[str(victimID)] = {
			'url': url,
			'name': name if type(name) != type(1.0) else 'Unknown',
			'age': str(int(age)) if not isnan(age) else 'Unknown',
			'ageGroup': str(int(ageGroup)) if not isnan(ageGroup) else 'Unknown',
			'date': date.strftime('%d %b %Y'),
			'state': stateName,
			'city': city,
			'gender': str(gender) if type(gender) is not type(1.0) else 'Unknown'
		}

		if str(gender) in counts:
			counts[gender]['total']+=1
			if str(ageGroup) in counts[gender]:
				counts[str(gender)][str(ageGroup)] += 1

	return victims

if __name__ == '__main__':
	slate_gun_deaths = readCSV(location='data', filename='/Users/sachinmb/VDS/SlateGunDeath/SlateGunDeaths.csv')
	stateCount = stateCounts(slate_gun_deaths)
	cityCount = cityCounts(slate_gun_deaths)
	cityVictims = getVictims(slate_gun_deaths)
	victims = getVictimsList(slate_gun_deaths)
	writeJSON(stateCount, location='data', filename='/Users/sachinmb/VDS/SlateGunDeath/PreprocessedData/stateCounts.json')
	writeJSON(cityCount, location='data', filename='/Users/sachinmb/VDS/SlateGunDeath/PreprocessedData/cityCounts.json')
	writeJSON(cityVictims, location='data', filename='/Users/sachinmb/VDS/SlateGunDeath/PreprocessedData/cityVictims.json')
	writeJSON(victims, location='data', filename='/Users/sachinmb/VDS/SlateGunDeath/PreprocessedData/victimsList.json')