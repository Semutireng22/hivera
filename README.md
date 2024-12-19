# Hivera Bot

## Requirements

- Python 3.8 or higher

## Usage

1. Clone this repository 
```git
git clone https://github.com/Semutireng22/hivera.git
```
2. Open folder
```
cd hivera
```
3. Install requirements.txt
```bash
pip install -r requirements.txt
```
4. Edit `data.txt` with your own token ([How to find token](#how-to-obtain-your-token))
   
5. Edit file `config.json` jika kamu membutuhkan.
   
   >**use_proxy** = change to true if you want to use a proxy
   
   >**min_power** = the minimum amount of power to be executed
   
   If you want to use a proxy, please create a file called `proxy.txt` and fill it as follows
   `http://ip:port@username:pw` or `http://ip:port`
   
6. Run script
```bash
python3 bot.py
```

7. The script will process each account, perform actions, and print results to the console.

## How to Obtain Your Token

To run the script, you'll need to get a token from the Major bot. Follow these steps to obtain your token:

1. **Login to Telegram Web**:
   - Open [web.telegram.org](https://web.telegram.org) in the Kiwi browser.

2. **Open Bot**:
   - Find and open the chat with the bot in Telegram.

3. **Access Developer Tools**:
   - Click on the three dots in the top right corner of the Major bot chat.
   - Select **"Developer Tools"** from the menu that appears.

4. **Open the Network Tab**:
   - In Developer Tools, go to the **"Network"** tab.

5. **Copy like this pict**
   >Only copy after `auth_data`
   
   ![image](https://github.com/user-attachments/assets/8eb877f0-69a6-42f4-a146-2db7d0dee77a)

6. **Done**
   Paste what you copied into the `data.txt` file

