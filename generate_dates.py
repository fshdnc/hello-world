# requirements: faker
# generates dates in different formats to be normalize
# ("Helmikuun 1. 2003", "01.02.2003")
# 1. Helmikuuta vuonna 2003
# etc.

import sys
import random
from faker import Faker


def generate_gold(fake, n):
    golds = [fake.date() for i in range(n)]
    golds = [format_conversion(gold) for gold in golds]
    return golds

def format_conversion(date):
    '''YYYY-MM-DD generated to DD.MM.YYYY'''
    YYYY, MM, DD = date.split('-')
    return '.'.join([DD, MM, YYYY])

def unnormalize(date):
    to = random.choice([1,2,3])
    if to == 1:
        return to_YYYY_MM_DD(date)
    elif to ==2:
        return to_MM_DD_YYYY(date)
    else:
        return to_DD_MM_YYYY(date)

def to_YYYY_MM_DD(DDMMYYYY):
    '''2019.01.05
       2019.1.5
       2019-01-05
       2019-1-5
       2019/1/5
       2019/01/05'''
    DD, MM, YYYY = DDMMYYYY.split('.')
    DD, MM = remove_zero(DD, MM)
    sep = choose_sep(empty=False)
    return sep.join([YYYY, MM, DD])
        

def remove_zero(DD, MM):
    remove = random.choice([1,2])
    if remove == 1:
        DD = _remove_zero(DD)
        MM = _remove_zero(MM)
        return DD, MM
    else:
        return DD, MM

def _remove_zero(NN):
    assert len(NN) == 2 or len(NN) == 1
    if NN.startswith('0'):
        return NN[-1]
    else:
        return NN
        
def choose_sep(empty=True):
    if empty:
        sep = random.choice([1,2,3,4])
    else:
        sep = random.choice([1,2,3])
        
    if sep == 1:
        return '.'
    elif sep == 2:
        return '/'
    elif sep == 3:
        return '/'
    else:
        return None

def to_MM_DD_YYYY(DDMMYYYY):
    '''Toukokuun 10. (päivänä) 2018'''
    DD, MM, YYYY = DDMMYYYY.split('.')
    DD = paivana(DD)
    MM = spell_month(MM)
    MM = MM + 'n'
    MM = case(MM)
    YYYY = vuonna(YYYY)
    return ' '.join([MM, DD, YYYY])

def case(string):
    case = random.choice([1,1,1,1,2,3,3,3,3])
    if case == 1:
        return string.lower()
    elif case == 2:
        return string.upper()
    else:
        return string[0].upper() + string[1:].lower()
    
def spell_month(MM):
    return month_dict[int(MM)]

month_dict = {1: 'tammikuu', 2: 'helmikuu', 3: 'maaliskuu', 4: 'huhtikuu', 5: 'toukokuu', 6: 'kesäkuu', 7: 'heinäkuu', 8: 'elokuu', 9: 'syyskuu', 10: 'lokakuu', 11: 'marraskuu', 12: 'joulukuu'}

def paivana(DD):
    add = random.choice([1,2])
    DD = _remove_zero(DD)
    if add == 1:
        return DD + '. päivänä'
    else:
        return DD + '.'

def vuonna(YYYY):
    add = random.choice([1,2])
    if add == 1:
        return 'vuonna ' + YYYY
    else:
        return YYYY

def to_DD_MM_YYYY(DDMMYYYY):
    '''1. Helmikuuta vuonna 2003'''
    DD, MM, YYYY = DDMMYYYY.split('.')
    DD, MM = remove_zero(DD, MM)
    sep = choose_sep()
    if sep:
        return sep.join([DD, MM, YYYY])
    else:
        DD = paivana(DD)
        MM = spell_month(MM)
        MM = MM + 'ta'
        MM = case(MM)
        YYYY = vuonna(YYYY)
        return ' '.join([DD, MM, YYYY])


def write(dates, golds):
    with open('generated_dates.txt', 'w') as f:
        for date, gold in zip(dates, golds):
            f.write(date+'\t'+gold+'\n')

if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
    except IndexError:
        print('First argument is the number of dates to be generated')
    fake = Faker(['fi_FI'])
    golds = generate_gold(fake, n)
    dates = [unnormalize(gold) for gold in golds]
    write(dates, golds)
