from tensorflow.keras.callbacks import Callback
from telegram import Bot


class KerasTelegramBot(Callback):
    def __init__(self, bot_api_token, user_chat_id):
        self.bot_api_token = bot_api_token
        self.user_chat_id = user_chat_id

    def on_train_begin(self, logs=None):
        try:
            Bot(self.bot_api_token).sendMessage(self.user_chat_id, "Training started")
        except:
            print("Could not send message")

    def on_epoch_end(self, epoch, logs=None):
        metric_names = logs.keys()
        
        metrics_as_str = ', '.join(['{}: {}'.format(key, str(logs[key]))
                                    for key in metric_names])

        message = 'Epoch {}: {}'.format(epoch + 1,
                                        metrics_as_str)

        try:
            Bot(self.bot_api_token).sendMessage(self.user_chat_id, message)
        except:
            print("Could not send message")
