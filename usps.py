from xml.etree.ElementTree import Element, SubElement, tostring
import requests
import xmltodict

def makeUSPSVerifyXML(userID, addresses):
    """Create <AddressValidateRequest> document for the API containing addresses."""
    
    # Create wrapper element for request with required UID (= the API key)
    request = Element("AddressValidateRequest", USERID=userID)
    
    if isinstance(addresses, Element):
        # Single address request
        request.append(addresses)
        return request
        
    else:   
        # Multiple address request (max 5 can get sent to the API)
        if len(addresses) > 5:
            raise ValueError("Each request can have a maximum of 5 addresses.")
        else:    
            for addr in addresses:
                request.append(addr)
    
    return request    

def makeAddressXML(addr1="", addr2="", city="", state="", zip5="", zip4=""):
    """Create an <Address> element representing one address for the API."""
    
    # Root element for the address
    addr = Element('Address')

    # Create each element
    _addr1 = SubElement(addr, 'Address1') 
    _addr2 = SubElement(addr, 'Address2')
    _city = SubElement(addr, 'City')
    _state = SubElement(addr, 'State')
    _zip5 = SubElement(addr, 'Zip5')
    _zip4 = SubElement(addr, 'Zip4')
    
    # Fill with content
    _addr1.text = addr1
    _addr2.text = addr2
    _city.text = city
    _state.text = state
    _zip5.text = zip5
    _zip4.text = zip4
    
    return addr
    
def parseAddressValidateResponse(rawXML):
    """Parse XML from the USPS validation API into a dict.

    `addr` contains a representation of the full result returned from the USPS, including ZIP+4 
    (addr1, addr2, city, state, zip5, zip4)
    """
    
    result = xmltodict.parse(rawXML)
    addr = result.get('AddressValidateResponse').get('Address')
    
    return addr
    
def validateAddress(requestXML, parsed=True):
    """Take in an <AddressValidateRequest> XML object and return a result from the USPS
    address validation API.
    
    Parses into output for website if `parsed`, else string of XML.
    """
    
    ENDPOINT = "https://secure.shippingapis.com/ShippingAPI.dll"
    params = {
        'API': 'Verify',
        'XML': tostring(requestXML)
    }
    
    r = requests.get(ENDPOINT, params=params)
    if parsed: 
        return parseAddressValidateResponse(r.text)
    else:
        return r.text    
    
    
    