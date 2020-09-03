import datetime

class packageInformation:
    # constructor
    # Space-time complexity is O(1)
    def __init__(self, packageID, deliveryAddress, city, state, deadline, zipCode, weight, notes, status, delivery_time,load_time):
        
        self.packageID = int(packageID)
        self.deliveryAddress = deliveryAddress
        self.city = city
        self.state = state
        self.deadline = deadline
        self.zipCode = zipCode
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
        self.notes = notes
        self.load_time = load_time
    
    #function to print package details
    # Space-time complexity is O(1)s
    def printPackage(self):
        packageID = self.packageID
        deliveryAddress = self.deliveryAddress
        city = self.city
        state = self.state
        deadline = self.deadline
        zipCode = self.zipCode
        weight = self.weight
        status = self.status
        delivery_time = self.delivery_time   
        notes = self.notes
        print('\n')
        print(packageID,"   ",deliveryAddress,"   ",city,"   ",state,"   ",zipCode,"   ",deadline,"   ",weight,"   ",status,"   ",delivery_time)
    



# hashtable class using chaining
# space complexity: 0(1)
class packageDataTable:
    #initializes hashtable with 10 empty buckets
    def __init__(self, initial_length=10):
        #initilizes table with an empty bucket list
        #space complexity: 0(N)
        self.table = []
        for i in range(initial_length):
            self.table.append([])


    # function to insert item in to hashtable
    # space complexity: 0(N)
    def insertItem(self, packageID, packageInformation):
        bucket = int(packageID) % len(self.table)
        key_value = [packageID, packageInformation]
        bucketList = self.table[bucket]
        bucketList.append(key_value)


    # function to search item in hashtable
    # space complexity: 0(N)
    def searchItem(self, string):
        i = 0
        packageNum = string
        #converts the input package ID to a bucket / hashtable key
        getKey = packageNum % 10
        #if condition to search package ID in hash table
        while i <= len(self.table[getKey]):
            if self.table[getKey][i][1].packageID == packageNum:
                self.table[getKey][i][1].printPackage()
                break
            else: 
                i += 1
        
    #function to search delivered packages by time range
    # space complexity: 0(N)
    def searchPackageByTime(self, startH, startM, endH, endM):
        # check and update hours and minutes to remove preceeding 0s
        if startH != ('00') and startH != ('0'):
            startH = int(startH.lstrip('0'))
        else: 
            startH = int(startH)
        if startM != ('00') and startM != ('0'):
            startM = int(startM.lstrip('0'))
        else:
            startM = int(startM)
        if endH != ('00') and endH != ('0'):
            endH = int(endH.lstrip('0'))
        else:
            endH = int(endH)
        if endM != ('00') and endM != ('0'):
            endM = int(endM.lstrip('0'))
        else:
            endM = int(endM)
        start_time = datetime.datetime(2020, 8, 30, startH, startM) 
        end_time = datetime.datetime(2020, 8, 30, endH, endM)

        bucket = 0
        # print package information: checks and updates delivery status based on user input search time. 
        # space complexity: 0(N)       
        for num in self.table:
            j = 0
            while j < len(self.table[bucket]):
                
                if start_time < self.table[bucket][j][1].load_time and end_time < self.table[bucket][j][1].load_time:
                    self.table[bucket][j][1].status = 'At Hub'
                    self.table[bucket][j][1].delivery_time = ''
                    self.table[bucket][j][1].printPackage()
                    j+=1
                
                elif start_time >= self.table[bucket][j][1].load_time and end_time > self.table[bucket][j][1].delivery_time:
                    self.table[bucket][j][1].printPackage()
                    j+=1

            
                elif start_time >= self.table[bucket][j][1].load_time and end_time <= self.table[bucket][j][1].delivery_time :
                    self.table[bucket][j][1].status = 'En route'
                    self.table[bucket][j][1].delivery_time = ''
                    self.table[bucket][j][1].printPackage()
                    j+=1
                else: 
                    print("missing:", "Load Time: ", self.table[bucket][j][1].load_time, "Delivery Time: ", self.table[bucket][j][1].delivery_time)
                    j+=1
            bucket+=1   


