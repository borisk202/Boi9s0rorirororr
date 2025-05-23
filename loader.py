import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import threading

# Цветовая схема
BG_COLOR = "#FFFFFF"
FG_COLOR = "#FF0000"
HEADER_COLOR = "#FF0000"

# Список сайтов для поиска
sites = [
    {
        'name': 'CyberSec Search',
        'url': 'https://cybersec.org/search/{}',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'IntelX Data Saver',
        'url': 'https://data.intelx.io/saverudata/',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'Reveng.ee',
        'url': 'https://reveng.ee/',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'Mobile Location',
        'url': 'https://mobile-location.org/punch-phone-number/{}',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': '8sot.su Codes7',
        'url': 'https://8sot.su/ru/codes7',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'Check Usernames',
        'url': 'https://checkusernames.com/',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'Namechk',
        'url': 'https://namechk.com/',
        'parser': lambda html: "Результаты не реализованы"  # Заглушка
    },
    {
        'name': 'Telegram1.txt (GitHub)',
        'url': '',  # Не нужен запрос, просто вывод содержимого файла
        'parser': lambda html: html,
        'content_url': 'https://raw.githubusercontent.com/rivkos/BorsBio/refs/heads/main/Telegram1.txt'
    },
    {
        'name': 'Telegram.txt (GitHub)',
        'url': '',
        'parser': lambda html: html,
        'content_url': 'https://raw.githubusercontent.com/rivkos/BorsBio/refs/heads/main/Telegram.txt'
    },
    {
        'name':='Data.txt (GitHub)',
       ='url':'', 
        ='parser'=lambda html:html,
        ='content_url':'https://raw.githubusercontent.com/rivkos/BorsBio/main/data.txt'
     }
]

# Функции парсинга (заглушки или простые)
def parse_simple(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(strip=True)[:500] + ('...' if len(soup.get_text()) > 500 else '')

# Основная функция поиска по сайту
def search_site(site, phone):
    try:
        if site.get('content_url'):
            response = requests.get(site['content_url'], timeout=10)
            if response.status_code == 200:
                return site['parser'](response.text)
            else:
                return f"Ошибка загрузки файла {site['name']}"
        elif site['url']:
            url = site['url'].format(phone)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return site['parser'](response.text)
            else:
                return f"Ошибка {response.status_code}"
        else:
            return "Нет URL для поиска"
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Обработчик поиска (в отдельном потоке)
def start_search():
    phone = entry_phone.get().strip()
    if not phone:
        messagebox.showwarning("Внимание", "Пожалуйста, введите номер телефона")
        return

    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, f"🔍 Поиск по номеру: {phone}\n\n")
    
    def run():
        for site in sites:
            text_result.insert(tk.END, f"--- {site['name']} ---\n")
            result = search_site(site, phone)
            text_result.insert(tk.END, result + "\n\n")
    
    threading.Thread(target=run).start()

# Создание GUI
root = tk.Tk()
root.title("XAC3 SOFT - Поиск по номерам")
root.geometry("800x600")
root.configure(bg=BG_COLOR)

# Баннер
banner_frame = tk.Frame(root, bg=HEADER_COLOR)
banner_frame.pack(fill=tk.X)

banner_label = tk.Label(banner_frame, text="XAC3 SOFT", font=("Arial", 24, "bold"), bg=HEADER_COLOR, fg=BG_COLOR)
banner_label.pack(pady=10)

# Ввод номера телефона
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

label_prompt = tk.Label(input_frame, text="Введите номер телефона:", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR)
label_prompt.pack(side=tk.LEFT, padx=5)

entry_phone = tk.Entry(input_frame, font=("Arial", 14), width=30)
entry_phone.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(input_frame, text="Поиск", font=("Arial", 14), bg=FG_COLOR, fg=BG_COLOR,
                          command=start_search)
search_button.pack(side=tk.LEFT, padx=5)

# Результат поиска
result_frame = tk.Frame(root, bg=BG_COLOR)
result_frame.pack(fill=tk.BOTH, expand=True)

text_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
text_result.pack(fill=tk.BOTH, expand=True)

root.mainloop()
