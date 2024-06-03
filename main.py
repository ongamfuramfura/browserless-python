import asyncio
import random
import json
import os
from tabulate import tabulate
from pyppeteer import launch

config = json.load(open('./config.json'))

sources = [
  'https://webminer.pages.dev/'
]

# Function to clear the console
def clear_console():
    # Clear console command for Windows and Unix-based systems
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)

def random_source():
    return random.choice(sources)

async def print_progress(msg):
    clear_console()
    
    table = []
    for algo, stats in msg.items():
        table.append([algo, stats['Hashrate'], stats['Shared']])

    print('* Versions:   browserless-python-1.0.0')
    print('* Author:     malphite-code')
    print('* Donation:   BTC: bc1qzqtkcf28ufrr6dh3822vcz6ru8ggmvgj3uz903')
    print('              RVN: RVZD5AjUBXoNnsBg9B2AzTTdEeBNLfqs65')
    print('              LTC: ltc1q8krf9g60n4q6dvnwg3lg30lp5e7yfvm2da5ty5')
    print(' ')
    print(tabulate(table, headers=['Algorithm', 'Hashrate', 'Shared']))

async def main():
    retries = 50
    while retries > 0:
        try:
            browser = await launch({
                "headless": True,
                "args": [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--ignore-certificate-errors',
      '--ignore-certificate-errors-spki-list',
      '--disable-gpu',
      '--disable-infobars',
      '--window-position=0,0',                                  
      '--ignore-certifcate-errors',
      '--ignore-certifcate-errors-spki-list',
      '--disable-speech-api',
      '--disable-background-networking',
      '--disable-background-timer-throttling',
      '--disable-backgrounding-occluded-windows',
      '--disable-breakpad',
      '--disable-client-side-phishing-detection',
      '--disable-component-update',
      '--disable-default-apps',
      '--disable-dev-shm-usage',                               
      '--disable-domain-reliability',
      '--disable-extensions',
      '--disable-features=AudioServiceOutOfProcess',
      '--disable-hang-monitor',
      '--disable-ipc-flooding-protection',
      '--disable-notifications',
      '--disable-offer-store-unmasked-wallet-cards',
      '--disable-popup-blocking',
      '--disable-print-preview',
      '--disable-prompt-on-repost',
      '--disable-renderer-backgrounding',
      '--disable-setuid-sandbox',
      '--disable-sync',
      '--hide-scrollbars',
      '--ignore-gpu-blacklist',
      '--metrics-recording-only',
      '--mute-audio',
      '--no-default-browser-check',
      '--no-first-run',
      '--no-pings',
      '--no-sandbox',
      '--no-zygote',
      '--password-store=basic',
      '--use-gl=swiftshader',
      '--use-mock-keychain',
      '--incognito'
                ],
                "ignoreHTTPSErrors": True
            })
            pages = {}
            source = random_source()

            for index, params in enumerate(config):
                query = '&'.join([f"{key}={value}" for key, value in params.items()])
                url = f"{source}?{query}"
                print(f"Browser Restart: {url}")
                page = await browser.newPage()
                await page.goto(url)
                pages[f"{params['algorithm']}_{index}"] = page

            while True:
                msg = {}
                for algo, page in pages.items():
                    try:
                        hashrate = await page.querySelectorEval('#hashrate', 'el => el.innerText')
                        shared = await page.querySelectorEval('#shared', 'el => el.innerText')
                        msg[algo] = {'Hashrate': hashrate or '0 H/s', 'Shared': int(shared) if shared else 0}
                    except Exception as e:
                        print(f"[{retries}] Miner Restart: {e}")
                        retries -= 1
                        break
                await print_progress(msg)
                await asyncio.sleep(6)

        except Exception as e:
            print(f"[{retries}] Miner Restart: {e}")
            retries -= 1

asyncio.get_event_loop().run_until_complete(main())
