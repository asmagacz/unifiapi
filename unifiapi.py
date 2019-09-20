import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UniFiAPI:

    def __init__(self, apiUrl, loginData):
        commandUrl = apiUrl + 'api/login'
        self.apiUrl = apiUrl
        self.session = requests.session()
        self.requestToken = self.session.request("POST", commandUrl, verify=False, data=json.dumps(loginData))
        self.token = self.requestToken.cookies.get_dict()['unifises']
        self.session.headers.update({"unifises": self.token})

    def getSites(self):
        commandUrl = self.apiUrl + 'api/self/sites'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getSysInfo(self):
        commandUrl = self.apiUrl + 'api/s/default/stat/sysinfo'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getAllAdmins(self):
        commandUrl = self.apiUrl + 'api/stat/admin'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getDevicesUnderControllerManagement(self, site):
        commandUrl = self.apiUrl + 'api/s/' + site + '/stat/device'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getDeviceBasic(self, site):
        commandUrl = self.apiUrl + 'api/s/' + site + '/stat/device-basic'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getSingleDevice(self, site, mac):
        commandUrl = self.apiUrl + 'api/s/' + site + '/stat/device/' + mac
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getOnlineClientDevices(self):
        commandUrl = self.apiUrl + 'api/s/default/stat/sta'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getHealth(self, site):
        commandUrl = self.apiUrl + 'api/s/' + site + '/stat/health'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getUsers(self):
        commandUrl = self.apiUrl + 'api/s/default/list/user'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getNetworkSettings(self):
        commandUrl = self.apiUrl + 'api/s/default/rest/networkconf'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getPortConfigurations(self):
        commandUrl = self.apiUrl + 'api/s/default/list/portconf'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getAllClientDevicesEverConnected(self):
        commandUrl = self.apiUrl + 'api/s/default/stat/alluser'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def getAllSitesHosted(self):
        commandUrl = self.apiUrl + 'api/stat/sites'
        output = self.session.request("GET", commandUrl, verify=False).json()
        return output

    def __del__(self):
        self.session.close()
