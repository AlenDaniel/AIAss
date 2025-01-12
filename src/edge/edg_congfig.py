# 一个配置edge参数的库




# http路由
ttlPath = 'http://0.0.0.0:5000/send/data'
logName = "./log/BCI_edge.log"
logSubject = "BCI_edge 日志告警"


# 服务
httpServer = {
    'uname':'0.0.0.0',
    "paths":"server.api:app",
    "ports":5500,
    "log":'info',
    "reloade":True
}
