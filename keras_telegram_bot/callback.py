from tensorflow.keras.callbacks import Callback
from telegram import Bot


class KerasTelegramBot(Callback):
    def __init__(self, bot_api_token, user_chat_id):
        self.bot_api_token = bot_api_token
        self.bot = Bot(self.bot_api_token)
        self.user_chat_id = user_chat_id

    def on_epoch_end(self, epoch, logs=None):
        metric_names = ['{}_{}'.format('epoch', metric.name)
                        for metric in self.model.metrics]

        metric_values = {metric: logs[metric] for metric in metric_names}

        has_val = 'val_{}'.format(metric_names[0]) in logs
        if has_val:
            for metric in metric_names:
                val_metric = 'val_{}'.format(metric)
                metric_values[val_metric] = logs[metric_values]
        
        metrics_as_str = ', '.join(['{}: {}'.format(key, str(metric_values[key]))
                                    for key in metric_values])

        message = 'Epoch {}: {}'.format(epoch + 1,
                                        metrics_as_str)

        self.bot.sendMessage(self.user_chat_id, message)
