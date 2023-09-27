


from pyrogram import Client

app = Client("My First Project",api_id=24541704,api_hash="7b1b63a5c5a2e53233a0e78727c068d3",bot_token="6667225591:AAEjt37G8XZSRl2aujX7dLamzdvPJZk_1Y4")

async def main():
    await app.start()
    await app.send_message(689061386, "Hello! Bro Whatsup")
    await app.stop()
app.run(main())
