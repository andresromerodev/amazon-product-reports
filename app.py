import threading
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from services.amazon_service import create_report

COLOR_ACTION = '#118ab2'
COLOR_RUNNING = '#f5f3f4'
COLOR_SUCCESS = '#06d6a0'
COLOR_ERROR = '#e71d36'

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
                         fg=COLOR_SUCCESS, font=('arial', 8, 'bold'))

main_canvas.create_window(150, 200, window=notifications)


def on_report_success():
    show_success_notification()
    set_app_to_ready_state()


def on_report_failure(error):
    show_error_notification(error)
    set_app_to_ready_state()


def action_create_report():
    threading.Thread(target=create_report, args=(
        on_report_success, on_report_failure,)).start()
    set_app_to_running_state()


def show_success_notification():
    notifications.config(fg=COLOR_SUCCESS)
    notifications_text.set('Success, check your email.')


def show_error_notification(error):
    notifications.config(fg=COLOR_ERROR)
    notifications_text.set(f'E: {error}')


def set_app_to_running_state():
    run_report_btn_text.set('Running...')
    run_report_btn.config(state=DISABLED, bg=COLOR_RUNNING)
    notifications_text.set('')


def set_app_to_ready_state():
    run_report_btn_text.set('Run Report')
    run_report_btn.config(state=NORMAL, bg=COLOR_ACTION)


def main():
    run_report_btn.config(command=action_create_report)
    root.mainloop()


if __name__ == "__main__":
    main()
