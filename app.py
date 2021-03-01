import time
import threading
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from services import amazon_service


root = tk.Tk()

root.title("Amazon Reports")

main_canvas = tk.Canvas(root, width=300, height=300)
main_canvas.pack()

run_report_btn_text = tk.StringVar()
run_report_btn_text.set('Run report')

notification_label_text = tk.StringVar()

run_report_btn = tk.Button(
    textvariable=run_report_btn_text, fg='black', width=25)

main_canvas.create_window(150, 150, window=run_report_btn)

success = tk.Label(root, textvariable=notification_label_text,
                   fg='green', font=('arial', 12, 'bold'))

main_canvas.create_window(150, 200, window=success)


def success_notification():
    run_report_btn_text.set('Run report')
    run_report_btn.config(state=NORMAL)
    notification_label_text.set('Report created, check your email.')
    time.sleep(3)
    notification_label_text.set('')


def action_create_report():
    run_report_btn_text.set('Report is running...')
    run_report_btn.config(state=DISABLED)
    t_report = threading.Thread(
        target=amazon_service.create_report, args=(success_notification,))
    t_report.start()


def main():
    run_report_btn.config(command=action_create_report)
    root.mainloop()


if __name__ == "__main__":
    main()
