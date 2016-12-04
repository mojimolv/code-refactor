#encoding=UTF-8

'''
重构说明：
1.测试的细节实现与整体实现相剥离
经过第二步的重构后，原先入口函数中的大量代码直接迁移到了AbnormalTesting类中，虽然做到了测试需求与实现的分离，但整体代码依然不好维护的现状并没有得到改善。
将更细节的异常测试实现从整体测试实现中剥离出来，可以有效控制整体测试实现的代码规模。

遗留问题：
1.随着AbnormalOperation类中异常操作种类的增加与减少，AbnormalTesting也依然需要增加与减少相应的if/else操作，两个类之间存在一定的耦合
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

    at = AbnormalTesting(matrix)
    at.execute_abnormal_test_and_check_log()
    
        
class AbnormalTesting():
    def __init__(self, matrix):
        self.__matrix=matrix
    
    def execute_abnormal_test_and_check_log(self,):
        connect_to_sut()                                        #伪代码函数，连接到被测设备
        vc = Verification()
        for matrix_item in self.__matrix:
            service_type = matrix_item[0]                       #服务种类
            service_state = matrix_item[1]                      #服务当前状态
            abnormal_operation = matrix_item[2]                 #对服务进行的异常操作类型

            services = get_all_services()                       #伪代码函数，获取整个分布式服务集群中的所有服务
            for index in range(len(services)):                  #遍历分布式集群上的所有服务
                if services[index].state==service_state:        #如当前服务，名称和状态与当前matrix项中一致，那就进行异常操作
                    ao = AbnormalOperation(services[index].name)
                    if abnormal_operation=="restart":
                        ao.operate_restart_service()

                    if abnormal_operation=="switchover":
                        ao.operate_switchover_service()

                    if abnormal_operation=="stop_then_start":
                        ao.operate_stop_then_start_service()

                    if abnormal_operation=="hanging_then_recovery":
                        ao.operate_hanging_then_recovery()
                    
                    vc.exception_log_should_not_be_found()          #异常操作后检查有无异常日志出现
                    break
        
        disconnect_from_sut()                                       #伪代码，断开被测设备连接


class AbnormalOperation():
    def __init__(self, service_name):
        self.service_name = service_name

    def operate_restart_service(self,):
        print "==开始重启%s服务==" % self.service_name
        restart_service(self.service_name)                          #伪代码函数，进行服务重启的异常操作
        wait_service_state_ready(self.service_name)                 #伪代码函数，等待服务恢复 
        print "==重启%s服务结束" % self.service_name

    def operate_switchover_service(self,):
        print "==开始主从切换%s服务==" % self.service_name
        switchover_service(self.service_name)                        #伪代码函数，进行服务主从切换的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==主从切换%s服务结束" % self.service_name

    def operate_stop_then_start_service(self,):
        print "==开始停止后重启%s服务==" % self.service_name
        stop_then_start_service(self.service_name)                   #伪代码函数，进行服务停止后重启的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==停止后重启%s服务结束" % self.service_name

    def operate_hanging_then_recovery(self,):
        print "==开始挂起后恢复%s服务==" % self.service_name
        hanging_then_recovery_service(self.service_name)             #伪代码函数，进行服务挂起后恢复的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==挂起后恢复%s服务结束" % self.service_name


class Verification():
    def __init__(self,):
        pass

    def exception_log_should_not_be_found(self,):
        print "==没有发现异常日志=="


if __name__=="__main__":
    trigger_abnormal_testing_then_check_exception_log()
    