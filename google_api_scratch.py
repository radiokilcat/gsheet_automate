from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

{"installed":{"client_id":"812898708254-thlmlfhmo79apiolrd3dd9u7s2kqs0vk.apps.googleusercontent.com","project_id":"quickstart-1584953971300","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"o_VRSP88PIaPWxznFCa6JnY1","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '10VHHFZCBFQmSo3Ro32Yzt49Q90aDHTWcime4Fz3KnEk'
SAMPLE_RANGE_NAME = 'march_detail!B2:B473'

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

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s, %s' % (row[0], row[4]))
            # if row.:
            #     print('%s' % row)
            for i in row:
                if "пятница" in i:
                    # cell_to_update =
                    print('%s' % i)


if __name__ == '__main__':
    main()