#encoding=UTF-8

'''
重构说明：
1.相似度高的不同异常操作类，定义抽象类约束规范，并从AbnormalOperation类中剥离
定义抽象类或接口，做到继承类的行为约束规范，从而实现面向接口编程，而非面向实现编程，也进一步实现解耦与提高代码整体可维护性。

至此，基本上完成了所有的重构过程，从测试整体需求，测试实现的整体实现，测试实现的细节实现完成了层次的剥离与解耦。
在这个例子中，这种分层的优势可能并不明显，但在大规模测试代码的维护中，层次耦合是代码维护的一个噩梦。
可以将这些不同的层次，在不同的代码文件或者代码package中进行相应的维护和管理，即可提高大规模自动化测试代码的可维护性。
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
        operation = OperateService(self.service_name)
        if abnormal_operation=="restart":
            operation = RestartService()

        if abnormal_operation=="switchover":
            operation = SwitchoverService()

        if abnormal_operation=="stop_then_start":
            operation = StopThenStartService()

        if abnormal_operation=="hanging_then_recovery":
            operation = HangingThenRecovery()

        operation.operate()


class OperateService():
    def __init__(self, service_name):
        self.service_name = service_name

    def operate(self,):             #提供类似于接口或抽象类的行为约束规范。但在python中没有相应的方式，这里仅仅是一种弱声明。
        pass


class RestartService(OperateService):
    def operate(self,):                                             #实现接口
        print "==开始重启%s服务==" % self.service_name
        restart_service(self.service_name)                          #伪代码函数，进行服务重启的异常操作
        wait_service_state_ready(self.service_name)                 #伪代码函数，等待服务恢复 
        print "==重启%s服务结束" % self.service_name


class SwitchoverService(OperateService):
    def operate(self,):                                              #实现接口
        print "==开始主从切换%s服务==" % self.service_name
        switchover_service(self.service_name)                        #伪代码函数，进行服务主从切换的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==主从切换%s服务结束" % self.service_name


class StopThenStartService(OperateService):
    def operate(self,):                                              #实现接口
        print "==开始停止后重启%s服务==" % self.service_name
        stop_then_start_service(self.service_name)                   #伪代码函数，进行服务停止后重启的异常操作
        wait_service_state_ready(self.service_name)                  #伪代码函数，等待服务恢复
        print "==停止后重启%s服务结束" % self.service_name


class HangingThenRecovery(OperateService):
    def operate(self,):                                              #实现接口
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
