from datetime import *

def strpdatetime(string, format, use_type=datetime):
    return use_type.fromtimestamp(mktime(strptime(string,format)))
    
def strpdate(string,format):
    return strpdatetime(string,format,use_type=date)
    
class monthdelta(object):
    def __init__(self, months=0):
        self.month = months
        
    def __rsub__(self, obj):
        return obj + monthdelta(-self.month)

    def __add__(self, obj):
        return self.__radd__(obj)

    def __radd__(self, obj):
        try:
            result = obj.replace(day=1)
            if self.month > 0:
                month_to_add = self.month
                add_days = 32
            else:
                add_days = -1
                month_to_add = -self.month

            # We have to iterate here to avoid borderline effect on variable days months
            while month_to_add > 0:
                result = (result + timedelta(days=add_days)).replace(day=1)
                month_to_add -= 1

            try:
                return obj.replace(year=result.year, month=result.month)
            except ValueError:
                return (result + monthdelta(1)) - timedelta(days=1)
        except Exception:
            # Essentially a type error
            raise TypeError, "unsupported operand type(s): '%s' and '%s'" % (type(self), type(obj))


def xdaterange(start, end=None, step=timedelta(days=1)):
    while end is None or start < end:
        yield start
        start += step

def daterange(start, end, step=timedelta(days=1)):
    return list(xdaterange(start, end, step))