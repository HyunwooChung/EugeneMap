from ctypes import *

# 유진 Library Load 모듈
class EugeneLib(object):
    OpCommAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCommAPI.dll')
    OpCodeAPI = windll.LoadLibrary('C:\\EugeneFN\\NewChampionLink\\OpCodeAPI.dll')

    # 초기화
    OpCommAPI_Initialize = OpCommAPI.OpCommAPI_Initialize
    OpCommAPI_Initialize.restype = c_bool
    OpCommAPI_Initialize.argtypes = [c_int]

    # 초기화 해제
    OpCommAPI_UnInitialize = OpCommAPI.OpCommAPI_UnInitialize
    OpCommAPI_UnInitialize.restype = c_bool
    OpCommAPI_UnInitialize.argtypes = []

    # 조회 데이터 INPUT값 지정
    OpCommAPI_SetRqData = OpCommAPI.OpCommAPI_SetRQData
    OpCommAPI_SetRqData.restype = c_void_p
    OpCommAPI_SetRqData.argtypes = [c_int, c_char_p]

    # 조회 데이터 INPUT값 전체삭제
    OpCommAPI_ClearRQData = OpCommAPI.OpCommAPI_ClearRQData
    OpCommAPI_ClearRQData.restype = c_void_p
    OpCommAPI_ClearRQData.argtypes = []

    # 조회 데이터 전송
    OpCommAPI_SendRq = OpCommAPI.OpCommAPI_SendRq
    OpCommAPI_SendRq.restype = c_int
    OpCommAPI_SendRq.argtypes = [c_int, c_int, c_int]

    # 조회 데이터 수신시(WM_EU_RQRP_RECV) 조회 데이터 Output 데이터를 가져오는 함수
    OpCommAPI_GetRqrpData = OpCommAPI.OpCommAPI_GetRqrpData
    OpCommAPI_GetRqrpData.restype = c_char_p
    OpCommAPI_GetRqrpData.argtypes = [c_int, c_int, c_int, c_int]

    # 조회 데이터 수신시(WM_EU_RQRP_RECV) 조회 데이터 Output 데이터의 조회 건수를 가져오는 함수
    OpCommAPI_GetRqrpCount = OpCommAPI.OpCommAPI_GetRqrpCount
    OpCommAPI_GetRqrpCount.restype = c_int
    OpCommAPI_GetRqrpCount.argtypes = [c_int, c_int]

    # 실시간 데이터 등록 및 해제
    OpCommAPI_RequestReal = OpCommAPI.OpCommAPI_RequestReal
    OpCommAPI_RequestReal.restype = c_int
    OpCommAPI_RequestReal.argtypes = [c_int, c_bool, c_byte, c_char_p]

    # 해당 윈도우의 모든 실시간 데이터 해제
    OpCommAPI_UnRegisterRealAll = OpCommAPI.OpCommAPI_UnRegisterRealAll
    OpCommAPI_UnRegisterRealAll.restype = c_void_p
    OpCommAPI_UnRegisterRealAll.argtypes = [c_int]

    # 리얼 데이터 수신시(WM_EU_REAL_RECV) 데이터를 가져 오는 함수
    OpCommAPI_GetRealData = OpCommAPI.OpCommAPI_GetRealData
    OpCommAPI_GetRealData.restype = c_char_p
    OpCommAPI_GetRealData.argtypes = [c_byte, c_int]

    # WM_EU_RQRP_ERR_RECV 수신시 lParma으로 넘어가는 오류 메세지 값
    OpCommAPI_GetErrMsg = OpCommAPI.OpCommAPI_GetErrMsg
    OpCommAPI_GetErrMsg.restype = c_char_p
    OpCommAPI_GetErrMsg.argtypes = []

    # WM_EU_NOTI_RECV 수신시 lParma으로 넘어가는 서버공지 메세지 값
    OpCommAPI_GetNotiMsg = OpCommAPI.OpCommAPI_GetNotiMsg
    OpCommAPI_GetNotiMsg.restype = c_char_p
    OpCommAPI_GetNotiMsg.argtypes = []

    # 단축코드로 표준코드를 구하는 함수
    OpCodeAPI_GetExpCode = OpCodeAPI.OpCodeAPI_GetExpCode
    OpCodeAPI_GetExpCode.restype = c_char_p
    OpCodeAPI_GetExpCode.argtypes = [c_char_p]

    # 표준코드로 단축코드를 구하는 함수
    OpCodeAPI_GetShCode = OpCodeAPI.OpCodeAPI_GetShCode
    OpCodeAPI_GetShCode.restype = c_char_p
    OpCodeAPI_GetShCode.argtypes = [c_char_p]

    # 종목명으로 단축코드를 구하는 함수
    OpCodeAPI_GetShCodeByName = OpCodeAPI.OpCodeAPI_GetShCodeByName
    OpCodeAPI_GetShCodeByName.restype = c_char_p
    OpCodeAPI_GetShCodeByName.argtypes = [c_char_p]

    # 코드로 종목명을 구하는 함수
    OpCodeAPI_GetNameByCode = OpCodeAPI.OpCodeAPI_GetNameByCode
    OpCodeAPI_GetNameByCode.restype = c_char_p
    OpCodeAPI_GetNameByCode.argtypes = [c_char_p]


CLib = EugeneLib()
