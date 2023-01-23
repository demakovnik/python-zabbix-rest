import constants, requests

def get_token(url, user, password):
  constants.auth_json['params']['user'] = user
  constants.auth_json['params']['password'] = password
  response = requests.post(url, json = constants.auth_json).json()
  if "error" in response:
    raise Exception(response['error']['data'])
  return response['result']

def get_items(url, token, hostid='', error ='', sortfield =''):
  constants.items_json['auth'] = token
  constants.items_json['params']['search']['hostid'] = hostid
  constants.items_json['params']['search']['error'] = error
  constants.items_json['params']['sortfield'] = sortfield
  return requests.post(url, json = constants.items_json).json()['result']

def get_hosts(url, token):
  constants.hosts_json['auth'] = token
  return requests.post(url, json = constants.hosts_json).json()['result']

def get_groups(url, token):
  constants.groups_json['auth'] = token
  return requests.post(url, json = constants.groups_json).json()['result']