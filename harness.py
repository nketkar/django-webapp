from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from geokey import encoder

keyDict = {'public': [0, 1, 2, 3, 4, 5, 6, 7]}
lookupFilename = "./geokey/Lookup.csv"
lookupNFilename = "./geokey/NLookup.csv"


def is_valid(num, rmin, rmax):
    try:
        x = float(num)
        if x >= rmin and x <= rmax:
            return True
        else:
            return False
    except ValueError:
        return False


class BaseGeoKeyView(APIView):

    renderer_classes = [JSONRenderer]

    def __init__(self, **kwargs):
        encoder.initialize(lookupFilename, lookupNFilename)
        self.gc = encoder.GeoCoder("Google")
        super(BaseGeoKeyView, self).__init__(**kwargs)


class EncodeAddressView(BaseGeoKeyView):

    def encodeGeoKeyFromAddress(self, address, keyset=None):
        # error out if the address is not present
        if address is None:
            response = {"Status": "Failure", "Failure Mode": "A valid address must be present."}
            return Response(response, status=400)

        # error out if key set is not valid
        if keyset is not None:
            if keyset.lower() != "public" and keyset.lower() not in keyDict.keys():
                response = {"Status": "Failure", "Failure Mode": "A valid keyset must be set beforehand."}
                return Response(response, status=400)
        else:
            keyset = "public"

        lat, lon = self.gc.geocode_address(address)

        if lat is None or lon is None:
            response = {"Status": "Failure", "Failure Mode": "Error in Geocoding the address."}
            return Response(response, status=400)
        else:
            latCode1, latCode2, lonCode1, lonCode2 = encoder.encode(lat, lon, keyDict[keyset])
            is_valid_values = all([latCode1, latCode2, lonCode1, lonCode2])
            if is_valid_values:
                s = latCode1 + ' ' + latCode2 + ' ' + lonCode1 + ' ' + lonCode2
                response = {"GeoKey": s, "Latitude": lat, "Longitude": lon}
                return Response(response)
            else:
                response = {"Status": "Failure", "Failure Mode": "Error in EasyLocating the address."}
                return Response(response, status=400)

    def get(self, *args, **kwargs):
        address = self.request.GET.get('address')
        keyset = self.request.GET.get('keyset')

        return self.encodeGeoKeyFromAddress(address, keyset)


class DecodeView(BaseGeoKeyView):

    def decodeGeoKey(self, geokey, keyset=None):
        if geokey is None:
            response = {"Status": "Failure", "Failure Mode": "Geokey must be present."}
            return Response(response, status=400)

        if keyset is not None:
            if keyset.lower() != "public" and keyset.lower() not in keyDict.keys():
                response = {"Status": "Failure", "Failure Mode": "A valid keyset must be set beforehand."}
                return Response(response, status=400)
        else:
            keyset = "public"

        isEasyLocate, listOfTokens = encoder.isEasyLocateCode(geokey)
        if isEasyLocate:
            latCode1, latCode2, lonCode1, lonCode2 = listOfTokens
            floatLat, floatLon = encoder.decode(latCode1, latCode2, lonCode1, lonCode2, keyDict[keyset])

            if floatLat is None or floatLon is None:
                response = {"Status": "Failure", "Failure Mode": "Error in decoding the GoeKey."}
                return Response(response, status=400)
            else:
                try:
                    reversedAddress = self.gc.reverse_geocode(floatLat, floatLon)
                    # self.easyLocateText.SetValue(reversedAddress)
                    response = {"Latitude": floatLat, "Longitude": floatLon, "Reversed Address": reversedAddress}
                    return Response(response)
                except Exception:
                    response = {"Status": "Failure", "Failure Mode": "Error in reverse Geocoding Lat/Long."}
                    return Response(response, status=400)
        else:
            response = {"Status": "Failure", "Failure Mode": "Invalid or unrecognizable geokey."}
            return Response(response, status=400)

    def get(self, *args, **kwargs):
        geokey = self.request.GET.get('geokey')
        keyset = self.request.GET.get('keyset')

        return self.decodeGeoKey(geokey, keyset)


#class EncodePositionView(BaseGeoKeyView):

#    def encodeGeoKeyFromPosition(self, lat, lon, keyset=None):
#        lat, lon = float(lat), float(lon)
#        if lat is None or lon is None:
#            response = {"Status": "Failure", "Failure Mode": "Latitude and Longitude must be present."}
#            return Response(response, status=400)

#        if not is_valid(lat, -90, 90):
#            response = {"Status": "Failure", "Failure Mode": "The latitude value must be between -90 and 90."}
#            return Response(response, status=400)

#        if not is_valid(lon, -180, 180):
#            response = {"Status": "Failure", "Failure Mode": "The longitude value must be between -180 and 180."}
#            return Response(response, status=400)

#        if keyset is not None:
#            if keyset.lower() != "public" and keyset.lower() not in keyDict.keys():
#                response = {"Status": "Failure", "Failure Mode": "A valid keyset must be set beforehand."}
#                return Response(response, status=400)
#        else:
#            keyset = "public"
#
#        latCode1, latCode2, lonCode1, lonCode2 = encoder.encode(lat, lon, keyDict[keyset])

#        is_valid_values = all([latCode1, latCode2, lonCode1, lonCode2])
#        if is_valid_values:
#            s = latCode1 + ' ' + latCode2 + ' ' + lonCode1 + ' ' + lonCode2
#            response = {"GeoKey": s, "Latitude": lat, "Longitude": lon}
#            return Response(response)
#        else:
#            response = {"Status": "Failure", "Failure Mode": "Error in EasyLocating the address."}
#            return Response(response, status=400)

#    def get(self, *args, **kwargs):
#        lat = self.request.GET.get('lat')
#        lon = self.request.GET.get('lon')
#        keyset = self.request.GET.get('keyset')
#
#        return self.encodeGeoKeyFromPosition(lat, lon, keyset)

class EncodePositionView(BaseGeoKeyView):

    def encodeGeoKeyFromPosition(self, lat, lon, keyset="public"):
        # Check if lat and lon are provided
        if lat is None or lon is None:
            response = {"Status": "Failure", "Failure Mode": "Latitude and Longitude must be present."}
            return Response(response, status=400)

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            response = {"Status": "Failure", "Failure Mode": "Latitude and Longitude must be valid numbers."}
            return Response(response, status=400)

        if not is_valid(lat, -90, 90) or not is_valid(lon, -180, 180):
            response = {"Status": "Failure", "Failure Mode": "Latitude must be between -90 and 90, and longitude must be between -180 and 180."}
            return Response(response, status=400)

        keyset = keyset.lower()

        if keyset != "public" and keyset not in keyDict:
            response = {"Status": "Failure", "Failure Mode": "A valid keyset must be set beforehand."}
            return Response(response, status=400)

        latCode1, latCode2, lonCode1, lonCode2 = encoder.encode(lat, lon, keyDict[keyset])

        if None in [latCode1, latCode2, lonCode1, lonCode2]:
            response = {"Status": "Failure", "Failure Mode": "Error in EasyLocating the address."}
            return Response(response, status=400)

        s = latCode1 + ' ' + latCode2 + ' ' + lonCode1 + ' ' + lonCode2
        response = {"GeoKey": s, "Latitude": lat, "Longitude": lon}
        return Response(response)

    def get(self, *args, **kwargs):
        lat = self.request.GET.get('lat')
        lon = self.request.GET.get('lon')
        keyset = self.request.GET.get('keyset', "public")

        return self.encodeGeoKeyFromPosition(lat, lon, keyset)


#class PrivateKeyset(BaseGeoKeyView):

#    def handleLookupMode(self, lookup_mode):
#        if lookup_mode.lower() != "public" and lookup_mode.lower() not in keyDict.keys():
            # generate new key since the lookupMode does not exist in the dict
#            keyDict[lookup_mode.lower()] = encoder.generateKey()
#        return {'mode': lookup_mode.lower()}

#    def setPrivateKeyset(self, keysetID):

#        if keysetID is None:
#            response = {"Status": "Failure", "Failure Mode": "KeysetID must be present."}
#            return Response(response, status=400)
#        else:
#            keysetID = keysetID.lower()

#        if keysetID == "public":
#            response = {"Status": "Failure", "Failure Mode": "KeysetID value of public is reserved.  Use another value."}
#            return Response(response, status=400)
#        elif keysetID == "":
#            response = {"Status": "Failure", "Failure Mode": "KeysetID value of blank cannot be used."}
#            return Response(response, status=400)
#        elif keysetID in keyDict.keys():
#            response = {"Status": "Failure", "Failure Mode": "KeysetID is already in use.  Use another keysetID."}
#            return Response(response, status=400)
#        else:
#            response = self.handleLookupMode(keysetID)
#            return Response(response)

#     def get(self, *args, **kwargs):
#        clientKey = self.request.GET.get('clientkey')

#        return self.setPrivateKeyset(clientKey)


class PrivateKeyset(BaseGeoKeyView):

    def handleLookupMode(self, lookup_mode):
        if lookup_mode.lower() != "public" and lookup_mode.lower() not in keyDict.keys():
            # generate new key since the lookupMode does not exist in the dict
            keyDict[lookup_mode.lower()] = encoder.generateKey()
        return {'mode': lookup_mode.lower()}

    def setPrivateKeyset(self, keysetID):
        if keysetID is None:
            response = {"Status": "Failure", "Failure Mode": "KeysetID must be present."}
            return Response(response, status=400)
        else:
            keysetID = keysetID.lower()

        if keysetID == "public":
            response = {"Status": "Failure", "Failure Mode": "KeysetID value of public is reserved.  Use another value."}
            return Response(response, status=400)
        elif keysetID == "":
            response = {"Status": "Failure", "Failure Mode": "KeysetID value of blank cannot be used."}
            return Response(response, status=400)
        elif keysetID in keyDict.keys():
            response = {"Status": "Failure", "Failure Mode": "KeysetID is already in use.  Use another keysetID."}
            return Response(response, status=400)
        else:
            response = self.handleLookupMode(keysetID)
            return Response(response)

#    def get(self, *args, **kwargs):
    def get(self, *args, **kwargs):
        clientKey = self.request.GET.get('clientkey')

        return self.setPrivateKeyset(clientKey)
        # This method handles the creation of a new private keyseti
        #keysetID = self.request.data.get('keysetID')  # Assuming 'keysetID' is sent in the request body

        #if keysetID is None:
        #    response = {"Status": "Failure", "Failure Mode": "KeysetID must be present in the request body."}
        #    return Response(response, status=400)

        #return self.setPrivateKeyset(keysetID)


