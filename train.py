import requests
import time
import termcolor
import tqdm
import pyttsx3


engine = pyttsx3.Engine()

engine.setProperty('rate', 150)

#// exit()

COLOR_MAPPING = {
    'RD':termcolor.colored('● RD', 'red'),
    'YL':termcolor.colored('● YL', 'yellow'),
    'GR':termcolor.colored('● GR', 'green'),
    'OR':termcolor.colored('● OR', 'yellow'),
    'BL':termcolor.colored('● BL', 'blue'),
    'SV':'● SV'
}

COLOR_NAMES_MAP = {
    'RD':'red',
    'YL':'yellow',
    'GR':'green',
    'OR':'yellow',
    'BL':'blue',
    'SV':'silver'
}

station_code_mapping = {
        "Addison Road-Seat Pleasant": "G03",
        "Anacostia": "F06",
        "Archives-Navy Memorial-Penn Quarter": "F02",
        "Arlington Cemetery": "C06",
        "Ashburn": "N12",
        "Ballston-MU": "K04",
        "Benning Road": "G01",
        "Bethesda": "A09",
        "Braddock Road": "C12",
        "Branch Ave": "F11",
        "Brookland-CUA": "B05",
        "Capitol Heights": "G02",
        "Capitol South": "D05",
        "Cheverly": "D11",
        "Clarendon": "K02",
        "Cleveland Park": "A05",
        "College Park-U of Md": "E09",
        "Columbia Heights": "E04",
        "Congress Heights": "F07",
        "Court House": "K01",
        "Crystal City": "C09",
        "Deanwood": "D10",
        "Downtown Largo": "G05",
        "Dunn Loring-Merrifield": "K07",
        "Dupont Circle": "A03",
        "East Falls Church": "K05",
        "Eastern Market": "D06",
        "Eisenhower Avenue": "C14",
        "Farragut North": "A02",
        "Farragut West": "C03",
        "Federal Center SW": "D04",
        "Federal Triangle": "D01",
        "Foggy Bottom-GWU": "C04",
        "Forest Glen": "B09",
        "Fort Totten": "B06,E06",
        "Franconia-Springfield": "J03",
        "Friendship Heights": "A08",
        "Gallery Pl-Chinatown": "B01,F01",
        "Georgia Ave-Petworth": "E05",
        "Glenmont": "B11",
        "Greenbelt": "E10",
        "Greensboro": "N03",
        "Grosvenor-Strathmore": "A11",
        "Herndon": "N08",
        "Huntington": "C15",
        "Hyattsville Crossing": "E08",
        "Innovation Center": "N09",
        "Judiciary Square": "B02",
        "King St-Old Town": "C13",
        "L'Enfant Plaza": "D03,F03",
        "Landover": "D12",
        "Loudoun Gateway": "N11",
        "McLean": "N01",
        "McPherson Square": "C02",
        "Medical Center": "A10",
        "Metro Center": "A01,C01",
        "Minnesota Ave": "D09",
        "Morgan Boulevard": "G04",
        "Mt Vernon Sq 7th St-Convention Center": "E01",
        "Navy Yard-Ballpark": "F05",
        "Naylor Road": "F09",
        "New Carrollton": "D13",
        "NoMa-Gallaudet U": "B35",
        "North Bethesda": "A12",
        "Pentagon": "C07",
        "Pentagon City": "C08",
        "Potomac Ave": "D07",
        "Reston Town Center": "N07",
        "Rhode Island Ave-Brentwood": "B04",
        "Rockville": "A14",
        "Ronald Reagan Washington National Airport": "C10",
        "Rosslyn": "C05",
        "Shady Grove": "A15",
        "Shaw-Howard U": "E02",
        "Silver Spring": "B08",
        "Silver Spring Transit Center": "T81",
        "Smithsonian": "D02",
        "Southern Avenue": "F08",
        "Spring Hill": "N04",
        "Stadium-Armory": "D08",
        "Suitland": "F10",
        "Takoma": "B07",
        "Tenleytown-AU": "A07",
        "Twinbrook": "A13",
        "Tysons": "N02",
        "U Street/African-Amer Civil War Memorial/Cardozo": "E03",
        "Union Station": "B03",
        "Van Dorn Street": "J02",
        "Van Ness-UDC": "A06",
        "Vienna/Fairfax-GMU": "K08",
        "Virginia Square-GMU": "K03",
        "Washington Dulles International Airport": "N10",
        "Waterfront": "F04",
        "West Falls Church": "K06",
        "West Hyattsville": "E07",
        "Wheaton": "B10",
        "Wiehle-Reston East": "N06",
        "Woodley Park-Zoo/Adams Morgan": "A04"
}

print("Line - No. Cars - Dest. - Occupancy - ETA (min.)\n")

iters = 1

for i in range(iters):
    for station_name in station_code_mapping:

        if station_name != "Vienna/Fairfax-GMU":
            continue

        time_now = int(time.time())
        station_code = station_code_mapping[station_name]

        response = requests.get(f'https://www.wmata.com/components/stations.cfc?method=getNextTrains&StationCode={station_code}&returnFormat=JSON&_={time_now}')

        print(station_name+':')
        data = response.json()['TRAINS']

         
     

        try:
            for line in data[:5]:
                print(COLOR_MAPPING[line['Line']], str(line['Car'])+' Car train to', line['Destination'], 'with an occupancy of', str(line['Oc']), 'is scheduled to arrive in '+str(line['Min'])+' min.' if line['Min'] not in ['BRD', 'ARR', 'DLY'] else termcolor.colored(f'[{line["Min"]}]', 'green'))
        except KeyError:
            termcolor.cprint(f'No Data!', 'yellow')
        finally:
            print('\n'*2)
        print('Key To Occupancy:')
        print('1 = Not Crowded')
        print('2 = Some Crowding')
        print('3 = Crowded')


    is_min_no = True
    allow_humor = True
    do_bell = True


    time.sleep(.5)

    try:
        temp = int(data[0]['Min'])
        del temp
    except:
        is_min_no = False

    engine.runAndWait()
    
    time_delay = 7.5
    tq_str = " " * 100
    
    if i+1 < iters:
        for tq_chr in tqdm.tqdm(tq_str, desc='Next Query'):
            time.sleep(time_delay/len(tq_str))
