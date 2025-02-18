import asyncio
from inst_bot import *

if not os.path.exists('photos'):
    os.makedirs('photos')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
