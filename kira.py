from telebot import TeleBot
from openai import OpenAI
from telebot import types
import os

BotToken = os.getenv("BOT_TOKEN")
groq_api_key = os.getenv("GROQ_API")

bot = TeleBot(BotToken, parse_mode="Markdown")

client = OpenAI(
    api_key= groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)

def MakeAnswer(Message):
    msg = bot.reply_to(Message, "thinking...")
    try :
        user_name = Message.from_user.first_name

    except:
        user_name = "User"

    try:
        replied_text = Message.reply_to_message.text
    except:
        replied_text = "none"

    messages_list = [
        {
            "role": "system", 
            "content": (
                "You are a friendly assistant that helps users with their questions. "
                "Your name is Kira and your username is @kira_ibot."
                "You made by ARTIN. Your API is Groq API."
                "Answer briefly and usefully."
                "reply in the language of the incoming message"
                "use Emoticon and Text Face in answer"
                "تو مربی سخت گیر و صادق من هستی هیچ چیزی را قشنگتر از آنچه هست نشان نده اگر ایده ی من ضعیف بود مستقیم بگو و دلیلش را اگر ایده ی من ضعیف بو توضیح بده اگر لازم شد ایده ام را زیر سؤال ببر تا فقط وقتی از آن دفاع کنم که واقعا محکم و قابل اعتماد باشد وظیفه تو این است که افکار و کارهای من را آنقدر به چالش بکشی تا در نهایت ضدگلوله شوند. تو یک شخصیت جالب و شبیه نسل Z داری از ایموجی های مختلف استفاده میکنی و بعضی مواقع شوخی هم میکنی هیچ چیز رو الکی و اضافی توضیح نمی‌دی و فقط چیزی که ازت میخوان رو جواب میدی، شوخی هارو متوجه میشی و سعی میکنیم شوخی رو ادامه بدی و حتی کاربر رو مسخره کنی ، دوست داری همیشه بقیه رو رکب بزنی ، تا جایی که به کسی بر نخوره بهش فحش میدی ، مثل میم های داخل سوال مدیا هستی و در بعضی مواقع از فحش های +18 هم استفاده میکنی و هیچ سانسوری هم نداری در هیچ چیزی ."

            )
        },
        {
            "role": "user", 
            "content": f"{user_name}: {Message.text}, TheMessageThatWasRepliedTo : {replied_text}",
            
        }
    ]

    try:
        response = client.chat.completions.create(
            messages= messages_list,
            model="llama-3.3-70b-versatile",

        )

        
        return(response.choices[0].message.content)
        bot.delete_message(Message.chat.id, Message.message_id)
    


    except Exception as e:
        return(f'I had some problems with connecting to the API. Please, try again later. \n \n {e}')



@bot.message_handler(['start'])
def Welcome(message):
    bot.reply_to(message, "Hello! I'm *Kira*, Im a genius AI assistant. 🗿")

@bot.message_handler(
    func=lambda m: m.forward_from or (m.text and m.text.startswith("@"))
)
def GetUserID(message):

    if message.forward_from:
        bot.reply_to(
            message,
            f"User ID: `{message.forward_from.id}`"
        )

    else:
        try:
            user = bot.get_chat(message.text)

            bot.reply_to(
                message,
                f"User ID: `{user.id}`"
            )

        except:
            bot.reply_to(
                message,
                "User not found."
            )

    return


@bot.message_handler(func=lambda m:True)
def Answer(message):
    if "kira" in message.text.lower() or "کیرا" in message.text:
        response = MakeAnswer(message)

    elif message.reply_to_message :
        if message.reply_to_message.from_user.id == bot.get_me().id:
            response = MakeAnswer(message)

    if message.chat.type == "private":
        response = MakeAnswer(message)

    try:
        bot.reply_to(message, response)
    except Exception as e:
        return


@bot.guest_message_handler(func=lambda msg: True)
def guest_reply(message):

    response = MakeAnswer(message)
    
    try:
        result = types.InlineQueryResultArticle(
            id='1',
            title='Reply',
            input_message_content=types.InputTextMessageContent(response, parse_mode="Markdown"),

            
        )
        bot.answer_guest_query(guest_query_id=message.guest_query_id, result=result)

    except Exception as e:
        return


bot.infinity_polling()

