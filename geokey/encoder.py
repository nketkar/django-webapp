import pdb
import sys
import random
import re

DEBUG = 0
USE_RANDOMIZER = 1

MODE = "PUBLIC"
NORMALIZATION_FACTOR = 360
KEYLEN = 8
PUBLIC_KEY = [0, 1, 2, 3, 4, 5, 6, 7]
LATLONG_PRECISION = 5

zLookup = {}
zNLookup = {}
zReverseLookup = {}
zNReverseLookup = {}


lookupFilename = "./Lookup.csv"
lookupNFilename = "./NLookup.csv"

#lookupFilename = "./EasyLocateAPI/geokey/Lookup.csv"


class GeoCoder(object): 

    GOOGLEAPIKEY = "AIzaSyAY-Pl97qQndp0LS9wKahRO9H2CTMjARrA"

    def __init__(self, geoCoderType = ""): 

        if geoCoderType == "Google":
            from geopy.geocoders import GoogleV3
            self.gc = GoogleV3(api_key=self.GOOGLEAPIKEY)
        else: 
            from geopy import Nominatim
            self.gc = Nominatim()

    def geocode_address(self, address_str): 
        try: 
            loc = self.gc.geocode(address_str)
            return round(loc.latitude, LATLONG_PRECISION), \
	           round(loc.longitude, LATLONG_PRECISION)
        except: 
            print "Error in geocoding"
            return None, None

    def reverse_geocode(self, lat, lon): 

        try: 
            loc = self.gc.reverse(str(lat) + ',' + str(lon))
            return loc[0].address
        except: 
            print "Error in reverse geocoding"
            return None, None


def load_file(aryName, reverseAryName, filename): 
    f = open(filename);
    for line in f: 
        num, code = line.split(",")
        aryName[num.zfill(4)] = code[:4]
        reverseAryName[code[:4]] = num.zfill(4)

    f.close()
        

def updateMode(input_str): 
    global MODE

    if input_str.lower() == "public": 
        #NORMALIZATION_FACTOR = 360
        MODE = "PUBLIC"
    elif input_str.lower() == "private": 
        #NORMALIZATION_FACTOR = random.randint(360,999)
        MODE = "PRIVATE"
    else: MODE = "PUBLIC"


def normalizeLat(latInt): 
    return latInt+NORMALIZATION_FACTOR 

def normalizeLon(lonInt): 
    return lonInt+NORMALIZATION_FACTOR 

def denormalizeLat(latInt): 
    return latInt-NORMALIZATION_FACTOR 

def denormalizeLon(lonInt): 
    return lonInt-NORMALIZATION_FACTOR 

def isEasyLocateCode(input_str): 
    p = re.compile("[a-zA-Z-][a-zA-Z-][a-zA-Z-][a-zA-Z-]$")

    l = input_str.split()
    if len(l) == 4: 
        if p.match(l[0])  and p.match(l[1]) and p.match(l[2])  and p.match(l[3]): 
            return True, l

    return False, []

def encode(lat, lon, theKey=PUBLIC_KEY): 
    global MODE
    isLatBetweenZeroAndMinusOne = False
    isLonBetweenZeroAndMinusOne = False

    if lat < 0 and lat > -1: 
        isLatBetweenZeroAndMinusOne = True
        
    if lon < 0 and lon > -1: 
        isLonBetweenZeroAndMinusOne = True


    # convert lat lon into floats
    lat = float(lat)
    lon = float(lon)

    # get the int part
    latInt = int(lat)
    lonInt = int(lon)

    # normalize
    latNew = normalizeLat(latInt)
    lonNew = normalizeLon(lonInt)

    if DEBUG:
        print '\nPrinting normalized lat and long:'
        print latNew
        print lonNew

    # get decimal part of lat and lon
    latDecimal = lat - latInt
    lonDecimal = lon - lonInt

    # round to 5th decimal place
    latDec5 = round(latDecimal, LATLONG_PRECISION)
    lonDec5 = round(lonDecimal, LATLONG_PRECISION)

    if DEBUG: 
        print '\nPrinting rounded decimal part of lat and long:'
        print latDec5
        print lonDec5

    # get cleaned versions
    cleanLat5 = abs(int(latDec5*100000))
    cleanLon5 = abs(int(lonDec5*100000))

    if DEBUG: 
        print '\nPrinting rounded decimal part of lat and long - covering 5 digits:'
        print latDec5
        print lonDec5

    fusedLat = str(latNew)+str(cleanLat5).zfill(LATLONG_PRECISION)
    fusedLon = str(lonNew)+str(cleanLon5).zfill(LATLONG_PRECISION)

    if DEBUG: 
        print '\nPrinting fused lat and long:'
        print fusedLat
        print fusedLon

    if USE_RANDOMIZER: 
        if DEBUG: print "\nUsing Randomizer..."
        print '\nPrinting fused lat and long:'
        # New randomizing algorithm for Change Concrol CR0001
        if int(fusedLat[6]) % 2 != 0:
            latCode1_int = int(fusedLat[:4]) + int(fusedLat[6])
            fusedLat = str(latCode1_int).zfill(4) + fusedLat[4:]
            if DEBUG: print fusedLat

        if int(fusedLon[6]) % 2 != 0: 
            lonCode1_int = int(fusedLon[:4]) + int(fusedLon[6])
            fusedLon = str(lonCode1_int).zfill(4) + fusedLon[4:]
            if DEBUG: print fusedLon

    #if MODE == "PRIVATE": 
    fusedLat = applyForwardKeyTransform(theKey, fusedLat)
    fusedLon = applyForwardKeyTransform(theKey, fusedLon)

    try:
        if isLatBetweenZeroAndMinusOne == True: 
            latCode1 = zNLookup[fusedLat[:4]]
        else: 
            latCode1 = zLookup[fusedLat[:4]]
        latCode2 = zLookup[fusedLat[4:]]

        if isLonBetweenZeroAndMinusOne == True: 
            lonCode1= zNLookup[fusedLon[:4]]
        else: 
            lonCode1= zLookup[fusedLon[:4]]
        lonCode2= zLookup[fusedLon[4:]]
        return latCode1, latCode2, lonCode1, lonCode2
    except:
        print "Error in address encoding.."
        return None, None, None, None




def decode (latCode1, latCode2, lonCode1, lonCode2, theKey=PUBLIC_KEY): 
    global MODE
    latIsNegative = False
    lonIsNegative = False

    try:
        fusedLat = zReverseLookup[latCode1]+zReverseLookup[latCode2]
    except KeyError: 
        fusedLat = zNReverseLookup[latCode1]+zReverseLookup[latCode2]
        latIsNegative = True

    try: 
        fusedLon = zReverseLookup[lonCode1]+zReverseLookup[lonCode2]
    except KeyError: 
        fusedLon = zNReverseLookup[lonCode1]+zReverseLookup[lonCode2]
        lonIsNegative = True
    except:
        print "Error in EasyCode decoding.."
        return None, None


    if DEBUG: 
        print '\nPrinting fused lat and long:'
        print fusedLat
        print fusedLon

    if USE_RANDOMIZER: 
        if DEBUG: print "\nUsing Randomizer..."
        print '\nPrinting fused lat and long:'
        # New randomizing algorithm for Change Concrol CR0001
        if int(fusedLat[6]) % 2 != 0:
            latCode1_int = int(fusedLat[:4]) - int(fusedLat[6])
            fusedLat = str(latCode1_int).zfill(4) + fusedLat[4:]
            if DEBUG: print fusedLat

        if int(fusedLon[6]) % 2 != 0: 
            lonCode1_int = int(fusedLon[:4]) - int(fusedLon[6])
            fusedLon = str(lonCode1_int).zfill(4) + fusedLon[4:]
            if DEBUG: print fusedLon

    #if MODE == 'PRIVATE':
    fusedLat = applyReverseKeyTransform(theKey, fusedLat)
    fusedLon = applyReverseKeyTransform(theKey, fusedLon)

    lat3 = denormalizeLat(int(fusedLat[:3]))
    lat5 = float(fusedLat[3:])/100000.0
    if lat3 < 0: 
       floatLat = (abs(lat3) + lat5) * -1.0
    else: 
        floatLat = lat3 + lat5

    lon3 = denormalizeLon(int(fusedLon[:3]))
    lon5 = float(fusedLon[3:])/100000.0
    if lon3 < 0: 
       floatLon = (abs(lon3) + lon5) * -1.0
    else: 
        floatLon = lon3 + lon5

    if latIsNegative: 
        floatLat = floatLat * (-1)
    if lonIsNegative: 
        floatLon = floatLon * (-1)
    return floatLat, floatLon


def generateKey():
    keyChars = []
    numKeyChars = 0

    while(True):
        if numKeyChars == KEYLEN: break
        i = random.randint(0,7)
        if i not in keyChars:
            keyChars.append(i)
            numKeyChars = numKeyChars + 1
        else: continue


    return keyChars

def applyForwardKeyTransform(key, s):
    global KEYLEN

    if len(s) != 8:
        print "Internal Error: The value to encrypt must be 8 characters in length\n"
        return ""

    i=0
    enc_s = (s + '.') [:-1]
    enc_l = list(enc_s)
    while(i < KEYLEN):
        enc_l[key[i]] = s[i]
        i = i + 1

    return ''.join(enc_l)

def applyReverseKeyTransform(key, s):
    global KEYLEN

    if len(s) != 8:
        print "Internal Error: The value to encrypt must be 8 characters in length\n"
        return ""

    i=0
    enc_s = (s + '.') [:-1]
    enc_l = list(enc_s)
    while(i < KEYLEN):
        enc_l[i] = s[key[i]]
        i = i + 1

    return ''.join(enc_l)


def initialize(lookupFilename, lookupNFilename):
    global MODE
    global NORMALIZATION_FACTOR
    global zLookup
    global zNLookup 
    global zReverseLookup 
    global zNReverseLookup 

    # load the lookup table
    load_file(zLookup, zReverseLookup, lookupFilename)
    load_file(zNLookup, zNReverseLookup, lookupNFilename)


# main line code
if __name__ == "__main__": 
    initialize(lookupFilename, lookupNFilename)
    gc = GeoCoder("Google")

    my_address = ""

    while (1): 
        isEasyLocate = False
        user_input = ""

        user_input = raw_input("\nEnter the address or the EasyLocate code:")
        if user_input.lower() in ["quit", "done"]: sys.exit(1)
        if user_input.lower() in ["public", "private"]: 
            updateMode(user_input)
            continue
    
        isEasyLocate, listOfTokens = isEasyLocateCode(user_input) 
    
        if isEasyLocate: 
            latCode1, latCode2, lonCode1, lonCode2 = listOfTokens
            floatLat, floatLon = decode(latCode1, latCode2, lonCode1, lonCode2, PUBLIC_KEY)

            if floatLat == None or floatLon == None: continue
            print '\nPrinting decoded values:'
            print floatLat
            print floatLon

            reversedAddress = gc.reverse_geocode(floatLat, floatLon)
            print '\nPrinting decoded and reversed geocoded address:'
            print reversedAddress
        

        else: 
            my_address = user_input
            lat, lon = gc.geocode_address(my_address)

            if lat == None or lon == None: continue

            latCode1, latCode2, lonCode1, lonCode2 = encode (lat, lon, PUBLIC_KEY)

            if latCode1 == None or latCode2 == None or lonCode1 == None or lonCode2 == None: continue
            print '\nPrinting encoded values:'
            print latCode1 + ' ' + latCode2 + ' ' + lonCode1 + ' ' + lonCode2

