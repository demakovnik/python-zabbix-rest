import base64, argparse, os, util, errno, functools, itertools
from prettytable import PrettyTable

def adder(x, y):
  x = dict(x)
  key = y['hostid']
  if key in x:
    li = list(x[key])
    li.append(y)
    x[key] = li
  else:
    li = []
    li.append(y)
    x[key] = li
  return x

def make_directory_if_not_exists(directory):
  if not os.path.exists(directory):
    try:
      os.makedirs(directory)
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise

def get_hostnames(hosts):
  def adder(x, y):
    x = dict(x)
    x[y['hostid']]=y['name']
    return x
  return functools.reduce(adder, hosts, {})

def dic_return():
  return {1: "One"} 
   




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
  make_directory_if_not_exists(element_cache_directory)

  # Помещаем элементы данных, хосты, группы с сервера в нужные файлы
  with open(os.path.join(element_cache_directory,'items.txt'),'w') as f_obj:
    print(items, file=f_obj)

  with open(os.path.join(element_cache_directory,'hosts.txt'),'w') as f_obj:
    print(hosts, file=f_obj)
  
  with open(os.path.join(element_cache_directory,'groups.txt'),'w') as f_obj:
    print(groups, file=f_obj)

  # Фильтруем items, оставляем только с ошибками
  items = itertools.filterfalse(lambda x: not str(x['error']), items)

  out_dict = functools.reduce(adder, items, {})

  repl = get_hostnames(hosts)

  for item in list(out_dict):
    name = repl[item]
    out_dict[name] = out_dict.pop(item)

  #columns = [("hostname","item_name","status","error")]
  l = [["hostname","item_name","error"]]
  for dict_item in out_dict:
    li = out_dict[dict_item]
    for el in li:
      l.append([dict_item, el['name'], el['error']])
  
  table = l
  tab = PrettyTable(table[0])
  tab.add_rows(table[1:])
  print(tab)
    
    


  statistics_directory = 'statistics'
  make_directory_if_not_exists(statistics_directory)
  with open(os.path.join(statistics_directory,'statistics.txt'),'w') as f_obj:
    print(tab, file=f_obj)

  

  
  




