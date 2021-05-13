# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import csv

employeeFileName = 'EmployeeTester.csv'
dataFileName = 'LockingData.csv'
verifiedStr = 'VERIFIED'
lockedStr = 'SECURITY_QUESTION'
unlockedStr = 'UNKNOWN_LOCK_CODE'
lockList = []
activeDurations = []

def findAvgTimeBetweenLocks(activeDurations):
    total = 0
    count = 0
    for duration in activeDurations:
        total = total + duration
        count = count + 1
    if count > 0:
        avgMilis = total/count
        print('Average (millis): ' + str(avgMilis))
        avgHours = avgMilis/1000/3600
        return avgHours
    else:
        return 0

def recordActiveDurations(data):
    lockList = []
    count = 0
    subcount = 0
    locked = 0
    while(len(data) > count):
        #Check of the current row indicates a lock
        if data[count][1] == verifiedStr and data[count][2] == lockedStr:
            locked = 1
            #Record the lock time
            lockTime_milis = data[count][4]
            #Continue interating down the list until we find the prior verified state
            while(len(data) > count + 1):
                count = count + 1
                #If this row in the verified state, record the time
                if data[count][1] == verifiedStr and data[count][2] == unlockedStr:
                    activeTime_milis = data[count][4]
                    account = [row[0], lockTime_milis, activeTime_milis]
                    print(account)
                    lockList.append(account)
                    activeDurations.append(int(lockTime_milis) - int(activeTime_milis))
                    break
        count = count + 1
    return locked

def isEmployee(id, employeeList):
    employee = 0
    for item in employeeList:
        if id == item:
            employee = 1
            break
    return employee

#Read in the list of employee tester IDs and create an array of their IDs
def createEmployeeList(file):
    list = []
    with open(file) as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',')
        for row in fileReader:
            if(row[0] != 'Ibotta Customer ID'):
                list.append(row[0])
    return list


#Main Method
if __name__ == '__main__':
    totalAccountCount = 0
    lockAccountCount = 0
    neverlockAccountCount = 0
    employeeList = createEmployeeList(employeeFileName)
    data = []
    with open(dataFileName) as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',')
        #Loop over each row in the data sheet.  **NOTE:  The data sheet must be sorted first by account ID
        #and then by Millis in decending order
        for row in fileReader:
            #Check if that row is an employee record.  If it is append all records for that employee
            #into a data array
            if bool(isEmployee(row[0], employeeList)):
                if len(data) == 0:
                    data.append(row)
                elif data[len(data)-1][0] == row[0]:
                    data.append(row)
                else:
                    #print(data)
                    #Pass the data array for locking analysis
                    locked = recordActiveDurations(data)
                    totalAccountCount = totalAccountCount + 1
                    if(bool(locked)):
                        lockAccountCount = lockAccountCount + 1
                    else:
                        neverlockAccountCount = neverlockAccountCount + 1
                    data = []
    print(activeDurations)
    print('Total Accounts: ' + str(totalAccountCount))
    print('Number of Accounts with Locks: ' + str(lockAccountCount))
    print('Number of Accounts with No Locks: ' + str(neverlockAccountCount))
    avg = findAvgTimeBetweenLocks(activeDurations)
    print('Average Active Time: ' + str(avg))

