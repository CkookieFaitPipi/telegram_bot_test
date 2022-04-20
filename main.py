import logging
from telegram.ext import Updater, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open("test_sheet")


def get_stat(id):
    worksheet = spreadsheet.get_worksheet(0)
    ids = worksheet.col_values(1)
    if str(id) in ids:
        stat = worksheet.row_values(ids.index(str(id)) + 1)[1]
        return stat
    else:
        return 'None'


def answ(update, context):

    update.message.reply_text(f'Ваша машина находиться в городе: {get_stat(update.message.text)}.')


def main():
    updater = Updater('5316050737:AAE7P45s1sX00-Jcd6Q4UqHVPBTao2gKWRw')
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, answ)

    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()