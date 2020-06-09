from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher
from tg_bot import GH_AUTH_TOKEN
from tg_bot.modules.sql import github_sql as sql

import re
from typing import List
from github import Github


@run_async
def commits(repo, entries, bot, update):
    message = update.effective_message
    commits = []
    for count, commit in enumerate(repo.get_commits()):
        if count >= entries:
            break
        commits.append(
            "[commit %s](%s)\n*Author:* %s `<%s>`\n*Date:* %s\n\n\t%s\n\n"
            % (
                commit.commit.sha[:20],
                commit.commit.html_url,
                commit.commit.author.name,
                commit.commit.author.email,
                commit.commit.author.date,
                commit.commit.message,
            )
        )
    message.reply_text(
        "\n".join(commits), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


@run_async
def events(repo, bot, update):
    # TODO: Fix this

    # message = update.effective_message
    # events = []
    # for event in repo.get_network_events():
    #     if event.type == "PushEvent" and event.payload["ref"][11:] == "master":
    #         pprint.pprint(event.payload)
    #         for commit in event.payload["commits"]:
    #             events.append(
    #                 "[%s](%s) pushed to *%s*\n([%s](%s)) - %s\n"
    #                 % (
    #                     commit["author"]["name"],
    #                     event.actor.html_url,
    #                     event.payload["ref"],
    #                     commit["sha"][:7],
    #                     re.sub(
    #                         "commits",
    #                         "commit",
    #                         re.sub("repos/", "", re.sub("api.", "", commit["url"])),
    #                     ),
    #                     commit["message"],
    #                 )
    #             )
    # message.reply_text(
    #     "\n".join(events), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    # )

    pass


@run_async
def gh(bot: Bot, update: Update, args: List[str]):
    try:
        message = update.effective_message
        command = args[0].lower()

        if command == "unregister":
            update.effective_message.reply_text(
                sql.unregister_repo(message.chat.id), parse_mode=ParseMode.MARKDOWN
            )
            return

        repo = sql.get_repo(message.chat.id)
        entries = 5
        if len(args) > 1:
            try:
                entries = int(args[1])
            except:
                repo = args[1]
        if len(args) > 2:
            repo = args[2]
        if not repo:
            update.effective_message.reply_text("Target repository not specified!")
            return

        try:
            target = Github(GH_AUTH_TOKEN).get_repo(repo)
        except:
            update.effective_message.reply_text("Invalid/inaccessible repository!")
            return

        if command == "commits" or command == "log":
            commits(target, entries, bot, update)
        elif command == "register":
            update.effective_message.reply_text(
                sql.register_repo(message.chat.id, repo), parse_mode=ParseMode.MARKDOWN
            )
        elif command == "events":
            events(target, bot, update)
        else:
            update.effective_message.reply_text("'%s' is not a valid gh command." % args[0])
    except:
        update.effective_message.reply_text(
            "Something went wrong! Check command arguments and retry in a while."
        )


__help__ = """
 - /gh log <n> <repo>: Get the n most recent commits from target repository (default: n = 5).
"""

__mod_name__ = "Github"


GH_HANDLER = CommandHandler("gh", gh, pass_args=True)

dispatcher.add_handler(GH_HANDLER)
