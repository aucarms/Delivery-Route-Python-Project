from datetime import datetime, timedelta
from DistanceInformation import Graph
from DistanceInformation import Vertex


# constructor
# Space-time complexity is O(1)
class Truck:
    def __init__(self, truck_num):
        # original date set at August 30 and time set at 12AM
        datetime_original = datetime(year=2020, month=8, day=30)
        
        # set earliest start time to 8AM
        hours_to_add = 8
        delivery_starttime = datetime_original + timedelta(hours = hours_to_add)
        self.truck_num = truck_num
        self.destination_list = [0]
        self.package_list = []
        self.date_time = delivery_starttime
        
