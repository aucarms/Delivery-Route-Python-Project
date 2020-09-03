# Carmen Au, Student ID: 001231431
from DistanceInformation import Graph
from DistanceInformation import Vertex
from PackageInformation import packageInformation
from PackageInformation import packageDataTable
from Truck import Truck
from datetime import datetime, timedelta


# set start time for all trucks:
# original date and time starting at 12AM
datetime_original = datetime(year=2020, month=8, day=30)


# start time at 8AM for Truck1 (priority packages )
hours_to_add = 8
datetime_truck1 = datetime_original + timedelta(hours = hours_to_add)

# start time at 9:05
hours_to_add = 9
minutes_to_add = 5
datetime_truck2 = datetime_original + timedelta(hours = hours_to_add, minutes = minutes_to_add)



# imports CSV files
import csv
exit = False
# loop until user exits program
# Space time complexity is O(N)
while exit is False:
    #open WGUPS Package CSV file
    with open('WGUPSpackageFile.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        delivery_packages = packageDataTable(10)
        packages_to_be_delivered = []
        
        # Transfers package data in to hashtable
        # space complexity: 0(N)
        for row in spamreader:
            # Checks if package ID is a numeric value
            if row[0].isdigit():
                if "Wrong address listed" in row[7]:
                    row[1] = '410 S State St'
                    row[4] = '84111'
                
                packageID = int(row[0])
                deliveryAddress = row[1]
                city = row[2]
                state = row[3]
                zipCode = row[4]
                deadline = row[5]
                weight = row[6]
                notes = row[7]
                status = row[8]
                delivery_time = row[9]
                load_time = ''
                packages_to_be_delivered.append(packageID)
                package = packageInformation(packageID, deliveryAddress, city, state, deadline, zipCode, weight, notes, status, delivery_time,load_time)
                # Assigns variables 
                key = packageID
                value = package    
                delivery_packages.insertItem(key, value)


    with open('distance_table.csv', newline='') as csvDataFile:
        reader = list(csv.reader(csvDataFile, delimiter = ','))
        distance_table = []
        total_distance = {}

        # import distance data to a list
        # space complexity: 0(N)
        for row in reader:
            distance_table.append(row)



    # import CSV file that contains location names
    with open('LocationByName.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter = ',')
        location_info = []
        vertex_list = []
        graph = Graph()

        

        i = 0
        #import vertex label, address, and name of location to a list
        # space complexity: 0(N)
        for row in csvReader:
            location_info.append(row)
            
            if '5383 S 900 East #104' in location_info[i][1]:
                location_info[i][1] = '5383 South 900 East #104'
            

            vertex_num = location_info[i][0]
            address = location_info[i][1]
            location_name = location_info[i][2]
            vertex = Vertex(vertex_num,address,location_name)
            vertex_list.append(vertex)
            graph.add_vertex(int(vertex_num))
            i+=1
        
        # import distance data to a dictionary
        # space complexity: 0(N) 
        for key in graph.adjacent_edge_list:
            j = 0
            # Space-time complexity is O(N)
            while j <= (len(distance_table[key])-1):
                vertex_a = key
                vertex_b = j
                distance = (distance_table[vertex_a][vertex_b])
                if '.' in distance and (distance != '0.0'):
                    graph.add_total_distance(vertex_a, vertex_b, distance)
                j += 1 
        
        
        
        #function to find fastest delivery route using dijkstra algorithm
        def find_fastest_route(graph, truck, destination_list, package_list):
            hub = 0
            nearest_distance = None
            total_distance_traveled = 0.00
            visited_list = []
            package_list = package_list
            destination_list = destination_list
            
            
            
            #finds nearest location from the starting point (hub)
            # space complexity: 0(N)
            for key in graph.edge_distance:
                if key[0] == hub and key[1] in destination_list:
                    if nearest_distance == None: 
                        nearest_distance = graph.edge_distance[key]
                        nearest_coord = key
                    else:
                        if float(nearest_distance) > float(graph.edge_distance[key]):
                            nearest_distance = float(graph.edge_distance[key])
                            nearest_coord = key
            #keep track of total miles, and vertex that has been visited
            total_distance_traveled += nearest_distance
            visited_list.append(0)
            destination_list.remove(0)

            
            #loop to search for nearest location until all destinations are complete
            # Space time complexity is O(N)
            while len(destination_list) != 0:
                current_coord = nearest_coord[1]
                nearest_distance = 0.00
                #search nearest vertex / edge distance from current vertex
                #space time complexity: 0(N)
                for key in graph.edge_distance:
                    if key[0] == current_coord and key[1] in destination_list: 
                        if nearest_distance == 0.00: 
                            nearest_distance = float(graph.edge_distance[key])
                            nearest_coord = key
                        else:
                            if float(nearest_distance) > float(graph.edge_distance[key]):
                                nearest_distance = float(graph.edge_distance[key])
                                nearest_coord = key                  
                traveled_time = (nearest_distance/18)*60
                truck.date_time += timedelta(minutes = traveled_time)
                #search for location of package and update delivery time and status
                #space time complexity: 0(N)
                iter_package_list = list(package_list)
                for item in iter_package_list:
                    i = 0
                    bucket = item % len(delivery_packages.table)
                    # Space-time complexity is O(N)
                    while i < len(delivery_packages.table[bucket]):
                        if vertex_list[nearest_coord[1]].full_address in delivery_packages.table[bucket][i][1].deliveryAddress and delivery_packages.table[bucket][i][1].packageID == item :
                            delivery_packages.table[bucket][i][1].status = "Delivered"
                            delivery_packages.table[bucket][i][1].delivery_time = truck.date_time
                            package_list.remove(item)
                            # search_complete = True
                            i+=1
                        else:
                            i+=1
                destination_list.remove(nearest_coord[1])
                total_distance_traveled += nearest_distance
                visited_list.append(nearest_coord[1])
            print('Truck #',truck.truck_num, " total distance traveled: ", round(total_distance_traveled,2),'\n')

        #initialize truck objects
        truck1 = Truck(1)
        truck1.truck_num = 1
        truck2 = Truck(2)
        truck2.truck_num = 2
        truck3 = Truck(3)
        truck3.truck_num = 3
        
        i = 0
        j = 0
        k = 0
        # sort and load packages to trucks based on priority
        # the for loop will search by each key(package ID) in the delivery package table and ensures that each package is loaded on to a truck based on priority / delivery notes
        #space time complexity 0(N)
        for key in delivery_packages.table:
            i = 0
            if j == 10:
                j = 0    
            # Space time complexity is O(N)
            while i < len(delivery_packages.table[j]) and j < 10:
                k=0
                #assigns packages to truck 2 based on special delivery notes
                if 'Can only' in delivery_packages.table[j][i][1].notes:
                    address = delivery_packages.table[j][i][1].deliveryAddress
                    #look for location by vertex number and add to destination and package list
                    #space time complexity 0(N)
                    for location in vertex_list:
                        if address in vertex_list[k].full_address:
                            vertex = vertex_list[location.label]
                            truck2.destination_list.append(vertex.label)
                            truck2.package_list.append(delivery_packages.table[j][i][1].packageID)
                            delivery_packages.table[j][i][1].load_time = truck2.date_time
                            packages_to_be_delivered.remove(delivery_packages.table[j][i][1].packageID)
                            i+=1
                            break
                        else: k += 1              
                #assigns packages to truck 3 based on special delivery notes "Delayed" and Zip Code
                elif ('Delayed' in delivery_packages.table[j][i][1].notes  or delivery_packages.table[j][i][1].zipCode == '84119' or delivery_packages.table[j][i][1].zipCode == '84118') and delivery_packages.table[j][i][1].packageID in packages_to_be_delivered:
                    address = delivery_packages.table[j][i][1].deliveryAddress
                    
                    #search for location by vertex number and add to destination and package list
                    #space time complexity 0(N)
                    for location in vertex_list:
                        if address in vertex_list[k].full_address:
                            vertex = vertex_list[location.label]
                            truck3.destination_list.append(vertex.label)
                            truck3.package_list.append(delivery_packages.table[j][i][1].packageID)
                            delivery_packages.table[j][i][1].load_time = truck3.date_time
                            packages_to_be_delivered.remove(int(delivery_packages.table[j][i][1].packageID))
                            i+=1
                            break
                        else: k += 1
                #assigns packages to truck 1 based on delivery deadline "AM" and Zip Code                    
                elif ('AM' in delivery_packages.table[j][i][1].deadline or delivery_packages.table[j][i][1].zipCode == '84115') and delivery_packages.table[j][i][1].packageID in packages_to_be_delivered:
                    address = delivery_packages.table[j][i][1].deliveryAddress
                    #look for location by vertex number and add to destination and package list
                    #space time complexity 0(N)
                    for location in vertex_list:
                        if address in vertex_list[k].full_address:
                            vertex = vertex_list[location.label]
                            truck1.destination_list.append(vertex.label)
                            truck1.package_list.append(delivery_packages.table[j][i][1].packageID)
                            delivery_packages.table[j][i][1].load_time = truck1.date_time
                            packages_to_be_delivered.remove(int(delivery_packages.table[j][i][1].packageID))
                            i+=1
                            break
                        else: k += 1   
                #assigns packages to truck 2 based on delivery deadline "EOD" and Zip Code
                elif 'EOD' in delivery_packages.table[j][i][1].deadline and delivery_packages.table[j][i][1].packageID in packages_to_be_delivered:
                    address = delivery_packages.table[j][i][1].deliveryAddress
                    #look for location by vertex number and add to destination and package list
                    #space time complexity 0(N)
                    for location in vertex_list:
                        if address in vertex_list[k].full_address:
                            vertex = vertex_list[location.label]
                            truck2.destination_list.append(vertex.label)
                            truck2.package_list.append(delivery_packages.table[j][i][1].packageID)
                            delivery_packages.table[j][i][1].load_time = truck2.date_time
                            packages_to_be_delivered.remove(int(delivery_packages.table[j][i][1].packageID))
                            i+=1
                            break
                        else: k += 1   
                    
                else:
                    i+=1
            j+=1
                

        
        #truck1 delivery starting delivery at 8:00 AM
        find_fastest_route(graph, truck1, list(dict.fromkeys(truck1.destination_list)), truck1.package_list)
        
        #truck3 delivery starting at 9:05 AM
        truck3.date_time = truck3.date_time+timedelta(minutes=65)
        find_fastest_route(graph, truck3, list(dict.fromkeys(truck3.destination_list)), truck3.package_list)

        #truck2 delivery starting at 9:30 AM
        truck2.date_time = truck2.date_time+timedelta(minutes=90)
        find_fastest_route(graph, truck2, list(dict.fromkeys(truck2.destination_list)), truck2.package_list)

    
    
        #Start Menu
        user_selection = input('>>> Hello, welcome to WGUPS!\n\nPlease select from the following options (A-C):\nA - Search by Package ID\nB - Search by Delivery Time\nC - Exit\n')
        if user_selection == "A" or user_selection == "a":
            #search package by package ID
            string = int(input('Search >>> Please enter a Package ID: '))
            delivery_packages.searchItem(string)
        elif user_selection =="B" or user_selection =="b":
            startH = input('Enter start time (HH) >> ')
            startM = input('Enter start time (MM) >> ')
            endH = input('Enter end time (HH) >> ')
            endM = input('Enter end (MM) >>')
            delivery_packages.searchPackageByTime(startH, startM, endH, endM)
        elif user_selection =="C" or user_selection =="c":
            exit = True
            break

