from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher, updater

from typing import List

job = updater.job_queue


def push_reminder(bot, job):
    message = " ".join(job.context["args"][1:]).strip()
    job.context["message"].reply_text(message)


@run_async
def remindme(bot, update, args: List[str]):
    global job
    context = {"message": update.effective_message, "args": args}
    job_remindme = job.run_once(push_reminder, 30, context=context)


__mod_name__ = "Reminders"


REMINDME_HANDLER = CommandHandler("remindme", remindme, pass_args=True)

dispatcher.add_handler(REMINDME_HANDLER)
