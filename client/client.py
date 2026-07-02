"""
Клиентское приложение для системы Tech Support
GUI на Tkinter с использованием стандартных компонентов
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime


class TechSupportClient:
    """Главный класс клиентского приложения"""
    
    API_URL = 'http://localhost:5000/api'
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система технической поддержки")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Основные переменные
        self.current_question_id = None
        
        self.setup_ui()
        self.load_data()
        
        # Обновление каждые 30 секунд
        self.schedule_refresh()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tab_questions = ttk.Frame(self.notebook)
        self.tab_consultants = ttk.Frame(self.notebook)
        self.tab_statistics = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_questions, text="Вопросы")
        self.notebook.add(self.tab_consultants, text="Консультанты")
        self.notebook.add(self.tab_statistics, text="Статистика")
        
        self.setup_questions_tab()
        self.setup_consultants_tab()
        self.setup_statistics_tab()
    
    def setup_questions_tab(self):
        """Настройка вкладки "Вопросы" """
        paned = ttk.PanedWindow(self.tab_questions, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=2)
        
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по статусу:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['все', 'new', 'in_progress', 'resolved', 'closed'], width=15)
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.set('все')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_questions())
        
        ttk.Button(filter_frame, text="Обновить", command=self.load_questions).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Новый вопрос", command=self.show_new_question_dialog).pack(side=tk.RIGHT, padx=5)
        
        columns = ('ID', 'Статус', 'Клиент', 'Тема', 'Приоритет', 'Ответов')
        self.questions_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        self.questions_tree.column('ID', width=50, anchor='center')
        self.questions_tree.column('Статус', width=100, anchor='center')
        self.questions_tree.column('Клиент', width=130, anchor='w')
        self.questions_tree.column('Тема', width=250, anchor='w')
        self.questions_tree.column('Приоритет', width=80, anchor='center')
        self.questions_tree.column('Ответов', width=70, anchor='center')
        
        self.questions_tree.heading('ID', text='ID')
        self.questions_tree.heading('Статус', text='Статус')
        self.questions_tree.heading('Клиент', text='Клиент')
        self.questions_tree.heading('Тема', text='Тема')
        self.questions_tree.heading('Приоритет', text='Приоритет')
        self.questions_tree.heading('Ответов', text='Ответов')
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.questions_tree.yview)
        self.questions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.questions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.questions_tree.bind('<<TreeviewSelect>>', self.on_question_select)
        
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        info_frame = ttk.LabelFrame(right_frame, text="Информация о вопросе")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.question_info = tk.Text(info_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        self.question_info.pack(fill=tk.X, padx=5, pady=5)
        
        answers_frame = ttk.LabelFrame(right_frame, text="Ответы")
        answers_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.answers_text = tk.Text(answers_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.answers_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.btn_assign = ttk.Button(action_frame, text="Назначить консультанта", 
                                    command=self.show_assign_dialog, state=tk.DISABLED)
        self.btn_assign.pack(side=tk.LEFT, padx=5)
        
        self.btn_answer = ttk.Button(action_frame, text="Добавить ответ", 
                                    command=self.show_answer_dialog, state=tk.DISABLED)
        self.btn_answer.pack(side=tk.LEFT, padx=5)
        
        self.btn_resolve = ttk.Button(action_frame, text="Отметить как решенный", 
                                     command=self.resolve_question, state=tk.DISABLED)
        self.btn_resolve.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh_detail = ttk.Button(action_frame, text="Обновить", 
                                            command=self.load_question_detail)
        self.btn_refresh_detail.pack(side=tk.RIGHT, padx=5)
    
    def setup_consultants_tab(self):
        """Настройка вкладки "Консультанты" """
        top_frame = ttk.Frame(self.tab_consultants)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Добавить консультанта", 
                  command=self.show_new_consultant_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Обновить", command=self.load_consultants).pack(side=tk.LEFT, padx=5)
        
        columns = ('ID', 'Имя', 'Специализация', 'Email', 'Вопросов обработано')
        self.consultants_tree = ttk.Treeview(self.tab_consultants, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.consultants_tree.heading(col, text=col)
            self.consultants_tree.column(col, width=150)
        self.consultants_tree.column('ID', width=50)
        
        scrollbar = ttk.Scrollbar(self.tab_consultants, orient=tk.VERTICAL, command=self.consultants_tree.yview)
        self.consultants_tree.configure(yscrollcommand=scrollbar.set)
        
        self.consultants_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
    
    def setup_statistics_tab(self):
        """Настройка вкладки "Статистика" """
        stats_frame = ttk.Frame(self.tab_statistics)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.stats_text = tk.Text(stats_frame, wrap=tk.WORD, font=('Courier', 11))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(self.tab_statistics, text="Обновить статистику", 
                  command=self.load_statistics).pack(pady=10)
    
    def load_data(self):
        """Загрузка всех данных"""
        self.load_questions()
        self.load_consultants()
        self.load_statistics()
    
    def load_questions(self):
        """Загрузка списка вопросов"""
        try:
            status = self.status_filter.get()
            if status == 'все':
                status = None
            
            url = f'{self.API_URL}/questions'
            if status:
                url += f'?status={status}'
            
            response = requests.get(url)
            if response.status_code == 200:
                questions = response.json()
                self.update_questions_tree(questions)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить вопросы: {e}")
    
    def update_questions_tree(self, questions):
        """Обновление дерева вопросов"""
        for item in self.questions_tree.get_children():
            self.questions_tree.delete(item)
        
        # Статусы
        status_text = {
            'new': 'НОВЫЙ',
            'in_progress': 'В РАБОТЕ',
            'resolved': 'РЕШЕН',
            'closed': 'ЗАКРЫТ'
        }
        
        # Приоритеты
        priority_text = {
            1: 'НИЗКИЙ',
            2: 'СРЕДНИЙ', 
            3: 'ВЫСОКИЙ'
        }
        
        if not questions:
            self.questions_tree.insert('', tk.END, values=('', 'Нет вопросов', '', '', '', ''))
            return
        
        for q in sorted(questions, key=lambda x: x['id'], reverse=True):
            status = q.get('status', 'new')
            status_display = status_text.get(status, status)
            priority = q.get('priority', 1)
            priority_display = priority_text.get(priority, str(priority))
            answers_count = len(q.get('answers', []))
            
            client_name = q.get('client_name', 'Неизвестно')
            title = q.get('title', 'Без темы')
            if len(title) > 35:
                title = title[:35] + '...'
            
            self.questions_tree.insert('', tk.END, values=(
                q.get('id', ''),
                status_display,
                client_name,
                title,
                priority_display,
                answers_count
            ))
        
        self.questions_tree.update_idletasks()
    
    def on_question_select(self, event):
        """Обработка выбора вопроса"""
        selection = self.questions_tree.selection()
        if selection:
            values = self.questions_tree.item(selection[0])['values']
            if values and values[0]:
                self.current_question_id = values[0]
                self.load_question_detail()
                self.btn_assign.config(state=tk.NORMAL)
                self.btn_answer.config(state=tk.NORMAL)
                self.btn_resolve.config(state=tk.NORMAL)
    
    def load_question_detail(self):
        """Загрузка деталей вопроса"""
        if not self.current_question_id:
            return
        
        try:
            response = requests.get(f'{self.API_URL}/questions/{self.current_question_id}')
            if response.status_code == 200:
                question = response.json()
                self.display_question_detail(question)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить детали: {e}")
    
    def display_question_detail(self, question):
        """Отображение деталей вопроса"""
        status_text = {
            'new': 'НОВЫЙ',
            'in_progress': 'В РАБОТЕ',
            'resolved': 'РЕШЕН',
            'closed': 'ЗАКРЫТ'
        }
        
        priority_text = {
            1: 'НИЗКИЙ',
            2: 'СРЕДНИЙ',
            3: 'ВЫСОКИЙ'
        }
        
        status_display = status_text.get(question.get('status', 'new'), question.get('status', 'new'))
        priority_display = priority_text.get(question.get('priority', 1), str(question.get('priority', 1)))
        
        info = f"Тема: {question.get('title', 'Без темы')}\n"
        info += f"Клиент: {question.get('client_name', 'Неизвестно')}\n"
        info += f"Статус: {status_display}\n"
        info += f"Приоритет: {priority_display}\n"
        info += f"Создан: {question.get('created_at', '')[:16]}\n"
        info += f"Обновлен: {question.get('updated_at', '')[:16]}\n"
        info += f"\nОписание:\n{question.get('description', 'Нет описания')}\n"
        
        if question.get('consultant_id'):
            info += f"\nНазначен консультант ID: {question['consultant_id']}"
        else:
            info += "\nКонсультант не назначен"
        
        self.question_info.config(state=tk.NORMAL)
        self.question_info.delete(1.0, tk.END)
        self.question_info.insert(1.0, info)
        self.question_info.config(state=tk.DISABLED)
        
        self.answers_text.config(state=tk.NORMAL)
        self.answers_text.delete(1.0, tk.END)
        
        answers = question.get('answers', [])
        if answers:
            for a in answers:
                self.answers_text.insert(tk.END, f"Консультант ID {a.get('consultant_id', '?')}:\n")
                self.answers_text.insert(tk.END, f"   {a.get('content', '')}\n")
                self.answers_text.insert(tk.END, f"   {a.get('created_at', '')[:16]}\n\n")
        else:
            self.answers_text.insert(tk.END, "Нет ответов")
        
        self.answers_text.config(state=tk.DISABLED)
    
    def load_consultants(self):
        """Загрузка списка консультантов"""
        try:
            response = requests.get(f'{self.API_URL}/consultants')
            if response.status_code == 200:
                consultants = response.json()
                
                for item in self.consultants_tree.get_children():
                    self.consultants_tree.delete(item)
                
                for c in consultants:
                    self.consultants_tree.insert('', tk.END, values=(
                        c.get('id', ''),
                        c.get('name', ''),
                        c.get('specialization', ''),
                        c.get('email', ''),
                        c.get('questions_handled', 0)
                    ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить консультантов: {e}")
    
    def load_statistics(self):
        """Загрузка статистики"""
        try:
            response = requests.get(f'{self.API_URL}/statistics')
            if response.status_code == 200:
                stats = response.json()
                
                status_rus = {
                    'new': 'Новые',
                    'in_progress': 'В работе',
                    'resolved': 'Решенные',
                    'closed': 'Закрытые'
                }
                
                text = "=" * 50 + "\n"
                text += "     СТАТИСТИКА СИСТЕМЫ ТЕХПОДДЕРЖКИ\n"
                text += "=" * 50 + "\n\n"
                
                text += f"Всего вопросов:     {stats.get('total_questions', 0)}\n"
                text += f"Решено вопросов:    {stats.get('resolved_count', 0)}\n"
                text += f"Консультантов:      {stats.get('consultants_count', 0)}\n"
                text += f"Всего ответов:      {stats.get('answers_count', 0)}\n\n"
                
                text += "Распределение по статусам:\n"
                for status, count in stats.get('by_status', {}).items():
                    status_name = status_rus.get(status, status)
                    text += f"  {status_name}: {count}\n"
                
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить статистику: {e}")
    
    def show_new_question_dialog(self):
        """Диалог создания нового вопроса"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый вопрос")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Клиент:").pack(anchor=tk.W, padx=10, pady=5)
        client_entry = ttk.Entry(dialog, width=50)
        client_entry.pack(padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Тема:").pack(anchor=tk.W, padx=10, pady=5)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.pack(padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Описание:").pack(anchor=tk.W, padx=10, pady=5)
        desc_text = scrolledtext.ScrolledText(dialog, height=8)
        desc_text.pack(padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(dialog, text="Приоритет:").pack(anchor=tk.W, padx=10, pady=5)
        priority_var = tk.IntVar(value=1)
        priority_frame = ttk.Frame(dialog)
        priority_frame.pack(padx=10, pady=5)
        ttk.Radiobutton(priority_frame, text="НИЗКИЙ", variable=priority_var, value=1).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(priority_frame, text="СРЕДНИЙ", variable=priority_var, value=2).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(priority_frame, text="ВЫСОКИЙ", variable=priority_var, value=3).pack(side=tk.LEFT, padx=10)
        
        def submit():
            data = {
                'client_name': client_entry.get().strip(),
                'title': title_entry.get().strip(),
                'description': desc_text.get(1.0, tk.END).strip(),
                'priority': priority_var.get()
            }
            
            if not all([data['client_name'], data['title'], data['description']]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                response = requests.post(f'{self.API_URL}/questions', json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Успех", "Вопрос создан")
                    dialog.destroy()
                    self.load_questions()
                else:
                    error = response.json().get('error', 'Неизвестная ошибка')
                    messagebox.showerror("Ошибка", f"Не удалось создать вопрос: {error}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать вопрос: {e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Создать", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_new_consultant_dialog(self):
        """Диалог добавления консультанта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый консультант")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Имя:").pack(anchor=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Специализация:").pack(anchor=tk.W, padx=10, pady=5)
        spec_entry = ttk.Entry(dialog, width=40)
        spec_entry.pack(padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Email:").pack(anchor=tk.W, padx=10, pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.pack(padx=10, fill=tk.X)
        
        def submit():
            data = {
                'name': name_entry.get().strip(),
                'specialization': spec_entry.get().strip(),
                'email': email_entry.get().strip()
            }
            
            if not all(data.values()):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                response = requests.post(f'{self.API_URL}/consultants', json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Успех", "Консультант добавлен")
                    dialog.destroy()
                    self.load_consultants()
                else:
                    error = response.json().get('error', 'Неизвестная ошибка')
                    messagebox.showerror("Ошибка", f"Не удалось добавить консультанта: {error}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить консультанта: {e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Добавить", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_assign_dialog(self):
        """Диалог назначения консультанта"""
        if not self.current_question_id:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Назначить консультанта")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Выберите консультанта:").pack(pady=10)
        
        try:
            response = requests.get(f'{self.API_URL}/consultants')
            consultants = response.json() if response.status_code == 200 else []
        except:
            consultants = []
        
        consultant_var = tk.StringVar()
        consultant_combo = ttk.Combobox(dialog, textvariable=consultant_var, 
                                       values=[f"{c['id']}: {c['name']} ({c['specialization']})" 
                                              for c in consultants],
                                       width=40)
        consultant_combo.pack(pady=5)
        
        def assign():
            if not consultant_var.get():
                messagebox.showerror("Ошибка", "Выберите консультанта")
                return
            
            consultant_id = int(consultant_var.get().split(':')[0])
            
            try:
                response = requests.put(
                    f'{self.API_URL}/questions/{self.current_question_id}/assign',
                    json={'consultant_id': consultant_id}
                )
                if response.status_code == 200:
                    messagebox.showinfo("Успех", "Консультант назначен")
                    dialog.destroy()
                    self.load_questions()
                    self.load_question_detail()
                else:
                    error = response.json().get('error', 'Неизвестная ошибка')
                    messagebox.showerror("Ошибка", f"Не удалось назначить: {error}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось назначить: {e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Назначить", command=assign).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_answer_dialog(self):
        """Диалог добавления ответа"""
        if not self.current_question_id:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить ответ")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="ID консультанта:").pack(anchor=tk.W, padx=10, pady=5)
        consultant_entry = ttk.Entry(dialog, width=20)
        consultant_entry.pack(padx=10, anchor=tk.W)
        
        ttk.Label(dialog, text="Текст ответа:").pack(anchor=tk.W, padx=10, pady=5)
        answer_text = scrolledtext.ScrolledText(dialog, height=8)
        answer_text.pack(padx=10, fill=tk.BOTH, expand=True)
        
        def submit():
            try:
                consultant_id = int(consultant_entry.get().strip())
                content = answer_text.get(1.0, tk.END).strip()
                
                if not content:
                    messagebox.showerror("Ошибка", "Введите текст ответа")
                    return
                
                data = {
                    'question_id': self.current_question_id,
                    'consultant_id': consultant_id,
                    'content': content
                }
                
                response = requests.post(f'{self.API_URL}/answers', json=data)
                if response.status_code == 201:
                    messagebox.showinfo("Успех", "Ответ добавлен")
                    dialog.destroy()
                    self.load_questions()
                    self.load_question_detail()
                else:
                    error = response.json().get('error', 'Неизвестная ошибка')
                    messagebox.showerror("Ошибка", f"Не удалось добавить ответ: {error}")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректный ID консультанта")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить ответ: {e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Отправить", command=submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def resolve_question(self):
        """Отметить вопрос как решенный"""
        if not self.current_question_id:
            return
        
        if not messagebox.askyesno("Подтверждение", "Отметить вопрос как решенный?"):
            return
        
        try:
            response = requests.put(f'{self.API_URL}/questions/{self.current_question_id}/resolve')
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Вопрос отмечен как решенный")
                self.load_questions()
                self.load_question_detail()
            else:
                error = response.json().get('error', 'Неизвестная ошибка')
                messagebox.showerror("Ошибка", f"Не удалось отметить: {error}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отметить: {e}")
    
    def schedule_refresh(self):
        """Периодическое обновление данных"""
        self.load_questions()
        self.root.after(30000, self.schedule_refresh)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == '__main__':
    client = TechSupportClient()
    client.run()