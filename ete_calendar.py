from datetime import date, timedelta, datetime


class ETECalendar:
    def __init__(self, first_day, last_day, school_days, wlist, blist):
        self.fday = first_day
        self.lday = last_day
        self.sdays = school_days
        self.d = date.today()

        self.black_list = []
        self.wlist = wlist

        self.generate_black_list(blist)
        self.generate_white_list()

        self.ndays = self.number_days_until(first_day, last_day).days
        self.days_left = self.number_days_until(self.d.strftime('%Y-%m-%d'), last_day).days
        self.sdays_left = self.school_days_left() - 1

        self.school_days_checker()

    def school_days_left(self):
        sdl = 0
        ld = datetime.strptime(self.lday, '%Y-%m-%d').date()
        for dt in self.daterange(self.d, ld):
            if dt not in self.black_list:
                sdl += 1
        return sdl

    def school_days_checker(self):
        sdays_checker = self.ndays - len(self.black_list) + 1
        if self.sdays != sdays_checker:
            raise TypeError(f"Error, school days count: {sdays_checker}, should be: {self.sdays}. "
                            f"Black list days count: {len(self.black_list)}")

    @staticmethod
    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    def generate_black_list(self, blist):
        i = 0
        while i < len(blist):
            if blist[i] != 'between':
                datetime_object = datetime.strptime(blist[i], '%Y-%m-%d').date()
                self.black_list.append(datetime_object)
                i += 1

            else:
                self.black_list.pop(-1)
                sdate = datetime.strptime(blist[i - 1], '%Y-%m-%d').date()
                edate = datetime.strptime(blist[i + 1], '%Y-%m-%d').date()

                delta = edate - sdate

                for j in range(delta.days + 1):
                    bday = sdate + timedelta(days=j)
                    self.black_list.append(bday)
                i += 2

        weekdays = [5, 6]
        s_dt = datetime.strptime(self.fday, '%Y-%m-%d').date()
        l_dt = datetime.strptime(self.lday, '%Y-%m-%d').date()
        for dt in self.daterange(s_dt, l_dt):
            if dt.weekday() in weekdays:
                self.black_list.append(dt)

    def generate_white_list(self):
        for day in self.wlist:
            datetime_object = datetime.strptime(day, '%Y-%m-%d').date()
            if datetime_object in self.black_list:
                self.black_list.remove(datetime_object)

    def check_today(self):
        d1 = datetime.strptime(self.fday, '%Y-%m-%d').date()
        d2 = datetime.strptime(self.lday, '%Y-%m-%d').date()
        if self.d not in self.black_list and (d1 <= self.d <= d2):
            return True
        else:
            return False

    @staticmethod
    def number_days_until(date1, date2):
        d1 = datetime.strptime(date1, '%Y-%m-%d').date()
        d2 = datetime.strptime(date2, '%Y-%m-%d').date()
        return d2 - d1

    def today_str(self):
        return self.d.strftime("%d/%m/%Y")
