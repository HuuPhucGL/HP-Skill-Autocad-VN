# -*- coding: utf-8 -*-
# Sua doi boi Nguyen Huu Phuc (2026) tu vn-autocad-skill cua andyluu98, Apache-2.0.
"""Lap bang du toan chi phi xay dung ra file Excel.

Quy tac bat buoc: 100% phong chu Times New Roman, khoi luong lam tron 2 so le,
moi dong co cot dien giai cach tinh va phan tru, thanh tien va cac khoan chi phi
deu la cong thuc; ty le chi phi nam trong o rieng, khong go cung trong cong thuc.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

FONT = "Times New Roman"
THIN = Side(style="thin", color="A6A6A6")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill("solid", fgColor="D9D9D9")
SEC_FILL = PatternFill("solid", fgColor="F2F2F2")

COLS = [("STT", 6), ("Ma hieu", 11), ("Noi dung cong tac", 46),
        ("Dien giai, phan tru", 34), ("DVT", 8), ("Khoi luong", 12),
        ("Don gia (VND)", 15), ("Thanh tien (VND)", 18)]
SO_COT = len(COLS)
LE_KHOI_LUONG = 2       # quy dinh rieng: khoi luong lam tron 2 so le


def build_estimate(path, project, rows, *, vat, overhead, contingency):
    """Xuat file .xlsx du toan.

    project: dict {ten, dia_diem, chu_dau_tu, ngay}
    rows: danh sach, moi phan tu la
          ("SECTION", "PHAN I: PHAN NGAM VA MONG")  hoac
          (ma_hieu, noi_dung, dvt, khoi_luong, don_gia)  hoac
          (ma_hieu, noi_dung, dvt, khoi_luong, don_gia, dien_giai)
    vat, overhead, contingency: ty le, bat buoc truyen vao; thu vien khong tu gia dinh.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "DuToan_ChiPhi"
    _title(ws, project)
    last = _body(ws, rows)
    _summary(ws, last, vat, overhead, contingency)
    _layout(ws)
    wb.save(path)
    return path


# ---------------------------------------------------------------------------
def _title(ws, p):
    cuoi = get_column_letter(SO_COT)
    ws.merge_cells("A1:%s1" % cuoi)
    ws["A1"] = "BANG TONG HOP DU TOAN CHI PHI XAY DUNG CONG TRINH"
    ws["A1"].font = Font(name=FONT, size=14, bold=True)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A2:%s2" % cuoi)
    ws["A2"] = "DU AN: %s  |  DIA DIEM: %s" % (p.get("ten", ""), p.get("dia_diem", ""))
    ws["A2"].font = Font(name=FONT, size=11, italic=True)
    ws["A2"].alignment = Alignment(horizontal="center")

    ws.merge_cells("A3:%s3" % cuoi)
    ws["A3"] = "Chu dau tu: %s     Ngay lap: %s" % (p.get("chu_dau_tu", ""), p.get("ngay", ""))
    ws["A3"].font = Font(name=FONT, size=11, italic=True)
    ws["A3"].alignment = Alignment(horizontal="center")

    for i, (name, _) in enumerate(COLS, 1):
        c = ws.cell(row=5, column=i, value=name)
        c.font = Font(name=FONT, size=11, bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.fill = HEAD_FILL
        c.border = BOX


def _body(ws, rows):
    r = 6
    stt = 0
    for item in rows:
        if item[0] == "SECTION":
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=SO_COT)
            c = ws.cell(row=r, column=1, value=item[1])
            c.font = Font(name=FONT, size=11, bold=True)
            c.fill = SEC_FILL
            c.alignment = Alignment(horizontal="left", vertical="center")
            for i in range(1, SO_COT + 1):
                ws.cell(row=r, column=i).border = BOX
            r += 1
            continue
        stt += 1
        ma, noi_dung, dvt, kl, dg = item[:5]
        dien_giai = item[5] if len(item) > 5 else ""
        _cell(ws, r, 1, stt, "center")
        _cell(ws, r, 2, ma, "center")
        _cell(ws, r, 3, noi_dung, "left", wrap=True)
        _cell(ws, r, 4, dien_giai, "left", wrap=True)
        _cell(ws, r, 5, dvt, "center")
        _cell(ws, r, 6, round(kl, LE_KHOI_LUONG), "right", fmt="#,##0.00")
        _cell(ws, r, 7, dg, "right", fmt="#,##0")
        _cell(ws, r, 8, "=F%d*G%d" % (r, r), "right", fmt="#,##0")
        r += 1
    return r


def _summary(ws, r, vat, overhead, contingency):
    first, last = 6, r - 1
    lines = [
        ("CONG CHI PHI TRUC TIEP", None, "=SUM(H%d:H%d)" % (first, last), True),
        ("Chi phi chung va quan ly", overhead, "=H%d*G%d" % (r, r + 1), False),
        ("Chi phi du phong", contingency, "=H%d*G%d" % (r, r + 2), False),
        ("Cong truoc thue", None, "=H%d+H%d+H%d" % (r, r + 1, r + 2), False),
        ("Thue GTGT", vat, "=H%d*G%d" % (r + 3, r + 4), False),
        ("TONG CONG GIA TRI DU TOAN SAU THUE", None, "=H%d+H%d" % (r + 3, r + 4), True),
    ]
    for i, (label, ty_le, formula, bold) in enumerate(lines):
        row = r + i
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
        c = ws.cell(row=row, column=1, value=label)
        c.font = Font(name=FONT, size=11, bold=bold)
        c.alignment = Alignment(horizontal="right", vertical="center")
        if ty_le is not None:
            o = ws.cell(row=row, column=7, value=ty_le)
            o.font = Font(name=FONT, size=11, bold=bold)
            o.number_format = "0.00%"
            o.alignment = Alignment(horizontal="right")
        v = ws.cell(row=row, column=8, value=formula)
        v.font = Font(name=FONT, size=11, bold=bold)
        v.number_format = "#,##0"
        v.alignment = Alignment(horizontal="right")
        for col in range(1, SO_COT + 1):
            ws.cell(row=row, column=col).border = BOX


def _cell(ws, r, c, value, align, fmt=None, wrap=False):
    cell = ws.cell(row=r, column=c, value=value)
    cell.font = Font(name=FONT, size=11)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    cell.border = BOX
    if fmt:
        cell.number_format = fmt
    return cell


def _layout(ws):
    for i, (_, w) in enumerate(COLS, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[5].height = 30
    ws.freeze_panes = "A6"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
