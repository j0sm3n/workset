"""Evento calendario
    Añade a los distintos calendarios de Google, los turnos de trabajo,
    con el nombre del turno, fecha, hora de inicio y hora de fin.
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings


# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def nuevo_evento(turno, inicio, fin, calendario):
    """ Crea un nuevo evento en Google Calendar con los datos del turno,
    hora de inicio, hora de fin, y el calendario en el que debe crear
    el evento.
    """
    creds = None
    tools_dir = os.path.join(settings.BASE_DIR, 'tools')
    token_file = os.path.join(tools_dir, 'token.pickle')
    json_file = os.path.join(tools_dir, 'credentials.json')

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary':
        f'Turno {turno}',
        'location':
        'Estación de Benidorm',
        'start': {
            'dateTime': inicio,  # '2020-05-18T09:00:00-07:00',
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': fin,  # '2020-05-18T17:00:00-07:00',
            'timeZone': 'Europe/Madrid',
        },
        'reminders': {
            'useDefault':
            False,
            'overrides': [
                {
                    'method': 'popup',
                    'minutes': 24 * 60
                },
                {
                    'method': 'popup',
                    'minutes': 10
                },
            ],
        },
    }

    event = service.events().insert(
            calendarId=calendario,
            body=event
        ).execute()
    print(f"Event created: {event.get('htmlLink')}")
