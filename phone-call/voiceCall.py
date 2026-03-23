import voiceCall
import utime
import log
from machine import Pin
import audio


pa = Pin(Pin.GPIO10, Pin.OUT, Pin.PULL_DISABLE,1)

voiceCall.setChannel(2) #切换到喇叭通道
voiceCall.setVolume(5) #设置音量为5


# 初始化日志
log.basicConfig(level=log.INFO)
vc_log = log.getLogger("VOICE_CALL")

# 配置参数
TARGET_PHONE = "18577391748"  # 替换为你的测试号码
CALL_TIMEOUT = 30  # 拨号超时时间（秒）


class VoiceCallManager:
    def __init__(self):
        self.call_status = 0  # 通话状态：0=空闲，1=拨号中，2=通话中，3=来电
        self.incoming_num = None  # 来电号码
        # 设置通话状态回调（监听来电、接通等事件）
        voiceCall.setCallback(self.__call_state_callback)

    def __call_state_callback(self, *args):
        """
        通话状态回调函数
        """
        # 第一步：解析嵌套参数（取出内部实际参数列表）
        if len(args) >= 1 and isinstance(args[0], tuple):
            call_args = args[0]  # 内部实际参数列表
        else:
            vc_log.warning("回调参数格式异常：{}".format(args))
            return

        # 第二步：提取事件类型和号码（确保参数数量足够）
        if len(call_args) >= 7:
            event_type = call_args[0]  # 事件类型（10/11/12/15等）
            phone_num = call_args[6]   # 来电号码（从日志中定位的位置）
            #vc_log.info("通话事件：类型 {}, 号码 {}".format(event_type, phone_num))
        else:
            vc_log.warning("参数长度不足，无法解析：{}".format(call_args))
            return

        # 第三步：映射模块特定事件类型到实际场景（关键！）
        # 根据你的日志，这些类型对应来电流程：
        if event_type == 10:
            # 10：来电请求（开始振铃）
            self.call_status = 3  # 标记为来电状态
            self.incoming_num = phone_num
            vc_log.info("收到来电：{}，正在振铃...".format(phone_num))
            # 可在此处添加自动接听（如延迟2秒接听）：
            utime.sleep(2)
            self.answer_call()

        elif event_type == 12:
            # 12：通话挂断（对方挂断或自动挂断）
            self.call_status = 0
            vc_log.info("通话已挂断，号码：{}".format(phone_num))

        elif event_type == 11:
            # 11：通话接通（对方已接听或自动接听成功）
            self.call_status = 2 # 如果之前是来电状态，更新为通话中（可能已接听）
            self.incoming_num = None
            vc_log.info("通话已接通，号码：{}".format(phone_num))

        elif event_type == 15:
            # 15：呼出中，对方未响铃
            self.call_status = 1  # 保持拨号中状态
            self.incoming_num = None
            vc_log.info("呼出中，对方未响铃，号码：{}".format(phone_num))

        else:
            # 其他未知类型，仅记录不处理
            vc_log.info("收到未知事件类型：{}，号码：{}".format(event_type, phone_num))

    def dial_call(self, phone_num):
        """发起语音呼叫"""
        if self.call_status != 0:
            vc_log.error("当前有活跃通话，无法拨号")
            return False

        self.call_status = 1  # 更新为拨号中
        vc_log.info("开始拨号：{}".format(phone_num))
        ret = voiceCall.callStart(phone_num)
        if ret != 0:
            vc_log.error("拨号失败，错误码：{}".format(ret))
            return False

        # 等待通话接通或超时
        start_time = utime.time()
        while self.call_status != 2:  # 未接通
            if utime.time() - start_time > CALL_TIMEOUT:
                vc_log.warning("拨号超时（{}秒），自动挂断".format(CALL_TIMEOUT))
                self.hangup_call()
                return False
            if self.call_status == 0:  # 对方已挂断
                vc_log.info("对方已挂断")
                return False
            utime.sleep(1)

        vc_log.info("通话中......")
        return True

    def answer_call(self):
        """接听来电"""
        if self.call_status != 3:  # 非来电状态
            vc_log.error("当前无来电，无法接听")
            return False

        vc_log.info("接听来电：{}".format(self.incoming_num))
        ret = voiceCall.callAnswer()
        if ret == 0:
            self.call_status = 2  # 更新为通话中
            return True
        else:
            vc_log.error("接听失败，错误码：{}".format(ret))
            return False

    def hangup_call(self):
        """挂断当前通话"""
        if self.call_status == 0:
            vc_log.warning("当前无通话，无需挂断")
            return False

        vc_log.info("挂断通话")
        ret = voiceCall.callEnd()
        if ret == 0:
            self.call_status = 0  # 更新为空闲
            return True
        else:
            vc_log.error("挂断失败，错误码：{}".format(ret))
            return False


if __name__ == "__main__":
    call_manager = VoiceCallManager()  # 模块初始化
    vc_log.info("语音通话示例启动，准备拨号：{}".format(TARGET_PHONE))

    # 演示：发起语音呼叫
    if not call_manager.dial_call(TARGET_PHONE):
        vc_log.info("呼叫结束，已挂断")

    vc_log.info("示例程序运行中，可测试来电场景")