from bot.actions import actions
from bot.replies import replies


def handle_messages(update, context):
    if update.message is None:
        return

    # job creation for channels
    if update.message.forward_from_chat is not None:
        return actions.add_new_channel_job(update)

    # job creation for groups/private chats
    reply_to_message = update.message.reply_to_message
    if reply_to_message is None:
        return
    text = reply_to_message.text_html
    if text == replies.request_jobname_message:
        actions.add_new_job(update, context)
    elif text == replies.request_text_message:
        actions.add_message(update, context)
    elif text == replies.delete_message:
        actions.remove_job(update, context)
    elif text == replies.start_message:
        actions.add_timezone(update)
    elif text == replies.list_jobs_message:
        actions.show_job_details(update, context)
    elif text == replies.checkcron_message:
        actions.decrypt_cron(update)
    elif text == replies.request_jobs_message:
        actions.add_new_jobs(update, context)
    elif (
        text == replies.request_crontab_message
        or text == replies.invalid_crontab_message
    ):
        actions.update_crontab(update, context)
    elif text == replies.change_timezone_message:
        actions.update_timezone(update, context)


def handle_photos(update, context):
    if update.message is None:
        return

    # job creation for channels
    if update.message.forward_from_chat is not None:
        return actions.add_new_channel_job(update)

    reply_to_message = update.message.reply_to_message
    if reply_to_message is None:
        return
    if reply_to_message.text_html == replies.request_text_message:
        actions.add_message(update, context, True)


def handle_polls(update, context):
    if update.message is None:
        return

    # job creation for channels
    is_channel_job = update.message.forward_from_chat is not None
    if update.message.poll.type == "quiz" and (
        update.message.chat.type != "private" or is_channel_job
    ):
        return replies.send_quiz_unavailable_message(update)

    if is_channel_job:
        return actions.add_new_channel_job(update=update, poll=True)

    reply_to_message = update.message.reply_to_message
    if reply_to_message is None:
        return

    if reply_to_message.text_html == replies.request_text_message:
        actions.add_message(update=update, context=context, photo=False, poll=True)


def handle_callback(update, context):
    query = update.callback_query
    if query.data == "1":
        actions.reset_chat(update, context)
    context.bot.editMessageReplyMarkup(
        chat_id=query.message.chat_id, message_id=query.message.message_id
    )
    query.answer()
