import time
import threading

from schedule import Scheduler

SUCCESS_SCHEDULE = 'Task scheduled successfully'
FAILURE_SCHEDULE = 'Task could no be scheduled:'


class TaskScheduler:

    def __init__(self):
        self.task_schedule = Scheduler()

    def minutely(self, minutes, task):
        """
        Execute task every specified set of minutes
        """
        try:
            self.task_schedule.every(minutes).minutes.do(task)
            print(SUCCESS_SCHEDULE)
        except Exception as error:
            print(FAILURE_SCHEDULE + error)

    def daily(self, time, task):
        """
        Execute task every day in the specified time
        """
        try:
            self.task_schedule.every().day.at(time).do(task)
            print(SUCCESS_SCHEDULE)
        except Exception as error:
            print(FAILURE_SCHEDULE + error)

    def monday_to_friday(self, time, task):
        """
        Execute task every monday to friday in the specified time
        """
        try:
            self.task_schedule.every().monday.at(time).do(task)
            self.task_schedule.every().tuesday.at(time).do(task)
            self.task_schedule.every().wednesday.at(time).do(task)
            self.task_schedule.every().thursday.at(time).do(task)
            self.task_schedule.every().friday.at(time).do(task)
            print(SUCCESS_SCHEDULE)
        except Exception as error:
            print(FAILURE_SCHEDULE + error)

    def run_tasks_in_background(self, interval=1):
        """
        Background run, while executing pending jobs at each elapsed time interval
        """
        cease_background_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_background_run.is_set():
                    self.task_schedule.run_pending()
                    time.sleep(interval)

        background_thread = ScheduleThread()
        background_thread.start()
        return cease_background_run
