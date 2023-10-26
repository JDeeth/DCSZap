from dcs_bios_socket import DcsBiosSocket


def main():
    """daft demo - toggle SA342 panel lights"""
    dcs = DcsBiosSocket()
    flag = True
    while True:
        dcs.send_cmd("PANEL_LIGHTING", 1 if flag else 0)
        flag = not flag
        input()
