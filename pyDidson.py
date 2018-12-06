import codecs
import struct
import os
import time
import csv
import datetime

# Current test files
strFile = "Z:\\Habitat\\Data\\UHSI\\DIDSON\\2014\\UHSI_DIDSON_NWFSC\\UHSI.DIDSON.NWFSC.August.11.07\\2014-08-09_210855_HF_S001.ddf"
strFile = "Z:\\Habitat\\Data\\UHSI\\DIDSON\\2015\\UHSI.DIDSON.2015.NW\\UHSI.2015.Station.07\\102\\2015-08-04_#195.ddf"
strFile = "C:\\Users\\Nicholas.Shaffer\\Desktop\\2016-10-29_183900_SyncOut.ddf"

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

dictFrameAttributes = {
    "FrameNumber": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    }, 
    "FrameTime": {
        "Type": "8c",
        "Size" : 8,
        "Value" : None
    },
    "Version": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Status": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Year": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Month": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Day": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Hour": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Minute": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Second": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "H Second": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Transmit Mode": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Window Start": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Window Length": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Threshhold": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Intensity": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Receiver Gain": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Power Supply Temp C": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "A/D Temp C": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Humidity": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Focus": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Battery": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "User Value 1": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 2": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 3": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 4": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 5": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 6": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 7": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "User Value 8": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Velocity": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Depth": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Altitude": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Pitch": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Pitch Rate": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Roll": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Roll Rate": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    }, 
    "Heading": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Heading Rate": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Compass Heading": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Compass Pitch": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Compass Roll": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Latitude": {
        "Type": "d",
        "Size" : 8,
        "Value" : None
    },
    "Longitude": {
        "Type": "d",
        "Size" : 8,
        "Value" : None
    },
    "Sonar Position": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Config Flags": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Beam Tilt": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Target Range": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Target Bearing": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Target Present": {
        "Type": "?",
        "Size" : 1,
        "Value" : None
    },
    "Firmware Revision": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Flags": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Source Frame": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Water Temp": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Timer Period": {
        "Type": "I",
        "Size" : 4,
        "Value" : None
    },
    "Sonar X": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Sonar Y": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Sonar Z": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Sonar Pan": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Sonar Tilt": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Sonar Roll": {
        "Type": "f",
        "Size" : 4,
        "Value" : None
    },
    "Data LF": {
        "Type": "24576c",
        "Size" : 24576,
        "Value" : None
    },
    "Data HF": {
        "Type": "49152c",
        "Size" : 49152,
        "Value" : None
    }
}

dictTupleLengths = {
    "f": 1,
    "I": 1,
    "i": 1,
    "?": 1,
    "d": 1,
    "8c": 8,
    "4c": 4,
    "256c": 256,
    "49152c": 49152,
    "24576c": 24576
}

dictMasterAttributes = {
    "Version": {
        "Type": "4c",
        "Size" : 4,
        "Value" : None
    },
    "FrameTotal": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "FrameRate": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "HighResolution": {
        "Type": "?",
        "Size" : 1,
        "Value" : None
    },
    "NumRawBeams": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "SampleRate": {
        "Type": "f",
        "Size" : 1,
        "Value" : None
    },
    "SamplesPerChannel": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "ReceiverGain": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "WindowStart": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "WindowLength": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "Reverse": {
        "Type": "?",
        "Size" : 1,
        "Value" : None
    },
    "SN": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "Date": {
        "Type": "32c",
        "Size" : 32,
        "Value" : None
    },
    "HeaderID": {
        "Type": "256c",
        "Size" : 256,
        "Value" : None
    },
    "UserID1": {
        "Type": "i",
        "Size" : 1,
        "Value" : None
    },
    "UserID2": {
        "Type": "i",
        "Size" : 1,
        "Value" : None
    },
    "UserID3": {
        "Type": "i",
        "Size" : 1,
        "Value" : None
    },
    "UserID4": {
        "Type": "i",
        "Size" : 1,
        "Value" : None
    },
    "StartFrame": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "EndFrame": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "TimeLapse": {
        "Type": "?",
        "Size" : 1,
        "Value" : None
    },
    "RecordInterval": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "RadioSeconds": {
        "Type": "i",
        "Size" : 1,
        "Value" : None
    },
    "FrameInterval": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "Flags": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "AuxFlags": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "Sspd": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    },
    "3DFlags": {
        "Type": "I",
        "Size" : 1,
        "Value" : None
    }
    # "RsvdData": {
    #     "Type": "120p",
    #     "Size" : 120,
    #     "Value" : None
    # }
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
    dictMasterHeader = dictMasterAttributes
    lstAttributes = list()

    with open(FullFilePath, mode='rb') as didsonFile:
        fileContent = didsonFile.read(512)
        tupAllAttributes = struct.unpack('4cII?IfIIII?I32c256ciiiiII?IiIIIII120p', fileContent[0:512])
        iTupleCount = 0

        for Attribute in dictMasterHeader:
            iTupleSize = dictMasterHeader[Attribute]["Size"]
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
                strFormat += dictFrameAttributes[i]["Type"]
                lstNames.append(i)

        lstFrames.append(lstNames)
        #iFrameSize = dictFrameAttributes[strDataType]["Size"] + 256
        iFrameSize = struct.calcsize(strFormat)

        for i in range(iFrameTotal+1):
            tupFrameAttributes = struct.unpack(strFormat, fileContent[iFrameStartByte: iFrameStartByte + iFrameSize])
            iTupleCount = 0
            lstAttributes = list()
            for Attribute in dictFrameAttributes:
                if Attribute != strDictIgnore:
                    strType = dictFrameAttributes[Attribute]["Type"]
                    iTupleSize = dictTupleLengths[strType]
                    Value = None
                    iSize = dictFrameAttributes[Attribute]["Size"]

                    if iTupleSize == 1: 
                        Value = tupFrameAttributes[iTupleCount]
                    # else:
                    #     Value = b''
                    #     for j in range(iTupleCount, iTupleCount + iTupleSize):
                    #         Value += tupFrameAttributes[j]
                    #     Value = Value.decode()

                    bCurrentBytes = fileContent[iCurrentByte: iCurrentByte + iSize]
                    iCurrentByte += iSize
                    iTupleCount += iTupleSize
                    lstAttributes.append([Attribute, Value])

            lstAttributes = lstTranspose(lstAttributes)
            lstFrames.append(lstAttributes[1])
            iFrameStartByte += iFrameSize

    return lstFrames


#test = lstDidsonMasterHeader(strFile)
test = lstGetAllDidsonFrames(strFile, 719, 'Data HF', 'Data LF')
print('DONE.')








# TODO edit dictMasterHeader/Size, reference dictTupleLengths instead in lstGetDidsonMasterHeader
# TODO edit lstGetDidsonMasterHeader size, get size instead of hardcoding, for standardizing
# TODO lstGetAllDidsonFrames is unfinished. Needs finalizing/testing. Compare raw bytes to string. 
# TODO add better/more comments for documentation



