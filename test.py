import datetime
import pytz

# Datetime module information
today = datetime.date.today()  # today's date
today.weekday()  # day of the week of today (Monday = 0, Sunday = 6)
today.isoweekday()  # day of the week of today (Monday = 1, Sunday = 7)
d = datetime.date(2016, 7, 24)
print(d)
print(today)

time_delta = datetime.timedelta(days=7)
print(today + time_delta)

# date2 = date1 + timedelta
# timedelta = date1 + (or -) date2

birthday = datetime.date(2017, 4, 9)

days_until_birthday = birthday - today
print(days_until_birthday.total_seconds())

# datetime.time() is not very useful since most of the time
# you want to handle both the days and times
t = datetime.time(10, 0, 45, 100000)
print(t.hour)

dt = datetime.datetime(2016, 4, 9, 12, 0, 0, 0)
print(dt)

dt_delta = datetime.timedelta(hours=12)
print(dt + dt_delta)

dt_today = datetime.datetime.today()  # returns without a timezone
dt_now = datetime.datetime.now()  # can pass a timezone
dt_utcnow = datetime.datetime.utcnow()  # does not assign timezone

print(dt_today)
print(dt_now)
print(dt_utcnow)

dt_new = datetime.datetime(2016, 7, 27, 12, 30, 45, 0, tzinfo=pytz.UTC)
print(dt_new)  # includes UTC offset

dt_utcnow = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

dt_est = dt_utcnow.astimezone(pytz.timezone('US/Eastern'))
dt_pst = dt_utcnow.astimezone(pytz.timezone('US/Pacific'))
print(dt_est)

for tz in pytz.all_timezones:
    print(tz)

# to assign a timezone to a naive datetime, one must run a timezone localize function
dt = datetime.datetime.now()
est_tz = pytz.timezone('US/Eastern')

dt = est_tz.localize(dt)

print(dt.strftime('%B %d, %Y'))

s = 'August 10, 2016'
dt = datetime.datetime.strptime(s, '%B %d, %Y')
print(dt)

# Named Tuple - a lightweight object that works just like a regular tuple, but is more readable
# Tuples are immutable - remember!
# Has the functionality of a tuple but with some other properties of a dictionary
from collections import namedtuple

color = (55, 155, 255)

print(color[0])  # returns 55 - but anyone looking at it might not know what the numbers represent

Color = namedtuple('Color', ['red', 'green', 'blue'])
color = Color(55, 125, 255)  # one way of using namedtuple
color = Color(red = 55, green = 125, blue = 255)  # alternate way of constructing

print(color[0])
print(color.red)  # both of these statements print the same thing

# don't have to type everything over like you would with a dictionary
white = Color(255, 255, 255)
print(white.blue)


# if __name__ == '__main__' explanation
# ??
print(__name__)

# str() vs repr()
# The goal of __repr__ is to be unambiguous
# The goal of __str__ is to be readable
a = [1, 2, 3, 4]
b = 'sample string'

print(str(a))
print(repr(a))

print(str(b))
print(repr(b))

# Else clauses on for loops
my_list = [1, 2, 3, 4, 5]

for i in my_list:
    print(i)
else: # think of this statement as a no-break statement
    print('Hit the for/else statement')

# In other words, if the entire for loop ran without breaking, then the else clause will be run

# Dictionary tests

dict = {'a': 3, 'b':5, 'c':8}
print(dict)
for key in dict:
    print(key)

# testing some tuple stuff

tup = (1, 2)
for val in tup:
    print(val)

# Creating a generator

def int_gen(n):
    num = 0
    while num < n:
        yield num
    num += 1

class Dog:

    def __init__(self, color, size):
        self.color = color
        self.size = size

    def __str__(self):
        return "I am a dog that is " + self.color + " and " + self.size + "."

d = Dog("brown", "large")
print(d)

g = lambda x: x ** 2

print(g(3))