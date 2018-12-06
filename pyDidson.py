import codecs
import struct
import os
import time
import csv
import datetime

# size = struct.calcsize("III?IfIIII?I32c256ciiiiII?IiIIIII120p")
# size = struct.calcsize("?")
# size = struct.calcsize("32c")
# size = struct.calcsize("L")
# size = struct.calcsize("I8cIIIIIIIIIIIIIIIIIIIIffffffffffffffffffffddfIfff?IIIfIffffff49152c")


StructSizes = {
        "x" : 1, #   pad byte	no value
        "c" : 1, #   char	bytes of length 1
        "b" : 1, #   signed char	integer
        "B" : 1, # 	unsigned char	integer
        "?" : 1, # 	_Bool	bool
        "h" : 2, #   short	integer
        "H" : 2, #   unsigned short	integer
        "i" : 4, # 	int	integer
        "I" : 4, # 	unsigned int	integer
        "l" : 4, # 	long	integer
        "L" : 4, # 	unsigned long	integer 
        "q" : 8, #   long long	integer
        "Q" : 8, #   unsigned long long	integer
        "f" : 4, # 	float	float
        "d" : 8, # 	double	float
        "s" : 1, # 	char[]	bytes
        "p" : 8, #   char[]	bytes
        "P" : 8, #   void *	integer
        "32c": 32,
        "256c": 256,
        "120p": 120
    }

dictTupleLengths = {
    "f": 1,
    "I": 1,
    "i": 1,
    "?": 1,
    "d": 1,
    "8c": 8,
    "4c": 4,
    "32c": 32,
    "120p": 120,
    "256c": 256,
    "49152c": 49152,
    "24576c": 24576
}

dictByteSizes = {
    "f": 4,
    "I": 4,
    "i": 4,
    "?": 1,
    "d": 8,
    "8c": 8,
    "4c": 4,
    "32c": 32,
    "120p": 120,
    "256c": 256,
    "49152c": 49152,
    "24576c": 24576
}

dictMasterAttributes = {
    "Version": "4c",
    "FrameTotal": "I",
    "FrameRate": "I",
    "HighResolution": "?",
    "NumRawBeams": "I",
    "SampleRate": "f",
    "SamplesPerChannel": "I",
    "ReceiverGain": "I",
    "WindowStart": "I",
    "WindowLength": "I",
    "Reverse": "?",
    "SN": "I",
    "Date": "32c",
    "HeaderID": "256c",
    "UserID1": "i",
    "UserID2": "i",
    "UserID3": "i",
    "UserID4": "i",
    "StartFrame":"I",
    "EndFrame": "I",
    "TimeLapse": "?",
    "RecordInterval": "I",
    "RadioSeconds": "i",
    "FrameInterval": "I",
    "Flags": "I",
    "AuxFlags": "I",
    "Sspd": "I",
    "3DFlags": "I"
    #"RsvdData": "120p"
}

dictFrameAttributes = {
    "FrameNumber": "I", 
    "FrameTime": "8c",
    "Version": "I",
    "Status": "I",
    "Year": "I",
    "Month": "I",
    "Day": "I",
    "Hour": "I",
    "Minute": "I",
    "Second": "I",
    "H Second": "I",
    "Transmit Mode": "I",
    "Window Start": "I",
    "Window Length": "I",
    "Threshhold": "I",
    "Intensity": "I",
    "Receiver Gain": "I",
    "Power Supply Temp C": "I",
    "A/D Temp C": "I",
    "Humidity": "I",
    "Focus": "I",
    "Battery": "I",
    "User Value 1": "f",
    "User Value 2": "f",
    "User Value 3": "f",
    "User Value 4": "f",
    "User Value 5": "f",
    "User Value 6": "f",
    "User Value 7": "f",
    "User Value 8": "f",
    "Velocity": "f",
    "Depth": "f",
    "Altitude": "f",
    "Pitch": "f",
    "Pitch Rate": "f",
    "Roll": "f",
    "Roll Rate": "f", 
    "Heading": "f",
    "Heading Rate": "f",
    "Compass Heading": "f",
    "Compass Pitch": "f",
    "Compass Roll": "f",
    "Latitude": "d",
    "Longitude": "d",
    "Sonar Position": "f",
    "Config Flags": "I",
    "Beam Tilt": "f",
    "Target Range": "f",
    "Target Bearing": "f",
    "Target Present": "?",
    "Firmware Revision": "I",
    "Flags": "I",
    "Source Frame": "I",
    "Water Temp": "f",
    "Timer Period": "I",
    "Sonar X": "f",
    "Sonar Y": "f",
    "Sonar Z": "f",
    "Sonar Pan": "f",
    "Sonar Tilt": "f",
    "Sonar Roll": "f",
    "Data LF": "24576c",
    "Data HF": "49152c"
}


# Recursively gets a list of all files, their sub directories, and their
# attributes in the given directory tree 
def vRunFullTest():
    
    #allSQLFiles = getListOfFiles('C:\\Users\\Nicholas.Shaffer\\Desktop')
    #didsonTestFiles = getListOfFiles('Z:\\Habitat\\Data\\UHSI\\DIDSON\\2014\\UHSI_2014_DIDSON_AFSC')

    # Read file tree.
    print('Beginning read through directory tree.', datetime.datetime.now())

    allDidsonFiles = getListOfFiles('Z:\\Habitat\\Data\\UHSI\\DIDSON')
    #allDidsonFiles = getListOfFiles('Z:\\Habitat\\Data\\UHSI\\DIDSON\\2014\\UHSI_2014_DIDSON_AFSC\\UHSI.DIDSON.AFSC.August.07')
    print('Fininshed read through directory tree.', datetime.datetime.now())

    # Write info to csv file
    try:
        with open("C:\\Users\\Nicholas.Shaffer\\Desktop\\DIDSON Stuff\\DidsonAttributes.csv",
                "w+", newline = '') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=',')
            csvWriter.writerow(['File Name', 'File Type', 'DateTime Modified', 'DateTime From Name', 'Location', 
                'Full Path', 'Version', 'Frame Total', 'Frame Rate', 'High Resolution', 'Num Raw Beams', 
                'Sample Rate', 'Samples Per Channel', 'Receiver Gain',  'Window Start', 'Window Length', 
                'Reverse', 'Sonar Serial Number', 'Date', 'HeaderID', 'UserID1', 'UserID2', 'UserID3', 'UserID4',
                'Start Frame', 'End Frame', 'Time Lapse', 'Record Interval', 'Frame Interval', 'Flags', 'Aux Flags',
                'Sound Velocity in Water', '3D Flags', 'Rsvd Data'])
            csvWriter.writerows(allDidsonFiles)

        print('Successfully saved as CSV.')
            
    except PermissionError:
        print("Permission error.")

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfItems = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for item in listOfItems:
        # Create full path
        fullPath = os.path.join(dirName, item)
        # If item is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if os.path.getsize(fullPath) > 200000:
                try:
                    lstFileAttributes = lstGetFileAttributes(fullPath)
                    lstMasterAttributes = lstGetDidsonMasterHeader(fullPath)
                    lstAllAttributes = lstFileAttributes + lstMasterAttributes
                    lstAllAttributes = [[lstAllAttributes[j][i] for j in range(len(lstAllAttributes))] for i in range(len(lstAllAttributes[0]))]
                    allFiles.append(lstAllAttributes[1])
                except:
                    print(fullPath)
    return allFiles

def lstTranspose(lstInput):
    return [[lstInput[j][i] for j in range(len(lstInput))] for i in range(len(lstInput[0]))]

def lstGetFileAttributes(FullFilePath):
    #Get seconds since last updated
    SecSinceModified = os.path.getmtime(FullFilePath)
    #Convert to time object
    TimeModified = time.localtime(SecSinceModified)
    #Convert to readable string
    DateTimeModified = time.strftime('%Y-%m-%dT%H:%M:%SZ', TimeModified)
    #Separate file name and type
    FileNameAndType = os.path.basename(FullFilePath)
    FileName = os.path.splitext(FileNameAndType)[0]
    FileType = os.path.splitext(FileNameAndType)[1]

    # Search directory string for facility location
    Location = None
    if FullFilePath.find('AK') > 0 or FullFilePath.find('AFSC') > 0:
        Location = 'AK'
    elif FullFilePath.find('NW') > 0 or FullFilePath.find('NWFSC') > 0:
        Location = 'NW'
    elif FullFilePath.find('SE') > 0 or FullFilePath.find('SEFSC') > 0:
        Location = 'SE'
                
    # Get timestamp from the file name, if applicable
    TimeFromFileName = None
    if len(FileName) == 20 or len(FileName) == 25:
        TimeFromFileName = FileName[0:10] + 'T' + FileName[11:13] + ':' + FileName[13:15] + ':' + FileName[15:17] + "Z"
    else:
        TimeFromFileName = 'N/A'

    lstAttributes = list()
    lstAttributes.append(["FileName", FileName])
    lstAttributes.append(["FileType", FileType])
    lstAttributes.append(["DateTimeModified", DateTimeModified])
    lstAttributes.append(["TimeFromFileName", TimeFromFileName])
    lstAttributes.append(["Location", Location])
    lstAttributes.append(["FullFilePath", FullFilePath])

    return lstAttributes

def lstGetDidsonMasterHeader(FullFilePath):
    #Open file to read header information in the first 512 bytes
    lstAttributes = list()
    lstNames = list()
    strFormat = ''

    with open(FullFilePath, mode='rb') as didsonFile:
        fileContent = didsonFile.read(512)

        for i in dictMasterAttributes:
            strFormat += dictMasterAttributes[i]
    
        byBuffer = struct.calcsize(strFormat)

        tupAllAttributes = struct.unpack(strFormat, fileContent[0:byBuffer])
        iTupleCount = 0

        for Attribute in dictMasterAttributes:
            strType = dictMasterAttributes[Attribute]
            iTupleSize = dictTupleLengths[strType]
            Value = None

            if iTupleSize == 1: 
                Value = tupAllAttributes[iTupleCount]
            elif Attribute == 'Date' or Attribute == 'HeaderID':
                 PlaceHolder = 0
            else:
                Value = b''
                for j in range(iTupleCount, iTupleCount + iTupleSize):
                    Value += tupAllAttributes[j]
                Value = Value.decode()
            iTupleCount += iTupleSize
            lstAttributes.append([Attribute, Value])

    return lstAttributes
        
def lstGetAllDidsonFrames(FullFilePath, iFrameTotal, strDataType, strDictIgnore):
    lstFrames = list()

    with open(FullFilePath, mode='rb') as didsonFile:
        fileContent = didsonFile.read()
        strFormat = ''
        lstNames = list()
        iFrameStartByte = 512
        iCurrentByte = 512

        for i in dictFrameAttributes:
            if i != strDictIgnore:
                strFormat += dictFrameAttributes[i]
                lstNames.append(i)

        lstFrames.append(lstNames)
        #iFrameSize = dictFrameAttributes[strDataType]["Size"] + 256
        iFrameSize = struct.calcsize(strFormat)

        for _ in range(iFrameTotal+1):
            tupFrameAttributes = struct.unpack(strFormat, fileContent[iFrameStartByte: iFrameStartByte + iFrameSize])
            iTupleCount = 0
            lstAttributes = list()

            for Attribute in dictFrameAttributes:
                if Attribute != strDictIgnore:
                    strType = dictFrameAttributes[Attribute]
                    iTupleSize = dictTupleLengths[strType]
                    iByteSize = dictByteSizes[strType]
                    Value = None

                    if iTupleSize == 1: 
                        Value = tupFrameAttributes[iTupleCount]
                    # else:
                    #     Value = b''
                    #     for j in range(iTupleCount, iTupleCount + iTupleSize):
                    #         Value += tupFrameAttributes[j]
                    #     Value = Value.decode()

                    bCurrentBytes = fileContent[iCurrentByte: iCurrentByte + iByteSize]
                    iCurrentByte += iByteSize
                    iTupleCount += iTupleSize
                    lstAttributes.append([Attribute, Value])

            lstAttributes = lstTranspose(lstAttributes)
            lstFrames.append(lstAttributes[1])
            iFrameStartByte += iFrameSize

    return lstFrames



# Current test files
#strFile = "Z:\\Habitat\\Data\\UHSI\\DIDSON\\2014\\UHSI_DIDSON_NWFSC\\UHSI.DIDSON.NWFSC.August.11.07\\2014-08-09_210855_HF_S001.ddf"
#strFile = "Z:\\Habitat\\Data\\UHSI\\DIDSON\\2015\\UHSI.DIDSON.2015.NW\\UHSI.2015.Station.07\\102\\2015-08-04_#195.ddf"
strFile = "C:\\Users\\Nicholas.Shaffer\\Desktop\\2016-10-29_183900_SyncOut.ddf"


test = lstGetDidsonMasterHeader(strFile)
test = lstGetAllDidsonFrames(strFile, 719, 'Data HF', 'Data LF')
print('DONE.')








# TODO lstGetAllDidsonFrames is unfinished. Still has issues. Needs finalizing/testing. Compare raw bytes to string. 
# TODO add better/more comments for documentation



