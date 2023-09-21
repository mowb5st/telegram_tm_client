from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application

from utils import (
    logger_custom_exception,
    get_settings,
    get_balance,
    get_items_on_sale
)


class TmClient:
    def __init__(self):
        self.settings = get_settings
        self.tm_api = None
        self.tg_api = None
        self.chat_id = None
        self.last_message = None
        self.sleep_const = 10
        self.sleep_time = 10

    def run(self):
        self.load_app()
        self.load_tg_bot()

    def load_app(self):
        try:
            self.settings = self.settings()
            self.tm_api = self.settings['tm_api']
            self.tg_api = self.settings['tg_api']
        except Exception as error:
            logger_custom_exception(error, __name__)

    def load_tg_bot(self):
        application = Application.builder().token(self.tg_api).build()
        application.add_handler(CommandHandler('start', self.timer))
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def timer(self, update: Update,
                    context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        try:
            context.job_queue.run_once(
                self.work,
                0,
                chat_id=chat_id,
                name=str(chat_id)
            )
            context.job_queue.run_repeating(
                self.work,
                interval=self.sleep_const,
                chat_id=chat_id,
                name=str(chat_id)
            )
        except Exception as error:
            logger_custom_exception(error, __name__)

    async def work(self, context: ContextTypes.DEFAULT_TYPE):
        job = context.job
        message = self.create_message()
        if self.last_message:
            await context.bot.edit_message_text(
                text=message,
                chat_id=job.chat_id,
                message_id=self.last_message.id
            )
        else:
            self.last_message = await context.bot.send_message(
                job.chat_id, text=message)

    async def job(self,
                  context: ContextTypes.DEFAULT_TYPE,
                  error=False,
                  error_message=''):
        job = context.job
        if error:
            await context.bot.send_message(
                job.chat_id,
                text=error_message
            )
            return
        if self.last_message:
            await context.bot.edit_message_text(
                # self.tm(),
                job.chat_id,
                self.last_message.id,
                text=self.create_message()
            )
        else:
            self.last_message = await context.bot.send_message(
                job.chat_id,
                text=self.create_message()
            )

    def create_message(self):
        try:
            balance = get_balance(self.tm_api)
            success, items_on_sale, items_sold = (
                get_items_on_sale(self.tm_api)
            )
            message = (
                f'Balance: {balance["money"]} '
                f'{balance["currency"]}; \nItems on sale: '
                f'{items_on_sale}; \n'
                f'Items sold and waiting for trade: {items_on_sale}; \n'
                f'Last update: '
                f'{datetime.now().strftime("%H:%M:%S | %d-%m-%y")}'
            )
            return message
        except Exception as err:
            print(f'Error: {err}')
            logger_custom_exception(err, __name__)


if __name__ == '__main__':
    client = TmClient()
    client.run()
