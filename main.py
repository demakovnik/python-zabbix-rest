import base64, argparse, os, util, errno, functools, operator


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Get statistics from Zabbix Server')
  parser.add_argument('-l','--login', required=True,type=str,help='Zabbix API User')
  parser.add_argument('-p','--password', required=True,type=str,help='Zabbix API Password')
  parser.add_argument('-e','--encoded', default='True', required=False,type=str,help='Use encoded password')
  parser.add_argument('-u','--url', required=True,type=str,help='Zabbix REST API URL')
  args = parser.parse_args()

  user =  args.__dict__['login']
  password = args.__dict__['password']
  encoded = 'False' if type(args.__dict__['encoded']) == 'NoneType' else args.__dict__['encoded']  

  if args.__dict__['encoded'].lower() in ['true', '1', 'y', 'yes']:
    try:
      base64_bytes = password.encode('ascii')
      message_bytes = base64.b64decode(base64_bytes)
      password = message_bytes.decode('ascii')
    except UnicodeDecodeError:
      print('Incorrect user name or password or account is temporarily blocked.')
        
  url = args.__dict__['url']

  # Получаем токен
  token = util.get_token(url,user,password)

  # Получаем элеметы сервера по токену
  items = util.get_items(url, token, error = '', sortfield='')
  hosts = util.get_hosts(url, token)
  groups = util.get_groups(url, token)

  element_cache_directory = 'element_cache'

  if not os.path.exists(element_cache_directory):
    try:
      os.makedirs(element_cache_directory)
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise

  element_cache_directory = 'element_cache'

  # Получаем элементы данных, хосты, группы с сервера
  with open(os.path.join(element_cache_directory,'items.txt'),'w') as f_obj:
    print(items, file=f_obj)

  with open(os.path.join(element_cache_directory,'hosts.txt'),'w') as f_obj:
    print(hosts, file=f_obj)
  
  with open(os.path.join(element_cache_directory,'groups.txt'),'w') as f_obj:
    print(groups, file=f_obj)


