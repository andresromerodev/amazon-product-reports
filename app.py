import time
import threading
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from services.amazon_service import create_report

COLOR_ACTION = '#118ab2'
COLOR_RUNNING = '#a8dadc'
COLOR_SUCCESS = '#06d6a0'

root = tk.Tk()

root.title("Amazon Reports")
root.resizable(0, 0)

main_canvas = tk.Canvas(root, width=300, height=300)
main_canvas.pack()

run_report_btn_text = tk.StringVar(value='Run Report')
notifications_text = tk.StringVar()

run_report_btn = tk.Button(textvariable=run_report_btn_text, bg=COLOR_ACTION,
                           fg='white', font=('arial', 10, 'bold'), width=25)

main_canvas.create_window(150, 150, window=run_report_btn)

notifications = tk.Label(root, textvariable=notifications_text,
                         fg=COLOR_SUCCESS, font=('arial', 12, 'bold'))

main_canvas.create_window(150, 200, window=notifications)


def on_report_success():
    run_report_btn_text.set('Run Report')
    run_report_btn.config(state=NORMAL, bg=COLOR_ACTION)
    show_success_notification()


def action_create_report():
    t_report = threading.Thread(
        target=create_report, args=(on_report_success,))
    t_report.start()
    set_app_to_running_state()


def show_success_notification():
    notifications_text.set('Success, check your email.')
    time.sleep(3)
    notifications_text.set('')


def set_app_to_running_state():
    run_report_btn_text.set('Running...')
    run_report_btn.config(state=DISABLED, bg=COLOR_RUNNING)


def main():
    run_report_btn.config(command=action_create_report)
    root.mainloop()


if __name__ == "__main__":
    main()
