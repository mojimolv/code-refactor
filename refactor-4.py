#encoding=UTF-8

'''
重构说明：
1.拆解AbnormalTesting与AbnormalOperation之间存在的耦合
测试整体实现AbnormalTesting中，需要根据AbnormalOperation提供异常操作种类变化而变化的部分，直接迁移内嵌到AbnormalOperation中。
至此，中间层次测试整体实现的代码已经不再需要变化，能较好地做到异常操作种类动态延伸收缩的兼容。

遗留问题：
1.AbnormalOperation类中存在较多相似性很高的异常操作方法，其不断扩展将直接影响AbnormalOperation类的可维护性
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
                    ao.excute_operation()
                    vc.exception_log_should_not_be_found()          #异常操作后检查有无异常日志出现
                    break
        
        disconnect_from_sut()                                       #伪代码，断开被测设备连接


class AbnormalOperation():
    def __init__(self, service_name, abnormal_operation):
        self.service_name = service_name
        self.abnormal_operation = abnormal_operation

    def excute_operation(self,):
        if abnormal_operation=="restart":
            self.__operate_restart_service()

        if abnormal_operation=="switchover":
            self.__operate_switchover_service()

        if abnormal_operation=="stop_then_start":
            self.__operate_stop_then_start_service()

        if abnormal_operation=="hanging_then_recovery":
            self.__operate_hanging_then_recovery()


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


class Verification():
    def __init__(self,):
        pass

    def exception_log_should_not_be_found(self,):
        print "==没有发现异常日志=="


if __name__=="__main__":
    trigger_abnormal_testing_then_check_exception_log()
