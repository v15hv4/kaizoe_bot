from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher
from tg_bot import GH_AUTH_TOKEN

import re
from typing import List
from github import Github


@run_async
def commits(repo, bot, update):
    message = update.effective_message
    commits = [
        "[commit %s](%s)\n*Author:* %s `<%s>`\n*Date:* %s\n\n\t%s\n\n"
        % (
            commit.commit.sha[:20],
            commit.commit.html_url,
            commit.commit.author.name,
            commit.commit.author.email,
            commit.commit.author.date,
            commit.commit.message,
        )
        for commit in repo.get_commits()
    ]
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
    arg = args[0]
    g = Github(GH_AUTH_TOKEN)
    repo = g.get_repo("v15hv4/dotfiles")
    if arg.lower() == "commits" or arg.lower() == "log":
        commits(repo, bot, update)
    elif arg.lower() == "events":
        events(repo, bot, update)
    else:
        update.effective_message.reply_text("Invalid command!")


GH_HANDLER = CommandHandler("gh", gh, pass_args=True)

dispatcher.add_handler(GH_HANDLER)
