from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from treemapHd import *
from treemapLib import *

# RQRP 조회 모듈
class EugeneQry(object):
    def __init__(self, QMainWindow):
        self.ui = QMainWindow

    # 주식 주문/체결 조회 요청
    def QueryStkTrd(self):
        self.ui.TableTrd.clearContents()
        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 0, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 비밀번호

        CLib.OpCommAPI_SetRqData( 2, b"")        # 주문번호 (NULL 전체주문)
        CLib.OpCommAPI_SetRqData( 3, b"%")       # 매도매수구분 (% 전체, 10 매도, 20 매수)
        CLib.OpCommAPI_SetRqData( 4, b"%")       # 종목코드 (% 전체)
        CLib.OpCommAPI_SetRqData( 5, b"2")       # 정렬구분 (1 정순, 2 역순)
        CLib.OpCommAPI_SetRqData( 6, b"01")      # 체결구분 (01 전체, 02 미체결)
        CLib.OpCommAPI_SetRqData( 7, b"0")       # 조회구분 (0 고정)

        # 조회 요청 처리
        iRtn = CLib.OpCommAPI_SendRq(self.ui.winId(), RQRP_TRAN_STK_TRD, 0)

        if iRtn < 0:
            sErrMsg = DIC_SENDRQ_ERR.get(iRtn)
            sErrMsg = "주식주문 조회 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "주식주문 조회 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn


    # 주식 주문/체결 조회 응답 처리
    def RecvStkTrd(self, wParam, lParam, iRqRpID):
        iCnt = CLib.OpCommAPI_GetRqrpCount(iRqRpID, 1)
        sMsg = "주식주문 조회 건수 : " + str(iCnt)
        self.ui.TxtBrLog.append(sMsg)

        for i in range(iCnt):
            if i >= self.ui.TableTrd.rowCount():
                self.ui.TableTrd.insertRow(i)
                self.ui.TableTrd.setRowHeight(i, 20)

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 4)      # 주문번호
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 0, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 5)      # 원주문번호
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 1, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 6)      # 종목코드
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 2, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 7)      # 종목명
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 3, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 8)      # 정정취소구분
            sVal = sVal.decode("cp949").strip()
            sVal = DIC_ORD_TCD.get(sVal)
            self.ui.TableTrd.setItem(i, 4, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 9)      # 매매구분
            sVal = sVal.decode("cp949").strip()
            sVal = DIC_SELL_BUY_TCD.get(sVal)
            self.ui.TableTrd.setItem(i, 5, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 11)     # 주문수량
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 6, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 12)     # 주문가격
            sVal = sVal.decode("cp949").strip()
            sVal = str(int(float(sVal)))
            self.ui.TableTrd.setItem(i, 7, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 13)     # 미체결잔량
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 8, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 14)     # 체결수량
            sVal = sVal.decode("cp949").strip()
            self.ui.TableTrd.setItem(i, 9, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 32)     # 체결평균단가
            sVal = sVal.decode("cp949").strip()
            sVal = str(int(float(sVal)))
            self.ui.TableTrd.setItem(i, 10, QTableWidgetItem(sVal))

            # 컬럼 정렬
            iTblCnt = self.ui.TableTrd.columnCount()
            for j in range(iTblCnt):
                self.ui.TableTrd.item(i, j).setTextAlignment(TPL_TRD_FORM[j][1])


    # 주식잔고 조회 요청
    def QueryStkPstn(self):
        self.ui.TablePstn.clearContents()

        CLib.OpCommAPI_SetRqData( 0, b"1")       # 조회구분 (1 고정)

        sVal = self.ui.EditAcno.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 1, sVal)       # 계좌번호

        sVal = self.ui.EditPswd.text()
        sVal = sVal.encode()
        CLib.OpCommAPI_SetRqData( 2, sVal)       # 비밀번호

        CLib.OpCommAPI_SetRqData( 3, b"040")     # 주문매체구분 (040 고정)
        CLib.OpCommAPI_SetRqData( 4, b"N")       # 수수료포함여부 (Y 수수료 포함, N 수수료 포함 안함)
        CLib.OpCommAPI_SetRqData( 5, b"N")       # 현재가반영여부 (N 고정)

        # 조회 요청 처리
        iRtn = CLib.OpCommAPI_SendRq(self.ui.winId(), RQRP_TRAN_STK_PSTN, 0)

        if iRtn < 0:
            sErrMsg = DIC_SENDRQ_ERR.get(iRtn)
            sErrMsg = "주식잔고 조회 : 오류 (" + sErrMsg + ")"
            self.ui.TxtBrLog.append(sErrMsg)
        else:
            sErrMsg = "주식잔고 조회 : 성공"
            self.ui.TxtBrLog.append(sErrMsg)

        return iRtn


    # 주식잔고 조회 응답 처리
    def RecvStkPstn(self, wParam, lParam, iRqRpID):
        iCnt = CLib.OpCommAPI_GetRqrpCount(iRqRpID, 1)
        sMsg = "주식잔고 조회 건수 : " + str(iCnt)
        self.ui.TxtBrLog.append(sMsg)

        for i in range(iCnt):
            if i >= self.ui.TablePstn.rowCount():
                self.ui.TablePstn.insertRow(i)
                self.ui.TablePstn.setRowHeight(i, 20)

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 0)      # 종목코드
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 0, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 1)      # 종목명
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 1, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 6)      # 잔고수량
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 2, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 11)      # 매입단가
            sVal = sVal.decode("cp949").strip()
            sVal = str(int(float(sVal)))
            self.ui.TablePstn.setItem(i, 3, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 12)     # 매입금액
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 4, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 21)     # 현재가
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 5, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 22)     # 평가금액
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 6, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 23)     # 평가손익
            sVal = sVal.decode("cp949").strip()
            self.ui.TablePstn.setItem(i, 7, QTableWidgetItem(sVal))

            sVal = CLib.OpCommAPI_GetRqrpData(iRqRpID, 1, i, 24)     # 평가손익률
            sVal = sVal.decode("cp949").strip()
            sVal = str(round(float(sVal),2))
            self.ui.TablePstn.setItem(i, 8, QTableWidgetItem(sVal))

            # 컬럼 정렬
            iTblCnt = self.ui.TablePstn.columnCount()
            for j in range(iTblCnt):
                self.ui.TablePstn.item(i, j).setTextAlignment(TPL_PSTN_FORM[j][1])
