import sys
import win32gui, win32con, win32ts
from ctypes import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from treemapHd import *
from treemapQry import *

# 실행파일과 동일한 폴더에 ui 파일을 복사할 것
# 바로가기로 실행하면 프로그램 경로를 가져올 수 없는 경우가 있어서 절대경로로 입력
# uidir = os.path.dirname(os.path.realpath(__file__))
ui = uic.loadUiType("C:\\EugeneFN\\NewChampionLink\\treemap.ui")[0]

class MyWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 윈도우 컨트롤 셋팅
        self.SetControl()

        # 윈도우폼 셋팅
        self.SetWindowForm()

        # 웹브라우저 컨트롤 셋팅
        self.SetTreemap()

        # 윈도우 이벤트 수신처리
        self.WindowEvent(self.winId())

        # RQRP 조회 인스턴스 생성
        self.CQry = EugeneQry(self)

        # 초기화
        iRtn = CLib.OpCommAPI_Initialize(self.winId())

        if iRtn == 0:
            self.TxtBrLog.append("서버접속 : 실패")
        else:
            self.TxtBrLog.append("서버접속 : 성공")

    # 윈도우 컨트롤 셋팅
    def SetControl(self):
        self.BtnPstn.clicked.connect(self.BtnPstnClick)

    # 윈도우 form 셋팅
    def SetWindowForm(self):
        # 잔고조회 QTableWidget 컬럼 Height 셋팅
        iTblRow = self.TablePstn.rowCount()
        for i in range(iTblRow):
            self.TablePstn.setRowHeight(i, 20)

        # 잔고조회 QTableWidget 컬럼 Width 셋팅
        iTblCnt = self.TablePstn.columnCount()
        for i in range(iTblCnt):
            self.TablePstn.setColumnWidth(i, TPL_PSTN_FORM[i][0])

        # 테이블그리드 헤더색상 변경
        style = "::section {""background-color: rgb(17,22,38); }"
        self.TablePstn.horizontalHeader().setStyleSheet(style)

        # 비밀번호 **** 마스킹 처리
        self.EditPswd.setEchoMode(QLineEdit.Password)

        # 디폴트 입력값
        self.EditAcno.setText("27111091101")   # 계좌번호
        self.EditPswd.setText("1357")          # 비밀번호


    # 트리맵 셋팅
    def SetTreemap(self):
        a = 1

    # 유진투자증권 API 윈도우 이벤트 수신처리
    # PyQt 사용시 일반적인 윈도우 이벤트 수신처리 방법을 모르겠음
    # 해당방법으로 정상 작동은 함
    def WindowEvent(self, app_hwnd):
        win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        #win32ts.WTSRegisterSessionNotification(app_hwnd, win32ts.NOTIFY_FOR_ALL_SESSIONS)

        def WindowProc(hWnd, msg, wParam, lParam):
            # OpCommAPI_RequestReal 요청에 대한 실시간 데이터 수신 메시지
            if msg == WM_EU_REAL_RECV:
                self.RecvReal(wParam, lParam)
            # OpCommAPI_SendRQ 요청에 대한 응답 메시지
            elif msg == WM_EU_RQRP_RECV:
                self.RecvRqRp(wParam, lParam)
            # OpCommAPI_SendRQ 요청에 대한 오류응답 메시지
            elif msg == WM_EU_RQRP_ERR_RECV:
                self.RecvRqRpErr(wParam, lParam)
            # 서버에서 보내는 긴급 메시지(통신단절, 접속해제 등)
            elif msg == WM_EU_NOTI_RECV:
                self.RecvNoti(wParam, lParam)
            elif msg == win32con.WM_DESTROY:
                # 해당 윈도우의 모든 실시간 데이터 해제
                CLib.OpCommAPI_UnRegisterRealAll(self.winId())

                # 초기화 해제
                iRtn = CLib.OpCommAPI_UnInitialize()
                if iRtn == 0:
                    self.TxtBrLog.append("서버종료 : 실패")
                else:
                    self.TxtBrLog.append("서버종료 : 성공")

                win32gui.DestroyWindow(app_hwnd)
                win32gui.PostQuitMessage(0)

            try:
                return win32gui.CallWindowProc(self.old_win32_proc, hWnd, msg, wParam, lParam)
            except Exception as e:
                print("except")

        self.old_win32_proc = win32gui.SetWindowLong(app_hwnd, win32con.GWL_WNDPROC, WindowProc)


    # OpCommAPI_RequestReal 요청에 대한 실시간 데이터 수신 처리
    def RecvReal(self, wParam, lParam):
        # 실시간 주식 우선호가 수신처리
        if wParam == REAL_TRAN_STK_PRC:
            self.CReal.RecvRealStkPrc(wParam, lParam)
        # 실시간 주식 체결시세 수신처리
        elif wParam == REAL_TRAN_STK_TICK:
            self.CReal.RecvRealStkTick(wParam, lParam)


    # OpCommAPI_SendRQ 요청에 대한 응답 처리
    def RecvRqRp(self, wParam, lParam):
        # 주식잔고 조회 응답처리
        if wParam == self.iRqRpID and self.RQRP_TRAN_ID == RQRP_TRAN_STK_PSTN:
            self.CQry.RecvStkPstn(wParam, lParam, self.iRqRpID)

        # 조회 데이터 INPUT값 전체삭제
        CLib.OpCommAPI_ClearRQData()


    # OpCommAPI_SendRQ 요청에 대한 오류응답 처리
    def RecvRqRpErr(self, wParam, lParam):
        # lParam 주소값을 문자열로 변환
        sVal = string_at(lParam)
        sVal = sVal.decode("cp949")
        self.TxtBrErr.setText(sVal)


    # 서버에서 보내는 긴급 메시지
    def RecvNoti(self, wParam, lParam):
        sErrMsg = DIC_NOTI_MSG.get(wParam)
        sErrMsg = "알림 : " + sErrMsg
        self.TxtBrLog.append(sErrMsg)

        # wParam = 100 : 서버에서 내려온 긴급 메시지
        if wParam == 100:
            # lParam 주소값을 문자열로 변환
            sErrMsg = string_at(lParam)
            sErrMsg = sErrMsg.decode("cp949")
            self.TxtBrLog.append(sErrMsg)

    # 주식잔고 조회 버튼 클릭
    def BtnPstnClick(self):
        self.iRqRpID = self.CQry.QueryStkPstn()
        self.RQRP_TRAN_ID = RQRP_TRAN_STK_PSTN


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()