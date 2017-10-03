globalinfo = {
    # option: http or https.
    'HTTP_PROTOCOL': 'http',
    # False or the path to certificate file. used for https
    'CERT_VERIFY': False
}

rabbitserverinfo = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'port':  5672,
    'CERT_VERIFY': False,
}

rabbithttpapi = {
    'root_url': 'http://{}:15672'.format(rabbitserverinfo['host']),
    'exchange_url': '/api/exchanges',
    'queue_url': '/api/queues',
}

storeserver = {
    'IP': '127.0.0.1',
    'PORT': 8000,
    'API_SERVER_USER': 'admin',
    'API_SERVER_PWD': 'admin',
    'ALLOWED_HOSTS':['192.168.1.102', 'localhost', '127.0.0.1', 'jeawy-pc'],
   
    # get the remote node to delivery
    'API_GET_NODE': '/api/nodes/',
    'API_ADD_TASK': '/nodes/taskcounter/',

    'API_RUN_COMPUTE': '/api/run_compute/',
    'API_RUN_FILEUPLOAD': '/api/autofile/upload_file/',
    'API_GET_FILE_SERVER': '/api/fileserver/get_upload_info/',
	'RESULT_UPDATE_API': '/api/results/{0}/',
	'SIMUFUNCTION_FILE_IN_PATH': 'result/{0.year}/{0.month}/{0.day}/{1}/model/',
	'UPLOAD_INPUTFILE_API': '/api/results/transferfile?pk={0}&nodeapi={1}',
    'CERT_VERIFY': False,
}

 
rabbit = {
    #the route key bindded to exchange and queue
    'KEY_FOR_Q_AVAIL': 'msg_avail',
    'KEY_FOR_Q_REAL': 'msg_real',

    'Q_AVAILABLE_GOODS': 'q_available_goods',
    'Q_REAL_GOODS': 'q_real_goods',

    'EXCHANGE': 'store_exchange',
}
