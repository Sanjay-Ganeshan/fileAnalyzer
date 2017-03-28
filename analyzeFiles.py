import os


def bytesToHumanReadable(numBytes):
    numBytes = float(numBytes)
    KB_CUTOFF = 3
    MB_CUTOFF = 5
    GB_CUTOFF = 1
    BYTES_PER_KB = 1024.0
    BYTES_PER_MB = BYTES_PER_KB * 1024
    BYTES_PER_GB = BYTES_PER_MB * 1024
    def kb(x):
        return round(x / BYTES_PER_KB,2)
    def mb(x):
        return round(x / BYTES_PER_MB,2)
    def gb(x):
        return round(x / BYTES_PER_GB,2)
    numToReturn = numBytes
    unit = "B"
    if gb(numBytes) > GB_CUTOFF:
        numToReturn = gb(numBytes)
        unit = "GB"
    elif mb(numBytes) > MB_CUTOFF:
        numToReturn = mb(numBytes)
        unit = "MB"
    elif kb(numBytes) > KB_CUTOFF:
        numToReturn = kb(numBytes)
        unit = "KB"
    return "%.2f %2s" % (numToReturn,unit)
    

def humanSizeOf(path):
    return bytesToHumanReadable(sizeOf(path))

def sizeOf(path):
    return os.path.getsize(path)

def fetch_dir(path,includeDirs = True, includeFiles = True):
    sizeDict = {}
    navigationDict = {}
    path = path.replace("/","\\")
    root = path
    for path, dirs, files in os.walk(path):
        files.sort()
        for fn in files:
            ffn = os.path.join(path, fn)
            #print(ffn, humanSizeOf(ffn))
            currSize = sizeOf(ffn)
            if includeFiles:
                sizeDict[ffn] = currSize
            if includeDirs:
                sizeDict[path] = currSize + sizeDict[path] if path in sizeDict else currSize
            navigationDict[path] = dirs,files
    return root,navigationDict,sizeDict
    
def investigate(root,navigationDict,sizeDict):
    currentNode = root
    print(sorted(list(sizeDict.keys())[:15]))
    input()
    clearScreen()
    while True:
        clearScreen()
        print("Exploring %s -- Total Size = %s" % (currentNode,bytesToHumanReadable(sizeDict[currentNode])))
        for eachDir in sorted(navigationDict[currentNode][0]):
            print("%s %s" % (eachDir,bytesToHumanReadable(sizeDict["%s%s\\" % (currentNode,eachDir)])))
        for eachFile in sorted(navigationDict[currentNode][1]):
            print("%s %s" % (eachFile,bytesToHumanReadable(sizeDict["%s\\%s" %(currentNode,eachFile)])))
        nextNode = input()
        if nextNode == "..":
            nextNode = ""
            current = currentNode.split("\\")[:-1]
            for eachThing in current:
                nextNode += "%s\\" % eachThing
            nextNode = nextNode[:-2]
        else:
            nextNode = "%s\\%s" % (root,currentNode)
        currentNode = nextNode

def getLargestFiles(numFiles,path):
    root,nav,sizes = fetch_dir(path,False,True)
    reverseLookupDict = {}
    for eachKey in sizes:
        reverseLookupDict[sizes[eachKey]] = eachKey
    allValues = list(map(lambda x: sizes[x], sizes.keys()))
    for eachValue in sorted(allValues)[::-1][:numFiles]:
        print("%s - %s" %(reverseLookupDict[eachValue], bytesToHumanReadable(eachValue)))

    

def clearScreen():
    os.system("cls")


getLargestFiles(20,input())

