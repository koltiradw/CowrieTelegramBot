import telebot
from telebot import types
import config
import collectors.logcollector as logcollector
import collectors.slicescollector as slicecollector
import ipscan
import collections
import plot.countries as countries
import plot.protocols as protocols
import plot.memcmp    as memcmp
import plot.cpucmp    as cpucmp
import stats.system
import stats.cowriestats
import stats.time_slice
import inline
import requests
import time


conf        = config.Config("config.json")
bot         = telebot.TeleBot(conf.get_telegram_token())
users       = conf.get_list_of_valid_users()
collect_obj = None

@bot.message_handler(commands = ['start'])
def start(message):
    input_username = str(message.from_user.username)
    if input_username in users:
        bot.send_message(
                message.chat.id,
                "Hi " + input_username + "!\n"
                )
        menu_handler(message)

@bot.message_handler(commands = ['help'])
def help(message):
    help_info = "Inline commands: \n"
    help_info += "   /cpu_usage_cmp - Total CPU usage comparison graph \n"
    help_info += "   /mem_usage_cmp - Total memory usage comparison graph \n"
    help_info += "   To run inline command on server use : /run our_sequence_of_commands \n"
    help_info += "   To start/stop cowrie use: /start_cowrie or /stop_cowrie \n"

    bot.send_message(
            message.chat.id,
            help_info
            )

@bot.message_handler(content_types = ['text'])
def event_handler(message):
    if message.text == "Histograms":
        histograms_handler(message)

    if message.text == "Stats":
        stats_handler(message)

    if "/run" in message.text:
        inline_mode_handler(message.text, message)

    if message.text == "Menu":
        menu_handler(message)

    if message.text == "Countries":
        collect_obj  = logcollector.Collector(conf.get_path_to_log_dir())
        plot_hist_of_countries(message, collect_obj)

    if message.text == "Protocols":
        collect_obj = logcollector.Collector(conf.get_path_to_log_dir()) 
        plot_hist_of_protocols(message, collect_obj)
    
    if message.text == "Cowrie stats":
        cowrie_stats_handler(message)
    
    if message.text == "System stats":
        system_stats_handler(message)

    if message.text == "/cpu_usage_cmp":
        collect_obj = slicecollector.Collector(conf.get_path_to_slices())
        cpu_usage_handler(message, collect_obj)
    
    if message.text == "/mem_usage_cmp":
        collect_obj = slicecollector.Collector(conf.get_path_to_slices())
        mem_usage_handler(message, collect_obj)

    if message.text == "/start_cowrie":
        inline_mode_handler("/run ../bin/cowrie start", message)
        bot.send_message(
                message.chat.id,
                "PID of cowrie: " + str(stats.time_slice.get_pid()) + "\n"
                )

    if message.text == "/stop_cowrie":
        inline_mode_handler("/run ../bin/cowrie stop", message)

def cowrie_stats_handler(message):
    cowrie_stats_info = stats.cowriestats.get_cowrie_stats()

    bot.send_message(
            message.chat.id,
            "Cowrie stats: " + cowrie_stats_info + "\n" 
            )

def inline_mode_handler(cmd, message):
    output = inline.run_inline_cmd(cmd[5:])
    bot.send_message(
            message.chat.id,
            output + "\n"
            )

def cpu_usage_handler(message, collect_obj):
    data = collect_obj.collect()
    if len(data["common_cpu_usage"]) == 0:
        bot.send_message(
                    message.chat.id,
                    "Not enough data!\n"
                    )
    else:
        cpucmp.create_plot(data["common_cpu_usage"], data["cowrie_cpu_usage"], data["time"])
        bot.send_message(
                    message.chat.id,
                    "CPU usage compare!\n"
                    )
        with open(cpucmp.PATH_TO_PHOTO, "rb") as photo:
            bot.send_photo(
                    message.chat.id,
                    photo
                    )

def mem_usage_handler(message, collect_obj):
    data = collect_obj.collect()
    if len(data["common_mem_usage"]) == 0:
        bot.send_message(
                message.chat.id,
                "Not enough data!\n"
                )
    else:
        memcmp.create_plot(data["common_mem_usage"], data["cowrie_mem_usage"], data["time"])
    
        bot.send_message(
            message.chat.id,
            "Memory usage compare!\n"
        )

        with open(memcmp.PATH_TO_PHOTO, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo
                    )

def system_stats_handler(message):
    sys_stat_info = stats.system.get_common_system_state()
    bot.send_message(
            message.chat.id,
            "System stat\n"
            )
    bot.send_message(
            message.chat.id,
            sys_stat_info
            )
    stats_handler(message)

def stats_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    markup.row("System stats", "Cowrie stats", "Menu")
    bot.send_message(
                message.chat.id,
                "Stats section!",
                reply_markup = markup
                        )

def plot_hist_of_countries(message, collect_obj):
    x_list, y_list = countries.get_data(conf.get_ipinfo_token(), collect_obj)
    countries.create_hist(list(x_list), list(y_list))
    bot.send_message(
            message.chat.id,
            "Histogram of countries:\n"
            )
    with open(countries.PATH_TO_PHOTO, "rb") as photo:
        bot.send_photo(
                message.chat.id, 
                photo
                )
    histograms_handler(message)

def plot_hist_of_protocols(message, collect_obj):
    x_list, y_list = protocols.get_data(collect_obj)
    protocols.create_hist(list(x_list), list(y_list))
    bot.send_message(
                message.chat.id,
                "Histogram of protocols:\n"
                )
    with open(protocols.PATH_TO_PHOTO, "rb") as photo:
        bot.send_photo(
                message.chat.id, 
                photo
                )
    histograms_handler(message)

def histograms_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    markup.row("Countries", "Protocols", "Menu")
    bot.send_message(
            message.chat.id,
            "Histograms section!",
            reply_markup = markup
            )

def menu_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    markup.row('Histograms', "Stats")
    bot.send_message(
            message.chat.id,
            "Welcome to main menu!\n",
            reply_markup = markup
            )

def work_bot():
    try:
        bot.polling(none_stop=False, interval=0, timeout=20)
    except Exception as e:
        time.sleep(20)
        work_bot()

def main():
    bot.remove_webhook()

    work_bot()

if __name__ == "__main__":
    main()



