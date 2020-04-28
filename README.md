A site that consumes the USPS Web Tools API for address validation and returns a formatted address
line that is more likely to be properly read by the IRS stimulus tracker website.

`usps.py` is a standalone API client for the USPS Web Tools API's `Verify` endpoint.

Usage:

    from usps import *
    
    # Format an address object
    myAddress = makeAddressXML(addr2="123 Main St", city="Anytown", state="ZZ")
    
    # Make the API payload
    payload = makeUSPSVerifyXML("UID_HERE", myAddress)
    
    # Get result
    print( validateAddress(payload) )