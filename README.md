# ClipGemAi

## About

I was annoyed that MS PowerToys doesn't allow use of Google Gemini API so I created this python to handle this.

## Installation

Follow these steps to set up ClipGemAi locally:  

1. Clone the repository:  
   ```bash
   git clone https://github.com/AlexJankowski/ClipGemAi.git

2. Install the required dependencies using pip:
     ```bash
   pip install -r requirement.txt
3. Set up your API keys:
    ```bash
    GEMINI_API_KEY = "your_gemini_api_key"
    SELECTED_MODEL = "gemini-2.0-flash"  # Choose your desired model
4. Run python
   ```bash
   python main.py

* . Optionally you can copile the code to .exe
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole main.py

* . You can further add this to your startup so it works right after you boot up your pc
   ```bash
   win+R
   shell:startup
   place created .exe file in the folder

## HOW TO USE

Default shortcut to open ClipGemAi is shift+win+v (you can change it at the bottom of main.py)

1.a Select text you want Gemini to process and use shortcut the popup should appear 
![image](https://github.com/user-attachments/assets/1021861f-e927-4732-92ac-2311b0fb9c98)

1.b It also works if nothing was selected but you need to enter prompt in the popup's textbox
![image](https://github.com/user-attachments/assets/9a56b04f-b8e8-40d5-8ff3-535f1b1b5987)

2. Press Enter and AI will generate generate answer (by default answer is set up to be concise but you can change it in code under fetch_ai_response)  
![image](https://github.com/user-attachments/assets/3d817e98-cb5a-48c5-b81a-52ba0ef80ab5)

3.a Press Enter or Paste on Cursor button to paste answer on cursor (program remembers location of your cursor when opening popup)
![image](https://github.com/user-attachments/assets/79722aa5-5a22-4f1b-bb2e-a5a0b91e9292)

3.b Alternatively you can copy answer to your clipboard to use it somewhere else (ctrl+c or Coppy To Clipboard button)
   
