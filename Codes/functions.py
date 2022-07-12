'''This file contains all the functions of this program'''
import sys #Importing sys module
import datetime #Importing datetime module

def welcomeMessage():
    '''Function to the display welcome message'''
    print("\n" + "*" * 89)
    print("\t\t\t Welcome to the library management system.")
    print("*" * 89 + "\n")

def mainMenu():
    '''Function to show the main menu of the program'''
    global userInput #Declaring global variable
    continueInput = True 
    while continueInput == True:
        displayMainUserOptions()
        userInput = input("Please enter a value : ") 
        inputHandling() 

def displayMainUserOptions():
    '''Function to display the option for user to borrow, return or exit the program'''
    print("Enter '1' to borrow a book.")
    print("Enter '2' to return a book.")
    print("Enter '3' to add a book.")
    print("Enter '4' to exit.\n")

def inputHandling():
    '''Function to perform the respective intructions according to user input''' 
    if userInput == "1":
        borrowBook() 
    elif userInput == "2":
        returnBook()
    elif userInput == "3":
        addBook()
    elif userInput == "4":
        exitMessage()
    else:
        errorInput()

def errorInput():
    '''Function to display error message when user input is not 1 ,2, 3 or 4'''
    print("\n" + "*" * 89)
    print("\t\t\t\t     Invalid input!")
    print("\t\t     Please enter the value correctly among 1, 2, 3 or 4.")
    print("*" * 89 + "\n")

def openFile():
    '''Function to open the file'''
    file = open("BookInfo.txt", "r")
    return file

def writeFile():
    '''Function to write the file'''
    file = open("BookInfo.txt", "w")
    return file
   
def fileDictionary():
    '''Function to store the file in dictionary collection data type'''
    #Initializing
    bookDictionary = {}
    bookID = 1
    stringFile = openFile() 
    
    for line in stringFile:
        line = line.replace("\n","").split(",") 
        bookDictionary[str(bookID)] = line #Storing in dictionary collection data type with bookID as key and line as value
        bookID += 1
    stringFile.close()
    return bookDictionary

def bookTable():
    '''Function to display all the details of the books using the dictionary'''
    #Initializing
    bookInfo = fileDictionary()
    
    print("-" * 89 + "\n| Book-ID |  Name\t\t\t| Author   \t\t| Quantity\t| Price |" + "\n" + "-" * 89) 

    for key, value in bookInfo.items():
        print("| ", key, "\t  |  " + value[0] + "\t\t| " + value[1]+ "\t\t| " + value[2]+ "\t\t| " + value[3] + "\t|")
    print("-" * 89 + "\n")

def keyList():
    '''Function to store all the keys of dictionary in a list'''
    #Initializing
    bookDictionary = fileDictionary()
    keyList = []
    
    for key in bookDictionary.keys():
        keyList.append(key) #Adding dictionary key in the keyList which will be used later to check if the user input ID is among them
    return keyList 

def borrowBook():
    '''Function to borrow book'''
    #Initializing
    isBorrowing = True
    global borrowedBookIDList, borrowerName #Declaring global variables
    totalCost = 0
    borrowedBookIDList = []
    isBorrowerNameEmpty = True
    
    #Handling error so that the name of the borrower cannnot be empty
    while isBorrowerNameEmpty == True:
        
        borrowerName = input("Please enter the borrower's full name : ").replace(":", "") #Taking borrower's name as input from the user and using replace to handle file error

        if borrowerName == "":
            print("\n" + "*" * 89)
            print("\t\t\t  Please enter the borrower's name!")
            print("*" * 89 + "\n")
        else:
            isBorrowerNameEmpty = False
            
    
    while isBorrowing == True:
        bookTable()
        borrowValidation()

        print("\nDoes Mr/Ms.", borrowerName, "want to borrow another book?")
        continueBorrow = input("Press 'Enter' or any value to continue borrowing or 'no' to stop borrowing : ").lower()
        if continueBorrow == "no":
            isBorrowing = False #To exit this while loop
            writeBorrowDetail() #This function is called after the customer doesnot want to borrow more
            readUniqueFile() #This function is called to read and display the unique generated  borrow detail text file in the terminal

def displayInvalidID():
    '''Function to display invalid bookID'''
    print("\n" + "*" * 89)
    print("\t\t\t\t   Invalid ID entered!!!")
    print("*" * 89 + "\n")

def borrowValidation():
    '''Function to validate the borrow book ID and quantity'''
    #Initializing
    idList = keyList()
    bookDictionary = fileDictionary()
    global borrowBookID #Declaring global variables
    borrowBookID = input("Please enter the book ID to borrow : ")

    #Checking if the user input borrowBookID is in the dictionary key which contain all the available book ID
    if borrowBookID in idList:
        #Checking if the book is already borrowed or not
        if borrowBookID not in borrowedBookIDList:
            #Checking if the book which is to be borrowed has quantity above 0 
            if int(bookDictionary[borrowBookID][2]) > 0:
                borrowedBookIDList.append(borrowBookID) #Adding borrowBookID in the borrowedBookIDList to store all the borrowed bookID 
                print("\n" + "*" * 89)
                print("\t\t\t   The book is borrowed successfully.\n" + "*" * 89 + "\n")
                print("The cost of the book '" + bookDictionary[borrowBookID][0] + "' is " + bookDictionary[borrowBookID][3] + ".")
                writeBorrowUpdate() #This function is called everytime the book is borrowed
                bookTable()
            else:
                print("\n" + "*" * 89)
                print("\t\t\t   This book is not available for now.\n" + "*" * 89 + "\n")
        else:
            print("\n" + "*" * 89)
            print("\t\t\t    This book is already borrowed.\n" + "*" * 89 + "\n")
    else:
        displayInvalidID()
        borrowValidation()
    
def writeBorrowUpdate():
    '''Function to update the book detail table after borrowing the book'''
    #Initializing
    bookDictionary = fileDictionary()
    idList = keyList()
    bookFile = writeFile()

    for key, value in bookDictionary.items(): 
        #Checking if the key is equal to the last index of the borrowedBookIDList
        if str(key) in borrowedBookIDList[-1]:
            #Decreasing quantity and writing the update for the borrowed books in the BookInfo.txt file
            quantityUpdate = int(value[2]) - 1 #Decreasing the quantity of the borrowed book
            #Checking if the key is the last line so that there will be no new line otherwise this will create problem in adding process
            if str(key) == idList[-1]:
                bookFile.write(value[0] + "," + value[1] + "," + str(quantityUpdate) + "," + value[3]) #Writing without new line for last line
            else:
                bookFile.write(value[0] + "," + value[1] + "," + str(quantityUpdate) + "," + value[3] + "\n")  #Writing with new line
                
        else:
            #Writing for the unborrowed books in the BookInfo.txt file
            #Checking if the key is the last line so that there will be no new line otherwise this will create problem in adding process
            if str(key) == idList[-1]:
                bookFile.write(value[0] + "," + value[1] + "," + value[2] + "," + value[3]) #Writing without new line for last line
            else:
                bookFile.write(value[0] + "," + value[1] + "," + value[2] + "," + value[3] + "\n") #Writing with new line
    bookFile.close()

def borrowedCost():
    '''Function to calculate the cost of borrowed books'''
    #Initializing
    bookDictionary = fileDictionary()
    totalCost = 0

    for borrowedBook in borrowedBookIDList:
        cost = float(bookDictionary[borrowedBook][3].replace("$","")) #Extracting the third index of the value of the dictionary and replacing the '$' with empty string
        totalCost += cost #Calculating the total cost
    totalBorrowedCost = "$" + str(totalCost)
    return totalBorrowedCost

def writeBorrowDetail():
    '''Function to write a text file with borrow detail'''
    #Initializing
    global uniqueFileName
    bookDictionary = fileDictionary()
    idList = keyList()
    currentDateTime = str( datetime.datetime.now()).split(".")[0].replace(":", ";") #Converting into a string and removing the microsecond by spliting with '.' and taking the 0 index only and then replacing the ':' of time with ';' 
    uniqueFileName = "B- " + borrowerName + " " + currentDateTime #Using borrower name, date and time to create unique file name 

    #Writing the borrow details as a txt file
    writeFile = open(str(uniqueFileName) + ".txt", "w")
    writeFile.write("\n" + "*" * 49 + "\n")
    writeFile.write("\t\t---BORROW DETAILS--- \n")
    writeFile.write("\nDate and Time : " + str(currentDateTime) + "\n")
    writeFile.write("Name : " + str(borrowerName) + "\n")
    writeFile.write("-" * 49 + "\n| BookID |  Name \t\t\t| Price\t|\n" + "-" * 49 + "\n")

    #Writing all the borrowed book with bookID, book name and price in the borrow detail generated text file
    for borrowedBook in borrowedBookIDList:
        writeFile.write("| " + str(borrowedBook) + "\t |  " + bookDictionary[borrowedBook][0] + "\t\t| " + bookDictionary[borrowedBook][3] + "\t|\n")

    writeFile.write("-" * 49 + "\n \t \t \t     Total cost : " + str(borrowedCost()) + "\n") #Writing the total cost
    writeFile.write("\n" + "*" * 49 + "\n")
    writeFile.close()
    
def returnBook():
    '''Function to return book'''
    #Initializing
    isReturning = True
    global returnedBookIDList, returnerName, lendingDayList #Declaring global variables
    returnedBookIDList = []
    lendingDayList = []
    isReturnerNameEmpty = True

    #Handling error so that the name of the borrower cannnot be empty
    while isReturnerNameEmpty == True:

        returnerName = input("Please enter the returner's full name : ").replace(":", "") #Taking returner's name as input from the user and using replace to handle file error
        
        if returnerName == "":
            print("\n" + "*" * 89)
            print("\t\t\t  Please enter the returner's name!")
            print("*" * 89 + "\n")
        else:
            isReturnerNameEmpty = False

    while isReturning == True:
        bookTable()
        returnValidation()

        print("\nDoes Mr/Ms.", returnerName, "want to return another book?")
        continueReturn = input("Press 'Enter' or any value to continue returning or 'no' to stop returning : ").lower()
        if continueReturn == "no":
            isReturning = False #To exit this while loop
            writeReturnDetail() #This function is called after the customer doesnot want to return more
            readUniqueFile() #This function is called to read and display the unique generated return detail text file in the terminal

def returnValidation():
    '''Function to validate the return book ID'''
    #Initializing
    idList = keyList()
    bookDictionary = fileDictionary()
    global returnBookID #Declaring global variables
    
    returnBookID = input("Please enter the book ID to return : ")

    #Checking if the user input returnBookID is in the dictionary key which contain all the avaialble book's ID
    if returnBookID in idList:
        #Checking if the book is already returned or not
        if returnBookID not in returnedBookIDList:
            fineValidation()
            fineChargeValidation()
            returnedBookIDList.append(returnBookID) #Adding returnBookID in the returnedBookIDList to store all the returned bookID 
            print("\n" + "*" * 89)
            print("\t\t\t    The book is returned successfully.\n" + "*" * 89 + "\n")
            print("The fine for the book '", bookDictionary[returnBookID][0], "' is", fineList[-1], ".")
            writeReturnUpdate()
            bookTable()
        else:
            print("\n" + "*" * 89)
            print("\t\t\t     This book is already returned.\n" + "*" * 89 + "\n")
    else:
        displayInvalidID()
        returnValidation()

def fineValidation():
    '''Function to validate the fine'''
    isInteger = False
    global lendingDays #Declaring global variables

    while isInteger == False:
        #Implementing try except handling
        try:
            lendingDays = int(input("Enter the lending days : ")) #Taking lending days as input from the user of int type
            #Handling for negative numbers
            if lendingDays >= 0:
                lendingDayList.append(lendingDays)
                isInteger = True #Exiting the loop if the input is an integer
            else:
                print("\n" + "*" * 89)
                print("\t\t   Invalid input entered. Please enter a positive number!")
                print("*" * 89 + "\n")
        except:
            print("\n" + "*" * 89)
            print("\t\t   Invalid input entered. Please enter a whole number!")
            print("*" * 89 + "\n")

def fineChargeValidation():
    '''Function to validate the total fines of the book and total fines of all books'''
    #Initializing
    finePerDay = 0.1
    totalFine = 0
    maxLendingDays = 10
    global fineList #Declaring global variable
    fineList = []
    
    for lendedDays in lendingDayList:
        #Checking if the lending days is more than 10 days
        if lendedDays > maxLendingDays:
            fine = float((lendedDays - maxLendingDays) * finePerDay) #Calculating total fine for a book
            returnedFine = "$" + str(round(fine, 2))
            fineList.append(returnedFine) #returnedFine is added to FineList which will be used later in the return detail text file generation part to show the respective price of the book
            totalFine += fine #Calculating fine of all the books that have exceed 10 lending days
        else:
            fine = 0
            returnedFine = "$" + str(round(fine, 2))
            fineList.append(returnedFine)
            totalFine += fine #Calculating fine of all the books that have not exceed 10 lending days
    returnedTotalFine = "$" + str(round(totalFine, 2))
    return returnedTotalFine

def writeReturnUpdate():
    '''Function to update the book detail table after returning the book'''
    bookDictionary = fileDictionary()
    idList = keyList()
    bookFile = writeFile()

    for key, value in bookDictionary.items(): 
        #Checking if the key is equal to the last index of the returnedBookIDList
        if str(key) in returnedBookIDList[-1]:
            #Increasing quantity and writing the update for the returned books in the BookInfo.txt file
            quantityUpdate = int(value[2]) + 1 #Increasing the quantity of the returned book
            #Checking if the key is the last line so that there will be no new line otherwise this will create problem in adding process
            if str(key) == idList[-1]:
                bookFile.write(value[0] + "," + value[1] + "," + str(quantityUpdate) + "," + value[3]) #Writing without new line for last line
            else:
                bookFile.write(value[0] + "," + value[1] + "," + str(quantityUpdate) + "," + value[3] + "\n")
                
        else:
            #Writing for the books which are not returned in the BookInfo.txt file
            #Checking if the key is the last line so that there will be no new line otherwise this will create problem in adding process
            if str(key) == idList[-1]:
                bookFile.write(value[0] + "," + value[1] + "," + value[2] + "," + value[3]) #Writing without new line for last line
            else:
                bookFile.write(value[0] + "," + value[1] + "," + value[2] + "," + value[3] + "\n") #Writing with new line
    bookFile.close()

def writeReturnDetail():
    '''Function to write a text file with return detail'''
    #Initializing
    global uniqueFileName
    bookDictionary = fileDictionary()
    idList = keyList()
    i = 0
    currentDateTime = str( datetime.datetime.now()).split(".")[0].replace(":", ";") #Converting into a string and removing the microsecond by spliting with '.' and taking the 0 index only and then replacing the ':' of time with ';' 
    uniqueFileName = "R- " + returnerName + " " + currentDateTime #Using returner name, date and time to create unique file name 

    #Writing the return details as a txt file
    writeFile = open(str(uniqueFileName) + ".txt", "w")
    writeFile.write("\n" + "*" * 68 + "\n")
    writeFile.write(" \t \t \t---RETURN DETAILS--- \n")
    writeFile.write("\nDate and Time : " + str(currentDateTime) + "\n")
    writeFile.write("Name : " + str(returnerName) + "\n")
    writeFile.write("-" * 65 + "\n| BookID |  Name \t\t\t| Lending days \t| Fine  |\n" + "-" * 65 + "\n")

    #Writing all the returned book with bookID, book name, lending days and fine in the return detail generated text file
    for returnedBook in returnedBookIDList:
        writeFile.write("| " + str(returnedBook) + "\t |  " + bookDictionary[returnedBook][0] + "\t\t| " + str(lendingDayList[i]) + "\t\t| " + fineList[i] + "\t|\n")
        i += 1

    writeFile.write("-" * 65 + "\n \t \t \t \t \t     Total fine : " + fineChargeValidation() + "\n\n") #Writing the total fine
    writeFile.write("    Note: The fine exceeding 10 lending days is $0.1 per day.")
    writeFile.write("\n" + "*" * 68 + "\n")
    writeFile.close()

def readUniqueFile():
    '''Function to read the unique generated text file and displaying in the terminal'''
    readFile = open(str(uniqueFileName) + ".txt", "r")
    print(readFile.read())
    readFile.close()

def bookNameList():
    '''Function to store all the keys of dictionary in a list'''
    #Initializing
    bookDictionary = fileDictionary()
    nameList = []
    
    for value in bookDictionary.values():
        nameList.append(value[0]) #Adding dictionary book name in the nameList which will be used later to check if the user input book name is among them during adding
    return nameList

def addBook():
    '''Function to add new book in the BookInfo.txt''' 
    isAdding = True

    while isAdding == True:
        bookTable()
        addBookValidation()
        
        continueAdd = input("Press 'Enter' or any value to continue adding another book or 'no' to stop adding : ").lower()
        if continueAdd == "no":
            isAdding = False #To exit this while loop

def addBookValidation():
    '''Function to validate book name, book quantity, book quantity and book price in order to add'''
    existingBookNameList = bookNameList()
    global bookName, bookAuthor, bookQuantity, bookCost #Declaring global variables
    isInteger = False
    isFloat = False
    isBookNameEmpty = True
    isAuthorNameEmpty = True

    #Handling error so that the name of the book to be added cannot be empty
    while isBookNameEmpty == True:

        bookName = input("Enter the name of the book : ") #Taking book name input from the user
        
        if bookName == "":
            print("\n" + "*" * 89)
            print("\t\t\t Please enter the book name to be add the book!")
            print("*" * 89 + "\n")
        else:
            isBookNameEmpty = False

    #Checking if the book already exist in the BookInfo text file
    if bookName not in existingBookNameList:

        #Handling error so that the name of the book author to be added cannot be empty
        while isAuthorNameEmpty == True:

            bookAuthor = input("Enter the author name of the book : ")
            
            if bookAuthor == "":
                print("\n" + "*" * 89)
                print("\t\t\t  Please enter the author name of the book!")
                print("*" * 89 + "\n")
            else:
                isAuthorNameEmpty = False

        #Handling error using try catch         
        while isInteger == False:
            try:
                bookQuantity = int(input("Enter the quantity of the book : "))
                #Handling for negative inputs
                if bookQuantity >= 0:
                    isInteger = True
                else:
                    print("\n" + "*" * 89)
                    print("\t\t Invalid input entered. Please enter a positive number!")
                    print("*" * 89 + "\n") 
            except:
                print("\n" + "*" * 89)
                print("\t\t  Invalid input entered. Please enter a whole number!")
                print("*" * 89 + "\n")

        #Handling error using try catch
        while isFloat == False:
            try:
                bookCost = float(input("Enter the cost of the book : "))
                #Handling for negative inputs
                if bookCost >= 0:
                    isFloat = True
                else:
                    print("\n" + "*" * 89)
                    print("\t\t Invalid input entered. Please enter a positive number!")
                    print("*" * 89 + "\n")
            except:
                print("\n" + "*" * 89)
                print("\t   Invalid input entered. Please enter a decimal or whole number!")
                print("*" * 89 + "\n")

        print("\n" + "*" * 89)
        print("\t\t   The book '" + bookName + "' is added successfully.")
        print("*" * 89 + "\n")
        updateAddedBook()
        bookTable()
    else:
        print("\n" + "*" * 89)
        print("\t\t\t   This book already exist.")
        print("*" * 89 + "\n")

def updateAddedBook():
    '''Function to add the new book details in text file'''
    file = open("BookInfo.txt", "a") #Opening the BookInfo.txt file in append mode to append new values
    file.write("\n" + bookName + "," + bookAuthor + "," + str(bookQuantity) + ",$" + str(bookCost)) #Writing the book details in new line
    file.close()

def exitMessage():
    '''Function to display exit message'''
    print("\n" + "*" * 89)
    print("\t\t   Thank you for using our library management system.")
    print("\t\t\t\t    See you soon!")
    print("*" * 89 + "\n")
    sys.exit() #Exiting the program
