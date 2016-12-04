#encoding=UTF-8

'''
重构说明：
1.测试需求和测试实现应相互剥离
测试需求是的测试主体部分，而测试实现更多的是细节，主体与细节过多交织在一起，会造成无法快速的了解测试的目的。
测试实现更多的应该成为一种服务，当测试需求主体描述清楚后，在测试主体部分应屏蔽更多的测试实现细节。
matrix中的各种组合情况即是测试需求，至于这些服务如何进行restart，switchover等这样异常操作，则是细节，主体无需关心。

2.测试实现成为一种服务后，应屏蔽非必要的对外接口
AbnormalTesting类作为一种测试服务，其提供单一的对外接口execute_abnormal_test_and_check_log就够了，这是服务具备一种能力。
各种以__operate开头的功能函数只是服务于单一对外功能的辅助函数罢了，如不进行私有化，会使得AbnormalTesting的实例化调用者感到困惑。

遗留问题：
1.虽然完成了需求与实现的玻璃，但是整体代码依然存在代码可维护性较差的现状
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

        for matrix_item in self.__matrix:
            service_type = matrix_item[0]                       #服务种类
            service_state = matrix_item[1]                      #服务当前状态
            abnormal_operation = matrix_item[2]                 #对服务进行的异常操作类型

            services = get_all_services()                       #伪代码函数，获取整个分布式服务集群中的所有服务
            for index in range(len(services)):                  #遍历分布式集群上的所有服务
                if services[index].state==service_state:        #如当前服务，名称和状态与当前matrix项中一致，那就进行异常操作
                    self.service_name = services[index].name
                    if abnormal_operation=="restart":
                        self.__operate_restart_service()

                    if abnormal_operation=="switchover":
                        self.__operate_switchover_service()

                    if abnormal_operation=="stop_then_start":
                        self.__operate_stop_then_start_service()

                    if abnormal_operation=="hanging_then_recovery":
                        self.__operate_hanging_then_recovery()
                    
                    self.__exception_log_should_not_be_found()             #异常操作后检查有无异常日志出现
                    break
        
        disconnect_from_sut()                                       #伪代码，断开被测设备连接
        
    def __operate_restart_service(self,):
        print "==开始重启%s服务==" % self.service_name
        restart_service(self.service_name)                          #伪代码函数，进行服务重启的异常操作
        wait_service_state_ready(self.service_name)                 #伪代码函数，等待服务恢复 
        print "==重启%s服务结束" % self.service_name

    def __operate_switchover_service(self,):
        print "==开始主从切换%s服务==" % self.service_name
        switchover_service(self.service_name)                        #伪代码函数，进行服务主从切换的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==主从切换%s服务结束" % self.service_name

    def __operate_stop_then_start_service(self,):
        print "==开始停止后重启%s服务==" % self.service_name
        stop_then_start_service(self.service_name)                   #伪代码函数，进行服务停止后重启的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==停止后重启%s服务结束" % self.service_name

    def __operate_hanging_then_recovery(self,):
        print "==开始挂起后恢复%s服务==" % self.service_name
        hanging_then_recovery_service(self.service_name)             #伪代码函数，进行服务挂起后恢复的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==挂起后恢复%s服务结束" % self.service_name

    def __exception_log_should_not_be_found(self,):
        print "==没有发现异常日志=="


if __name__=="__main__":
    trigger_abnormal_testing_then_check_exception_log()
    
