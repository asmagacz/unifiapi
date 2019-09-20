import unifiapi
import json
import argparse


def unifisession(user, passw, apiUrl):
    loginData = {
        "username": user,
        "password": passw
    }
    try:
        test = unifiapi.UniFiAPI(apiUrl, loginData)
    except ConnectionError:
        print("Nie udalo sie nawiazac polaczenia")
    return test


def discoverSite(session):
    sites = []
    for site in session.getSites()['data']:
        sites.append({"{#NAME}": site['name'], "{#DESC}": site['desc']})
    output = json.dumps({'data': sites}, indent=4)
    return output


def discoverAll(session):
    sites = []
    for site in session.getSites()['data']:
        for device in session.getDeviceBasic(site['name'])['data']:
            sites.append({
                "desc": site['desc'],
                "device": device['mac']
            })
    output = json.dumps({'data': sites}, indent=4)
    return output


def getApName(session):
    data = []
    apDetails = []
    for site in session.getSites()['data']:
        for device in session.getDeviceBasic(site['name'])['data']:
            data.append(session.getSingleDevice(site['name'], device['mac'])['data'])
    for items in data:
        for items in items:
            apDetails.append({
                "{#APNAME}": items['name']
            })
    output = json.dumps({'data': apDetails}, indent=4)
    return output


def getApDetails(parameter, apname, session):
    data = []
    for site in session.getSites()['data']:
        for device in session.getDeviceBasic(site['name'])['data']:
            data.append(session.getSingleDevice(site['name'], device['mac'])['data'])
    for items in data:
        for items in items:
            if items['name'] == apname:
                return items[parameter]


def healthPerSite(sitedesc, subsystem, parameter, session):
    for site in session.getSites()['data']:
        if site['desc'] == sitedesc:
            for item in session.getHealth(site['name'])['data']:
                if item['subsystem'] == subsystem:
                    if parameter == 'num_adopted':
                        print(item["num_adopted"])
                    elif parameter == 'num_disconnected':
                        print(item["num_disconnected"])
                break


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--sitedesc', help='site description')
    parser.add_argument('-sm', '--subsystem', help='subsystem')
    parser.add_argument('-p', '--parameter', help='parameter')
    parser.add_argument('-m', '--method', help='method name to call')
    parser.add_argument('-ap', '--apname', help='access point name')
    parser.add_argument('-un', '--username', help='username')
    parser.add_argument('-ps', '--password', help='password')
    parser.add_argument('-url', '--apiurl', help='api url')
    args = parser.parse_args()

    sitedesc = str(args.sitedesc).strip()
    subsystem = str(args.subsystem).strip()
    parameter = str(args.parameter).strip()
    method = str(args.method).strip()
    apname = str(args.apname).strip()
    username = str(args.username).strip()
    password = str(args.password).strip()
    apiurl = str(args.apiurl).strip()

    session = unifisession(username, password, apiurl)

    while switch(method):
        if case('sitehealth'):
            healthPerSite(sitedesc, subsystem, parameter, session)
            break
        if case('discoverall'):
            print(discoverAll(session))
            break
        if case('discoversite'):
            print(discoverSite(session))
            break
        if case('getapdetails'):
            print(getApDetails(parameter, apname, session))
            break
        if case('getapname'):
            print(getApName(session))
            break

        print('To run script use command: '
              'python <scriptname.py> --method<method to call> -parameter<method argument>'
              '\nAvailable parameters: '
              '\n-m, --method, help= method name to call'
              '\n-sd, --sitedesc, help= site description'
              '\n-sm, --subsystem, help= subsytem name'
              '\n-p, --parameter, help= parameter'
              '\n-ap, --apname, help= access point name'
              '\n-un, --username, help= username'
              '\n-ps, --password, help= password'
              '\n-url, --apiurl, help= api url'
              '\nTo call method use:'
              '\n\tpython ufapi.py -m sitehealth -sd BTH -sm wlan -p num_adopted '
              '\t\t-un username -ps password -url https://url/'
              '\n\tpython ufapi.py -m discoverall -un username -ps password -url https://url/'
              '\n\tpython ufapi.py -m discoversite -un username -ps password -url https://url/'
              '\n\tpython ufapi.py -m getapdetails -p num_sta -ap apname -un username '
              '\t\t-ps password -url https://url/'
              '\n\tpython ufapi.py -m getapname -un username -ps password -url https://url/')
        break

    session.__del__()


