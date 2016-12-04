#encoding=UTF-8

'''
重构说明：
1.用函数的方式剥离实现细节
为了实现一个测试需求，将几乎所有的代码都集中在一个函数过程中，特别是多级for循环过程中，是不合适的。
随着需要支持的分布式服务种类增加，以及异常测试类型的增加，整个测试代码将会变得越发冗长，不可维护。

遗留问题：
1.测试需求与测试实现依然存在很大程度上的耦合。
2.整个代码文件对外提供的接口函数没有public与private的区别，容易造成调用者的困惑与混淆。
'''

def trigger_abnormal_testing_and_check_exception_log():
    ‘‘‘对整个分布式服务集群进行异常操作测试，并在异常操作后进行异常日志校验’’’

    matrix=[['service1', 'working', 'restart'],             #定义服务名称，状态，异常操作种类的matrix
           ['service1', 'standby', 'restart'],
           ['service1', 'standby', 'switchover'],
           ['service2', 'working', 'stop_then_start'],
           ['service2', 'standby', 'stop_then_start'],
           ['service3', 'working', 'hanging_then_recovery'],
           ['service3', 'standby', 'hanging_then_recovery'],
    
    connect_to_sut()                                        #伪代码函数，连接到被测设备

    for matrix_item in matrix:
        service_type = matrix_item[0]                       #服务种类
        service_state = matrix_item[1]                      #服务当前状态
        abnormal_operation = matrix_item[2]                 #对服务进行的异常操作类型

        services = get_all_services()                       #伪代码函数，获取整个分布式服务集群中的所有服务
        for index in range(len(services)):                  #遍历分布式集群上的所有服务
            if services[index].state==service_state:        #如当前服务，名称和状态与当前matrix项中一致，那就进行异常操作
                service_name = services[index].name
                if abnormal_operation=="restart":
                    operate_restart_service(service_name)

                if abnormal_operation=="switchover":
                    operate_switchover_service(service_name)

                if abnormal_operation=="stop_then_start":
                    operate_stop_then_start_service(service_name)

                if abnormal_operation=="hanging_then_recovery":
                    operate_hanging_then_recovery(service_name)
                
                exception_log_should_not_be_found()         #异常操作后检查有无异常日志出现
                break
    
    disconnect_from_sut()                                   #伪代码，断开被测设备连接
    

def operate_restart_service(service_name):
    print "==开始重启%s服务==" % service_name
    restart_service(service_name)                           #伪代码函数，进行服务重启的异常操作
    wait_service_state_ready(service_name)                  #伪代码函数，等待服务恢复
    print "==重启%s服务结束" % service_name

def operate_switchover_service(service_name):
    print "==开始主从切换%s服务==" % service_name
    switchover_service(service_name)                        #伪代码函数，进行服务主从切换的异常操作
    wait_service_state_ready(service_name)                  #伪代码函数，等待服务恢复
    print "==主从切换%s服务结束" % service_name

def operate_stop_then_start_service(service_name):
    print "==开始停止后重启%s服务==" % service_name
    stop_then_start_service(service_name)                   #伪代码函数，进行服务停止后重启的异常操作
    wait_service_state_ready(service_name)                  #伪代码函数，等待服务恢复
    print "==停止后重启%s服务结束" % service_name

def operate_hanging_then_recovery(service_name):
    print "==开始挂起后恢复%s服务==" % service_name
    hanging_then_recovery_service(service_name)             #伪代码函数，进行服务挂起后恢复的异常操作
    wait_service_state_ready(service_name)                  #伪代码函数，等待服务恢复
    print "==挂起后恢复%s服务结束" % service_name


def exception_log_should_not_be_found():
    print "==没有发现异常日志=="
    
if __name__=="__main__":
    trigger_abnormal_testing_then_check_exception_log()
