```python
import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_API_TOKEN' with your actual bot token
API_TOKEN = 'YOUR_API_TOKEN'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me your LaTeX code and I will compile it to a PDF.')

def compile_latex(update: Update, context: CallbackContext) -> None:
    latex_code = update.message.text
    user_id = update.message.from_user.id
    file_name = f"latex_{user_id}.tex"

    with open(file_name, 'w') as f:
        f.write(latex_code)

    try:
        # Compile the LaTeX code to PDF
        subprocess.run(['pdflatex', file_name], check=True)
        pdf_file = file_name.replace('.tex', '.pdf')

        # Send the PDF file back to the user
        with open(pdf_file, 'rb') as f:
            update.message.reply_document(f)

        # Clean up the generated files
        os.remove(file_name)
        os.remove(pdf_file)
        os.remove(file_name.replace('.tex', '.log'))
        os.remove(file_name.replace('.tex', '.aux'))

    except subprocess.CalledProcessError as e:
        update.message.reply_text('There was an error compiling your LaTeX code.')

def main() -> None:
    updater = Updater(7334108575:AAHJxgC7puk3oul2gscWoJZlVH6TGW5xqN4)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, compile_latex))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

```
