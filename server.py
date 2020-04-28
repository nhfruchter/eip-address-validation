from flask import Flask, request, jsonify, render_template, abort
from flask_recaptcha import ReCaptcha
from flask_talisman import Talisman

from usps import validateAddress, makeAddressXML, makeUSPSVerifyXML
from xml.etree.ElementTree import tostring

app = Flask(__name__)

csp = {
    'default-src': [
        '\'self\'',
        '*.google.com',
        '*.google-analytics.com',
        '*.gstatic.com',                
        'unpkg.com'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        '*.googletagmanager.com',
        '*.google-analytics.com',
        '*.google.com',
        '*.gstatic.com',                
    ]
}
_t = Talisman(app, content_security_policy=csp) # HTTPS forced

# Configuration - replace with your own keys
app.config['USPS_UID'] = ""
app.config['RECAPTCHA_SITE_KEY'] = ""
app.config['RECAPTCHA_SECRET_KEY'] = ""

recaptcha = ReCaptcha(app=app)

@app.route("/api/format-address", methods=['POST'])
def formatAddress():
    """Internal API endpoint to return a formatted address. Proxies through errors."""
    
    if recaptcha.verify() or app.config.get('testing'):
        if 'addr2' not in request.form:
            result = {'error': "You need at least one address line."}
            return render_template("address.html", result=result, original=request.values)                    
            

        # Make an <Address> element
        formValues = dict(request.values)
        formValues.pop('g-recaptcha-response')
        addr = makeAddressXML(**formValues)

        # XML payload to send to USPS
        payload = makeUSPSVerifyXML(app.config.get("USPS_UID"), addr)

        result = validateAddress(payload)
        if result.get('Error'):
            result = {'error': result['Error'].get('Description')}

        return render_template("address.html", result=result, original=request.values)
        # return jsonify(result)
    else:
        result = {'error': "Please solve the CAPTCHA."}
        return render_template("address.html", result=result, original=request.values)
        

@app.route("/")
def home():
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True)