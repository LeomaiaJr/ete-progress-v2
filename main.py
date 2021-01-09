from ete_files_handler import ETEFilesHandler
from ete_calendar import ETECalendar
from twitter_provider import TwitterProvider
import math

FULL_CHARACTER = '█'
EMPTY_CHARACTER = "░"
CHARACTER_COUNT = 16


def calc_percent(full_value, value) -> int:
    return ((value * 100) / full_value).__round__()


def number_of_characters(percent) -> str:
    character_value = 100 / CHARACTER_COUNT
    characters = ((100 - percent) / character_value)
    characters = math.floor(characters)
    progress_bar = ''
    for cf in range(characters):
        progress_bar += FULL_CHARACTER
    for ce in range(CHARACTER_COUNT - characters):
        progress_bar += EMPTY_CHARACTER
    return progress_bar


ete_files = ETEFilesHandler()
d = ete_files.read_file_data("assets/school_days_data.json")
fday, lday, sdays, wlist, blist = d['schoolDaysData'].values()

ete_calendar = ETECalendar(fday, lday, sdays, wlist, blist)

ed = ete_files.read_file_data("assets/ete_progress_data.json")['eteProgressData']['schoolDaysLeft']['percent']

days_left_percent = calc_percent(ete_calendar.ndays, ete_calendar.days_left)
sdays_left_percent = calc_percent(ete_calendar.sdays, ete_calendar.sdays_left)

if ete_calendar.check_today():
    if sdays_left_percent == 0 and ete_calendar.sdays_left != 0:
        pass
    else:
        update_data = {
            "eteProgressData": {
                "schoolDaysCount": ete_calendar.sdays,
                "schoolDaysLeft": {
                    "days": ete_calendar.sdays_left,
                    "percent": sdays_left_percent
                },
                "daysCount": ete_calendar.ndays,
                "daysLeft": {
                    "days": ete_calendar.days_left,
                    "percent": days_left_percent
                },
                "lastUpdate": ete_calendar.today_str(),
            }
        }
        ete_files.write_file_data('assets/ete_progress_data.json', update_data)

        info = f'{100 - sdays_left_percent}%   {number_of_characters(sdays_left_percent)}\n' \
               f'Faltam {ete_calendar.days_left} dias ({ete_calendar.sdays_left} letivos)'

        print(info)

        twitter_provider = TwitterProvider()
        twitter_provider.tweet_sth(info)
