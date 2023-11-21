def sqr_grid(v): # a function to determine if a number is square (returns True if square)
    root = v ** 0.5
    if int(root) != 0:
        if root / int(root) == 1:
            return True
        else:
            return False

# Perform check to see if there are the same number of values on each line
# and if those values add up to the correct number.
def checkvalid(dictionary):
    if dictionary == rows:
        name = "row"
    elif dictionary == colms:
        name = "column"
    elif dictionary == diag:
        name = "diagonal"
    lenvalid = True
    sumvalid = True
    root = int(len(u) ** 0.5)
    for x in dictionary:
        suf = ""
        linelen = len(dictionary[x])
        
        if linelen > (root + 1) or linelen < (root - 1):
            suf = "s"
        if linelen > root:
            print("\n{} {} has {} extra value{}.".format(name.title(), x, (linelen - root), suf) )
            lenvalid = False
        elif linelen < root:
            print("\n{} {} is missing {} value{}.".format(name.title(), x, (root - linelen), suf) )
            lenvalid = False

        totalline = 0
        for n in dictionary[x]:
            try:
                totalline += int(n)
            except:
                continue
        if totalline != sumofrcd:
            print(name.capitalize(), x, "adds up to", totalline, ". This is wrong.")
            sumvalid = False 

    if sumvalid == True:
        print("\nAll {}s add up to".format(name), sumofrcd)
    elif sumvalid == False:
        print("Not all {}s add up to".format(name), sumofrcd, ". CHECK FAILED.", warning)

    if lenvalid == True:
        print("\nAll {}s have the correct number of values ({})".format(name, rowsize))
    elif lenvalid == False:
        print("\nNot all {}s have the correct number of values ({})".format(name, rowsize), warning)
    
    if lenvalid != True or sumvalid != True:
        return False
    return True
        
warning = "   <--- !!!"    

while True:
    while True:
        try:
            filename = input("\nPlease enter the name of the text file you wish to open, for example '3x3' or '4x4.txt': ")
            print("\n")
            if ".txt" not in filename:
                filename += ".txt" 
            file = open(filename, "r")
            break
        except:
            print("That is not a valid file name.")
    print(file.read())
    file.seek(0)
    rows = {}
    empty = 0
    i = 1
    filesize = len(file.readlines())
    file.seek(0)
    while True:
        line = file.readline().split()
        if line != []:
            rows[i] = []
            for x in line:
                try:
                    rows[i].append(int(x))# add each value in the line to a dictionary of rows as an integer
                except:
                    rows[i].append(x)
            i+= 1
        elif line == []:
            empty += 1
            if len(rows) < filesize - empty:
                continue
            elif len(rows) >= filesize - empty:
                break
                   
    emptyline = False
    if empty > 1:
        print("\nBlank lines removed for validation purposes but this file will NOT be valid. \nPlease remove blank lines.", warning)
        emptyline = True

    file.seek(0)
    u = file.read().split() # u is a list of all values in the grid for testing number of values and for repeat values
    rowsize = round(len(u) ** 0.5) #Determines proper row length by getting the square root of number of values

    
    # Find what each row/column/diagonal should add up to with a formula that takes the total number
    # of values (Row size squared) and the row size (square root of number of values)
    # and results in the only integer that each R/C/D can equal if you rearrange all the values so that they all
    # add up to the same integer
    sumofrcd = int(((rowsize ** 2) +1) / 2 * rowsize) #sum of rcd = sum of Rows, Columns, Diagonals
    

    # Make a dictionary of columns from the rows
    colms = {}
    try:
        for k in range(0,len(rows)):
            for x in range(1,len(rows) + 1):
                try:
                    colms[k + 1].append(rows[x][k]) # Add the 'k'th index from row[x] to the 'k'th column
                except:
                    colms[k + 1] = [rows[x][k]] 
    except:
        print("Error while separating column values, this is likely due to incorrect text formatting.")
    
    # Make dictionary of diagonals from the rows
    diag = {1:[], 2:[]} # Two keys are hardcoded as this will be the same for any size grid
    i = 0
    try:
        for x in rows:
            diag[1].append(rows[x][i])
            i+=1
        for x in rows:
            i -= 1
            diag[2].append(rows[x][i])
    except:
        print("Error while separating diagonal values, this is likely due to incorrect text formatting.")
    
    if len(u) == len(set(u)): # check for repeated values
        repeats = False
        print("\nNo values are repeated.")
    else:
        repeated = {}
        for x in u:
            if x not in repeated:
                if u.count(x) > 1:
                    repeated[x] = u.count(x)
        for n in repeated:
            print(n, "is repeated", repeated[n], "times.")
        repeats = True
    if repeats:
        print("Some values are repeated. CHECK FAILED.", warning)
    

    
    if sqr_grid(len(u)): #if there are a square number of values, then we know there is only one suitable order (length of rows/columns)
        print("\nThere are a square number of values in the text file ({}). \n".format(len(u)))
        print("Considering the number of values; This should be a " + str(rowsize) + "x" + str(rowsize) + " grid.")
    else:
        print("\nThere are NOT a square number of values in the text file.", warning)


    oob = False #out of bounds
    for x in rows: # check if any integers excede total number of values or are invalid
        for n in rows[x]:
            try:
                if n > len(u) or n < 1:
                    print("\nInvalid integer in text file: ", n)
                    oob = True
            except:
                print("\nInvalid character in text file:", n, warning)
                oob = True          
    if not oob:
        print("\nAll integers in grid are valid.")
    
    print("\nEstimated correct line total:", sumofrcd)
    # check that all rows, columns and diagonals add up to the right number and have the right length
    rcd = False
    if checkvalid(rows) and checkvalid(colms) and checkvalid(diag):
        rcd = True

    # Overall check/Results
    if not emptyline and sqr_grid(len(u)) and not oob and not repeats and rcd:
        file.seek(0)
        print("\nFile validated successfully!")
        valid = open("VALID_" + filename, 'w')
        valid.write(file.read())
        valid.close()
        file.close()
        print("Valid File Saved!")
    else:
        print("\nFile not suitable.")

    



