from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = ''

class purchase:
    def __init__(self, value, date, category):
        self.value = value
        self.date = date
        self.category = category


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    stopWords = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресение"]
    newValues = []
    if not values:
        print('No data found.')
    else:
        for row in values:
            newRow = []
            for content in row:
                if any(sw in content for sw in stopWords):
                    for s in stopWords:
                        if s in content:
                            newRow.append(content.replace(", %s" % s, ""))
                else:
                    newRow.append(content)
            newValues.append(newRow)
        # print(newValues)

    value_input_option = 'RAW'
    value_range_body = result
    value_range_body['values'] = newValues

    # print(value_range_body)
    request2 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                                      valueInputOption=value_input_option, body=value_range_body)
    response = request2.execute()


if __name__ == '__main__':
    main()