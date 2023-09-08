import utils.nlp.parse as parse

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def main(day='today'):
    date = parse.Time(day)
    _date = date.strftime("%A, %d of MM of ")
    _year = date.strftime("%Y")
    _date = _date.replace('MM', months[date.month-1])
    _year = _year[:(len(_year) // 2)] + "-" + _year[(len(_year) // 2):]
    return str(_date)+str(_year)

#print(main('tomorrow'))