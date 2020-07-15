import requests
import json
import csv
import time
import datetime
from operator import itemgetter
import xlwt


class NYCPokemon:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "referer": "https://nycpokemap.com/?forcerefresh"
        }

    def get_pokemon_filtered_data(self, pokemon_numeric_filter, file_name):
        myExcelFile = xlwt.Workbook(encoding='utf-8')
        sheet1 = myExcelFile.add_sheet("sheet-1")
        sheet1.col(0).width = 5000
        sheet1.col(1).width = 5000
        sheet1.write(0, 0, "Lat, Lng")
        sheet1.write(0, 1, "Despawn Time")
        row = 1

        currentTimeStamp = str(int(time.time()))
        pokemon_numeric_filter = pokemon_numeric_filter.replace(",", "%2C")
        api_url = "https://nycpokemap.com/query2.php?mons="+pokemon_numeric_filter+"&time="+currentTimeStamp+"&since=0"
        print("API URL: ", api_url)
        res = requests.get(api_url, headers=self.headers)
        print(res.status_code)
        resJSON = json.loads(res.content)
        allPokemonsDictList = resJSON['pokemons']
        # with open("DataFileSample.csv", 'w', encoding="utf-8", newline="") as output_fp:
        # csv_writer = csv.writer(output_fp)
        # csv_writer.writerow(["Lat, Lng", "Despawn Time"])
        all_pokemon_data_list = []
        for pokemon in allPokemonsDictList:
            lat = pokemon['lat']
            lng = pokemon['lng']
            coords = lat + "," + lng
            despawnTimeEpoch = pokemon['despawn']
            despawnTimeEpoch_diff = (int(despawnTimeEpoch) - int(time.time()))
            despawnTimeFinal = (str(datetime.timedelta(seconds=despawnTimeEpoch_diff))).split(":")[1:]
            despawnTimeFinal = ":".join(despawnTimeFinal)
            print("Coords: ", coords)
            print("Despawn Time: ", despawnTimeFinal)
            if (despawnTimeEpoch_diff/60) > 8:
                all_pokemon_data_list.append([coords, despawnTimeFinal, (despawnTimeEpoch_diff/6)])
        all_pokemon_data_list_sorted = sorted(all_pokemon_data_list, key=itemgetter(2))
        for idx, sorted_pokemon in enumerate(all_pokemon_data_list_sorted):
            sheet1.write(row, 0, sorted_pokemon[0])
            sheet1.write(row, 1, sorted_pokemon[1])
            row += 1
    # csv_writer.writerow(sorted_pokemon[:2])
        myExcelFile.save(file_name+".xls")



if __name__ == '__main__':
    nycPokemonInstance = NYCPokemon()
    # FileName e.g., TestSampleFile
    file_name = "TestSampleFile"

    # add filter value. Add comma separated values for multiple filters
    pokemonFilter = "65,190"

    nycPokemonInstance.get_pokemon_filtered_data(pokemonFilter, file_name)
