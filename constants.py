# JSOn-объект для аутентификации
auth_json = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': '',
        'password': ''
    },
    'id': 1,
  }

# JSON-объект для поиска элементов данных в зависимости от ошибки
items_json = {
    'jsonrpc': '2.0',
    'method': 'item.get',
    'params': {
        'search': {
            'hostid': '',
            'error': ''
        },
        # Поля которые нужно выводить
      'output': ['hostid', 'host', 'name', 'error', 'state', 'status'],
      'with_triggers': 'true',
      'sortfield': ''
    },
    # Здесь нужно указать токен
    'auth': '',
    'id': 1
}

# JSON-объект для вывода хостов 
hosts_json = {
    'jsonrpc': '2.0',
    'method': 'host.get',
    'params': {
      #'output': ['hostid', 'host', 'name'],
      #'output': [],
      'filter': {
            'name': '',
        },
    },
    'auth': '',
    'id': 1
}

groups_json = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            
        }
    },
    "auth": "",
    "id": 1
}