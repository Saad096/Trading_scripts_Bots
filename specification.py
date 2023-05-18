import time
import openai
import google.auth
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set your GPT-3 API key
openai.api_key = "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"

# Google Sheets API credentials
creds = None
creds_json = 'keys.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets']

def get_gpt3_response(prompt, max_tokens):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.8
    )
    return response.choices[0].text.strip()

def get_sheets_api():
    global creds
    if not creds:
        creds = service_account.Credentials.from_service_account_file(creds_json, scopes=scopes)

    try:
        sheets_api = build('sheets', 'v4', credentials=creds)
    except HttpError as error:
        print(f"An error occurred: {error}")
        sheets_api = None
    return sheets_api

def monitor_google_sheet(sheet_id, interval=30):
    sheets_api = get_sheets_api()
    if not sheets_api:
        print("Unable to access Google Sheets API.")
        return

    last_processed_row = 1

    while True:
        # try:
        sheet_data = sheets_api.spreadsheets().values().get(
            spreadsheetId=sheet_id, range='Sheet1!A2:H'  # Update the range to include columns A to G
        ).execute()
        rows = sheet_data.get('values', [])
        # print(rows)
        # exit()

        for row_idx, row in enumerate(rows[last_processed_row - 1:], start=last_processed_row):
            print(row)
            # exit()
            if len(row) >= 5 and row[3] and row[4] and (len(row) == 5 or not row[5] or not row[6]):
                # short_prompt = f'Give me the Specifications of the product{pr}; Size, shape, texture specifically.''
                product = row[3]  # Update the index to 3 for the 4th column (Product)
                verity = row[4]  # Update the index to 4 for the 5th column (Verity)
                print(product, verity)
                if(row[1]=='Fruits'):
                    # long_prompt = f'Give me long Specifications of the Fruit name {product} variety {verity} must be in one line ,must be in horizontol line;"Size:, Shape:, Skin Color:, Flesh Color:, Texture:, Weight"'
                    # short_prompt = f'Give me short Specifications of the Fruit name {product} variety{verity} in the following format ,must be in horizontol line;"Size: (in numeric value), Shape: (in one word) , Skin Color: (in one word and one color), Flesh Color: (in one word and one color), Texture: (less than two lines), Weight: (in Kg)"'
                    # summary = f'Give me two to three lines description of the Fruit name {product} variety{verity}'

                    # long_prompt = f'Give me long Specifications of the Fruit name {product} variety {verity} must be in horizontol line;"this must include the TSS value , Acidity and three key specifications of this fruit except Size, Shape, Skin Color, Flesh Color, Texture and weight; each specification should be in one to three words maximum, seperated by commas"'
                    long_prompt = f'Give me short Specifications of the Fruit name {product} variety {verity} in the following format ,must be in horizontol line;"Scientific name: (in one word to three words maximum), Origin: (in one word to three words maximum) , TSS value: (in numeric value or words or percentage), Acidity: (in numeric value or words or percentage), Taste: (in less than four words), Seed: (in one word to three words maximum), Ripening Season: (in less than two lines), Nutritional Value: (in less than two lines), Shelf life: (in numeric values or words)"'
                    short_prompt = f'Give me short Specifications of the Fruit name {product} variety{verity} in the following format ,must be in horizontol line;"Size: (in numeric value with measurement unit), Shape: (in one word to three words maximum) , Skin Color: (in one word to three words maximum), Flesh Color: (in one word to three words maximum), Texture: (less than two lines), Weight: (in grams only)"'
                    summary = f'Give me two to three lines description of the Fruit name {product} variety{verity} must be in horizontol line; "the description can include hilights of this fruit, region of production, seasonality,fruit likeness among consumers, other exciting features of the fruit"'

                elif(row[1] == 'vegetables'):
                    # short_prompt = f'Give me short Specifications of the vegetable name {product} variety{verity} in the following format ,must be in horizontol line;"Size: (in numeric value), Shape: (in one word) , Color: (in one word and one color), Appearance: (in one word), Texture: (less than two lines), Weight: (in Kg)"'
                   # long_prompt = f'Give me short Specifications of the vegetable name {product} variety {verity} must be in horizontol line;"the long specification must include the key specifications of the vegetable except Size, Shape, Skin Color, Appearance, Texture and weight; each specification should be in one to three words maximum, seperated by commas"'
                    long_prompt = f'Give me short Specifications of the vegetable name {product} variety {verity} in the following format ,must be in horizontol line;"Scientific name: (in one word to three words maximum), Origin: (in one word to three words maximum) , Taste: (in less than four words), Seed: (in one word to three words maximum), Ripening Season: (in less than two lines), Nutritional Value: (in less than two lines), Shelf life: (in numeric values or words)"'
                    short_prompt = f'Give me short Specifications of the vegetable name {product} variety{verity} in the following format ,must be in horizontol line;"Size: (in numeric value with measurement unit), Shape: (in one word to three words maximum) , Skin Color: (in one word to three words maximum), Appearance: (in one word to three words maximum), Texture: (less than two lines), Weight: (in grams only)"'
                    summary = f'Give me two to three lines description of the Vegetable name {product} variety{verity} must be in horizontol line; "the description can include hilights of this vegetable, region of production, seasonality,vegetable likeness among consumers, other exciting features of the vegetable"'

                else:
                    continue

                # short_prompt = f"Write  short specifications for Product {product} of verity {verity}."
                short_description = get_gpt3_response(short_prompt, 40)

                # long_prompt = f"Write Long specifications for Product {product} of verity {verity}."
                long_description = get_gpt3_response(long_prompt, 100)

                summary_description = get_gpt3_response(summary, 200)

                sheets_api.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=f'Sheet1!F{row_idx + 1}:H{row_idx + 1}',  # Update the range to columns F and G
                    valueInputOption='RAW',
                    body={'values': [[short_description, long_description.replace("\n", ""), summary_description.replace("\n", "")]]}
                ).execute()

                print(f"Updated row {row_idx + 2} with short and long descriptions.")
                last_processed_row = row_idx + 1

        time.sleep(interval)
        # except Exception as e:
        #     print(f"An error occurred while monitoring the sheet: {e}")

if __name__ == '__main__':
    sheet_id = '1r9hD8Wi8NRe4nAGlELqYrC5lHKCCl0CLayiTBno-k_A'
    monitor_google_sheet(sheet_id)