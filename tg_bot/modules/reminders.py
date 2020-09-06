from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher, updater

from typing import List

job = updater.job_queue


def parse_time(tstring):
    multiplier = {"h": 3600, "m": 60, "s": 1}
    unit = tstring[-1]
    try:
        value = int(tstring[:-1])
    except:
        return -1

    if unit not in multiplier.keys():  # Allow only H, M and S units
        return -2

    value *= multiplier[unit]
    if value > 21600:  # Limit max time to 6 hours
        return -3

    return value


def push_reminder(bot, job):
    message = "Reminder for @{username}: {text}".format(
        username=job.context["message"].from_user.username,
        text=" ".join(job.context["args"][1:]).strip(),
    )
    job.context["bot"].send_message(job.context["message"].chat_id, message)


@run_async
def remindme(bot, update, args: List[str]):
    global job
    timeout_err = {
        "-1": "Invalid time value specified!",
        "-2": "Invalid time unit specified!",
        "-3": "Timeout can not exceed 6 hours!",
    }

    message = update.effective_message
    context = {"message": message, "args": args, "bot": bot}
    timeout = parse_time(args[0])

    if timeout < 0:
        message.reply_text(timeout_err[str(timeout)])
        return

    job_remindme = job.run_once(push_reminder, timeout, context=context)
    message.reply_text("Reminder set!")


__mod_name__ = "Reminders"


REMINDME_HANDLER = CommandHandler("remindme", remindme, pass_args=True)

dispatcher.add_handler(REMINDME_HANDLER)
