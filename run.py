import config
import munz

def main():
    try:
        bot = munz.MunZ(config.TOKEN)
        bot.start()
    except Exception as err:
        print(err)
        main()

if __name__ == "__main__":
    main()
