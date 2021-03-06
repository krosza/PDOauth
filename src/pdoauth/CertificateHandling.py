#pylint: disable=no-member
from pdoauth.models.Credential import Credential
import urlparse
from pdoauth.ReportedError import ReportedError
from pdoauth.CredentialManager import CredentialManager
from pdoauth.CryptoUtils import CryptoUtils

class CertificateHandling(CryptoUtils):
    def addCertCredentialToUser(self, cert, user):
        identifier, digest = self.parseCert(cert)
        Credential.new(user, "certificate", identifier, digest)

    def registerAndLoginCertUser(self, email, cert):
        cred = self.loginOrRegisterCertUser(cert, [email])
        self.loginUser(cred)

    def extractCertFromForm(self, form):
        spkacInput = form.pubkey.data
        email = form.email.data
        if email is not None:
            commonName = email
        else:
            commonName = "someone"
        certObj = self.createCertFromSPKAC(spkacInput, commonName, email)
        certAsPem = certObj.as_pem()
        return certAsPem, certObj

    def createCertResponse(self, certObj):
        resp = self.make_response(certObj.as_der(), 200)
        resp.headers["Content-Type"] = "application/x-x509-user-cert"
        self.setCSRFCookie(resp)
        return resp

    def doKeygen(self, form):
        email = form.email.data
        certAsPem, certObj = self.extractCertFromForm(form)
        user = self.getCurrentUser()
        if user.is_authenticated():
            self.addCertCredentialToUser(certAsPem, user)
        else:
            self.registerAndLoginCertUser(email, certAsPem)
        return self.createCertResponse(certObj)

    def getEmailFromQueryParameters(self):
        requestUrl = self.getRequestUrl()
        parsed = urlparse.urlparse(requestUrl)
        email = urlparse.parse_qs(parsed.query).get('email', None)
        return email


    def registerCertUser(self, email, identifier, digest, cred):
        if email is None:
            raise ReportedError(["You have to register first"], 403)
        theEmail = email[0]
        CredentialManager.create_user_with_creds("certificate", identifier, digest, theEmail)
        cred = Credential.get("certificate", identifier)
        self.sendPasswordVerificationEmail(cred.user)
        return cred

    def loginOrRegisterCertUser(self, cert, email):
        if cert is None or cert == '':
            raise ReportedError(["No certificate given"], 403)
        identifier, digest = self.parseCert(cert)
        cred = Credential.get("certificate", identifier)
        if cred is None:
            cred = self.registerCertUser(email, identifier, digest, cred)
        cred.user.activate()
        return cred

    def doSslLogin(self):
        cert = self.getEnvironmentVariable('SSL_CLIENT_CERT')
        email = self.getEmailFromQueryParameters()
        cred = self.loginOrRegisterCertUser(cert, email)
        resp = self.finishLogin(cred)
        resp.headers['Access-Control-Allow-Origin']="*"
        return resp
