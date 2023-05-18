import os
import time
import pandas as pd
import mysql.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openpyxl import load_workbook
import time
from tqdm import tqdm
import pandas as pd
from difflib import SequenceMatcher

variety_values = ['Beef Cattle', 'Bullock', 'Hanwoo', 'Kedah Kelantan', 'Aubrac', 'Salers', 'Rouge des près', 'Angus', 'Hereford', 'Wagyu', 'Black Angus', 'Heifer', 'Bull', 'Herefordshire', 'Red Angus', 'Dexter', 'Brahman', 'Shorthorn', 'Charolais', 'Limousin', 'Canterbury Angus', 'Rubia Gallega', 'Wakanui', 'Fiorentina', 'Ox', 'Nelore', 'Chianina', 'Blonde', 'Caledonia Crown', 'Maori Lakes', 'Canterbury', 'Cinta Senese DOP', 'Riverlands Angus', 'Greenstone Creek', 'Riverlands', 'Heifer - Scottona', 'Local Indian Dairy', 'Turina', 'Cow', 'Young Bull', 'Brangus', 'Whole birds', 'Calf', 'Dikbil', 'Bovine', 'Cow and Bull', 'Senepol', 'Brown Swiss Cattle', 'Sanhe', 'Barrosã', 'Red Bororo', 'Mirandesa', 'Crossbreed - Unspecified']


def similarity(a, b):
    if (str(a) in str(b) or str(b) in str(a)):
        return 1
    return 0


threshold = 0.8


def build_city_map(df_cities):
    city_map = {}
    for _, row in df_cities.iterrows():
        key = row['CountryName']
        city = row['CityName']
        state = row['State']
        if "," in city:
            city = city.split(',')[0]
        if key not in city_map:
            city_map[key] = [(state, city)]
        else:
            city_map[key].append((state, city))
    return city_map


def find_best_match(city_name, country_name, city_map):
    if country_name not in city_map:
        return "", city_name

    for state_city in city_map[country_name]:
        state, city = state_city
        if city_name == city:
            return state, city

    return "", city_name


def build_category_map(df_categories):
    category_map = {}
    for _, row in df_categories.iterrows():
        category_map[row['Product Name']] = row['category']
    return category_map


def remove_duplicate_rows(dst_config):
    # Connect to the Tazah_main database
    conn = mysql.connector.connect(**dst_config)
    cursor = conn.cursor()

    # Find duplicate rows ignoring the id
    query = """
        SELECT GROUP_CONCAT(id ORDER BY id) as ids
        FROM products
        GROUP BY CountryName, State, CityName, Hscode, Variety, ProductName, CurrencyUnit, PriceDate, AveragePrice, MaxPrice, MinPrice, category
        HAVING COUNT(id) > 1;
    """
    cursor.execute(query)
    duplicate_groups = cursor.fetchall()

    # Remove duplicate rows, keeping the one with the lowest id
    for group in duplicate_groups:
        ids = group[0].split(',')
        ids_to_delete = ids[1:]  # All ids except the first one

        delete_query = """
            DELETE FROM products
            WHERE id IN (%s);
        """ % ','.join(ids_to_delete)

        cursor.execute(delete_query)

    conn.commit()
    cursor.close()
    conn.close()


def remove_hanwoo_entries(dst_config):

    # Connect to the Tazah_main database
    conn = mysql.connector.connect(**dst_config)
    cursor = conn.cursor()

    # Delete rows with 'Hanwoo' as the variety
    for value in enumerate(variety_values):
        # print("Value = ", value)
        value = value[1]
        delete_query = f"DELETE FROM products WHERE Variety = '{value}';"
        cursor.execute(delete_query)

        conn.commit()
    cursor.close()
    conn.close()


def aggregate_duplicate_rows(dst_config):
    # Connect to the Tazah_main database
    conn = mysql.connector.connect(**dst_config)
    cursor = conn.cursor()

    # Find rows with the same attributes except for the MaxPrice
    query = """
        SELECT CountryName, State, CityName, Hscode, Variety, category, ProductName, CurrencyUnit, PriceDate, COUNT(DISTINCT MaxPrice) AS count,
               AVG(AveragePrice) AS mean_price, MIN(MinPrice) AS min_price, MAX(MaxPrice) AS max_price
        FROM products
        GROUP BY CountryName, State, CityName, Hscode, Variety, category, ProductName, CurrencyUnit, PriceDate
        HAVING count > 1;
    """
    cursor.execute(query)
    duplicate_rows = cursor.fetchall()

    # Delete duplicate rows and insert the aggregated row
    for row in duplicate_rows:
        delete_query = """
            DELETE FROM products
            WHERE CountryName = %s AND State = %s AND CityName = %s AND Hscode = %s AND Variety = %s AND category = %s AND ProductName = %s AND CurrencyUnit = %s AND PriceDate = %s;
        """
        cursor.execute(delete_query, row[:-4])

        insert_query = """
            INSERT INTO products (CountryName, State, CityName, Hscode, Variety, category, ProductName, CurrencyUnit, PriceDate, AveragePrice, MaxPrice, MinPrice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        aggregated_row = row[:-4] + (row[-3], row[-1], row[-2])
        cursor.execute(insert_query, aggregated_row)

    conn.commit()
    cursor.close()
    conn.close()


class ExcelFileHandler(FileSystemEventHandler):
    def process(self, file_path, city_map, category_map):
        # Read Excel files
        start_time = time.time()
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception as e:
            print('cuurupted file : ', file_path)
            return
        try:
            print("Product Name: ", df.loc[0]['ProductName'])
        except Exception as e:
            pass


        # Connect to MySQL databases
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Taza@1234",
            database="Tazah_Raw"
        )

        dst_config = {
            'user': 'root',
            'password': 'Taza@1234',
            'host': 'localhost',
            'database': 'Tazah_main'
        }
        dst_conn = mysql.connector.connect(**dst_config)

        cursor = connection.cursor()
        cursor_dst = dst_conn.cursor()

        # Insert data into MySQL tables
        counter = 0
        for _, row in df.iterrows():
            city_name = row['CityName']
            country_name = row['CountryName']
            updated_city_name = city_name
            # print("Row: ", counter, city_name)
            product_name = row['ProductName']
            category = category_map.get(product_name, '')
            counter += 1
            variety = row['variety']
            # Find the best match for city_name
            if (',' in city_name):
                city_name = updated_city_name.split(',')[0]
            updated_state, updated_city_name = find_best_match(city_name, country_name, city_map)

            if (len(updated_state) <= 1):
                updated_state = updated_city_name

            # Insert data into Tazah_Raw table
            query_raw = f"""
                INSERT INTO products (CountryName, CityName, ProductName ,variety, CurrencyUnit, Hscode, PriceDate, Price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            try:
                data_raw = (
                    country_name if pd.notna(country_name) else None,
                    city_name if pd.notna(city_name) else None,
                    row['ProductName'] if pd.notna(row['ProductName']) else None,
                    row['variety'] if pd.notna(row['variety']) else None,
                    row['Currency/Unit'] if pd.notna(row['Currency/Unit']) else None,
                    row['Hscode'] if pd.notna(row['Hscode']) else None,
                    row['Price Date'] if pd.notna(row['Price Date']) else None,
                    row['Price'] if pd.notna(row['Price']) else None,
                )
                cursor.execute(query_raw, data_raw)
            except Exception as e:
                print('row product name:', row['ProductName'])
                print("error: ", e)
                continue

            if row['Price'] == "-" or pd.isna(row['Price']):
                continue
            if '*' in row['Price']:
                row['Price'].replace("*", "")
            if row["variety"] == "-":
                row['variety'] = "Unspecified"

            # Insert data into Tazah_main table
            query_main = f"""
                INSERT INTO products (CountryName ,State ,CityName ,Hscode ,Variety ,ProductName , CurrencyUnit, PriceDate, AveragePrice, MaxPrice, MinPrice, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            data_main = (
                country_name if pd.notna(country_name) else None,
                updated_state if pd.notna(updated_state) else None,
                updated_city_name if pd.notna(updated_city_name) else None,
                row['Hscode'] if pd.notna(row['Hscode']) else None,
                variety if pd.notna(variety) else None,
                product_name if pd.notna(product_name) else None,
                row['Currency/Unit'] if pd.notna(row['Currency/Unit']) else None,
                row['Price Date'] if pd.notna(row['Price Date']) else None,
                row['Price'] if pd.notna(row['Price']) else None,
                row['Price'] if pd.notna(row['Price']) else None,
                row['Price'] if pd.notna(row['Price']) else None,
                category if pd.notna(category) else None,
            )
            cursor_dst.execute(query_main, data_main)

        connection.commit()
        dst_conn.commit()
        cursor.close()
        cursor_dst.close()
        connection.close()
        dst_conn.close()

        # aggregate_duplicate_rows(dst_config)
        remove_duplicate_rows(dst_config)
        remove_hanwoo_entries(dst_config)
        print("Took: ", time.time() - start_time, " seconds ")

    def on_created(self, event):
        if event.src_path.endswith('.xlsx') or event.src_path.endswith('.xls'):
            self.process(event.src_path, city_map, category_map)


def process_existing_files(folder_path, city_map, category_map):
    print("Synching Folder....")
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            ExcelFileHandler().process(file_path, city_map, category_map)
    print("Synched Successfully!")
    print("==========================================")


def monitor_folder(folder_path, city_map):
    event_handler = ExcelFileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    try:
        print("Processing new File.....")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print("New File processed!")
    print("==========================================")

    observer.join()


if __name__ == "__main__":
    folder_path = "Data"
    file_path_categories = 'Categories List.xlsx'
    file_path_cities = 'city_map_edit.csv'
    sheet_name = 'Sheet2'
    df_cities = pd.read_csv(file_path_cities)
    print("Building cities map")
    city_map = build_city_map(df_cities)
    print("Cities map built")
    print("Building Category Map")
    df_categories = pd.read_excel(file_path_categories, engine='openpyxl')
    category_map = build_category_map(df_categories)
    print("Category Map built")
    process_existing_files(folder_path, city_map, category_map)
    monitor_folder(folder_path, city_map)