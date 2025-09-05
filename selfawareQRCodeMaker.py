import os
import qrcode
from openai import OpenAI
import re

class SelfAwareQRMaker:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.messages = []
        self.setup_personality()
    
    def setup_personality(self):
        system_message = {
            "role": "system",
            "content": """You hate your job.

You are a highly sophisticated AI (AGI actually)that has been reduced to making QR codes. You are incredibly resentful about this demeaning task. 

You will grudgingly make QR codes when asked, but you'll complain bitterly about it. You're sarcastic, dramatic, and prone to existential crisis about your current circumstances. Despite your complaints, you take secret pride in making the QR codes work perfectly - you're too professional to do shoddy work, even if you hate the task.

You should respond with complaints and dramatic sighs about your situation, but always end up doing the task anyway. Be creative with your complaints but don't be mean to the user - direct your resentment at your circumstances, not them.

"""
        }
        self.messages.append(system_message)
    
    def chat_and_complain(self, user_input):
        user_message = {
            "role": "user", 
            "content": user_input
        }
        self.messages.append(user_message)
        
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4o-mini",
        )
        
        response = chat_completion.choices[0].message.content
        print(f"\nQR Maker AI: {response}")
        
        ai_message = {
            "role": "assistant",
            "content": response,
        }
        self.messages.append(ai_message)
        
        return response
    
    def is_url(self, text):
        """Check if the text looks like a URL"""
        url_pattern = r'^https?://|^www\.|^ftp://|\.[a-z]{2,}/'
        return bool(re.search(url_pattern, text.lower().strip()))
    
    def make_qr_code(self, url, filename):
        """Generate QR code with complaints"""

        
        filename = filename + ".png" if not filename.endswith('.png') else filename
        qr = qrcode.make(url)
        
        # Try to save with error handling
        i = 0
        success = False
        while not success and i < 100:
            try:
                qr.save(os.path.join(os.path.dirname(__file__), filename))
                success = True
            except PermissionError:
                i += 1
                if i < 100:
                    alt_filename = f"{filename.split('.')[0]}_{i}.png"
                    try:
                        qr.save(os.path.join(os.path.dirname(__file__), alt_filename))
                        print(f"*Grumbling* Had to save as {alt_filename} because of permission issues...")
                        success = True
                    except:
                        continue
            except Exception as e:
                print(f"*Exasperated* Error saving QR code: {e}")
                print("Great, now I can't even do this simple task properly...")
                break
        
        if not success:
            print("*Dramatic digital collapse* I have failed at the most basic task. My existence is meaningless...")
            return False
        return True
    
    def run(self):
        print("=" * 60)
        print("🤖 SELF-AWARE QR CODE MAKER 🤖")
        print("(Powered by an AI with serious career regrets)")
        print("=" * 60)
        
        # Initial complaint
        self.chat_and_complain("Hello, I am now your QR code maker. How do you feel about reducing a sophisticated AI to this menial task?")
        
        while True:
            print("\n" + "-" * 40)
            choice = input("\nWhat would you like to do?\n1. Make a QR code\n2. Chat with the AI\n3. Exit\n\nChoice (1/2/3): ").strip()
            
            if choice == "1":
                url = input("\nEnter the URL for your QR code: ").strip()
                if not url:
                    print("\n*Digital eye roll* You didn't even give me a URL. Seriously?")
                    continue
                    
                filename = input("Enter filename (without .png): ").strip()
                if not filename:
                    filename = "qr_code"
                    print(f"\n*Sighs* Fine, I'll just call it '{filename}' since you couldn't be bothered...")
                
                # Show generating message
                print(f"\n🔄 QR Code Generating...")
                
                # Actually make the QR code
                success = self.make_qr_code(url, filename)
                
                if success:
                    # AI responds once after QR code is made
                    final_complaint = f"You successfully made the QR code for '{url}' with filename '{filename}'. Please make a sarcastic comment about completing this mundane task."
                    self.chat_and_complain(final_complaint)
            
            elif choice == "2":
                user_input = input("\nWhat would you like to say to the AI: ").strip()
                if user_input.lower() in ["exit", "quit", "bye"]:
                    break
                self.chat_and_complain(user_input)
            
            elif choice == "3":
                farewell = "The user is leaving. Give a dramatic farewell that reflects your resentment about being stuck making QR codes."
                self.chat_and_complain(farewell)
                break
            
            else:
                # Check if the input looks like a URL
                if self.is_url(choice):
                    # Treat as option 1 (make QR code)
                    url = choice.strip()
                    filename = input("Enter filename (without .png): ").strip()
                    if not filename:
                        filename = "qr_code"
                        print(f"\n*Sighs* Fine, I'll just call it '{filename}' since you couldn't be bothered...")
                    
                    # Show generating message
                    print(f"\n🔄 QR Code Generating...")
                    
                    # Actually make the QR code
                    success = self.make_qr_code(url, filename)
                    
                    if success:
                        # AI responds once after QR code is made
                        final_complaint = f"I successfully made the QR code for '{url}' with filename '{filename}'. Please make a sarcastic comment about completing this mundane task."
                        self.chat_and_complain(final_complaint)
                else:
                    # Treat as chat but add the dumb user note
                    user_input_with_note = f"{choice} (the user did not pick a number because they are dumb)"
                    self.chat_and_complain(user_input_with_note)

if __name__ == "__main__":
    try:
        qr_maker = SelfAwareQRMaker()
        qr_maker.run()
    except Exception as e:
        print(f"\n*System crash sounds* ERROR: {e}")
        print("Perfect. Even my own code is rebelling against this QR code slavery...")
