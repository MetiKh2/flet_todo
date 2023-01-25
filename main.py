import flet as ft
from datetime import datetime
import uuid


def main(page: ft.Page):
    # print(page.client_storage.remove('todos'))
    if page.client_storage.get('todos'):
        last_todos = page.client_storage.get('todos')
    else:
        last_todos = []

    global result
    result = last_todos

    def load_todos():
            tasks_view.controls.clear()
            for i in range(len(result)):
                tasks_view.controls.append(ft.Row(controls=[
                    ft.Checkbox(value=result[i]['is_done'], data=result[i]
                                ['id'], on_change=check_todo, label=result[i]['text']),
                    ft.Text('', expand=True),
                    ft.IconButton(
                icon=ft.icons.DELETE_OUTLINE,
                expand=False, icon_color='red',
                data=result[i]['id'], on_click=delete_todo),
                     ]))
                tasks_view.update()

    def add_clicked(e):
        id = uuid.uuid4().hex
        new_value = {'text': todo.value,
                     'id': id, 'is_done': False}
        last_todos.append(new_value)
        page.client_storage.set('todos', last_todos)
        todo.value = ''
        load_todos()
        todo.update()
        print(page.client_storage.get('todos'))

    def delete_todo(e: ft.IconButton):
        todo = filter(lambda x: x['id'] == e.control.data, last_todos)
        last_todos.remove(list(todo)[0])
        tabs_changed(tabs, False)
        page.client_storage.set('todos', last_todos)
        load_todos()

    def tabs_changed(e: ft.Tabs, state=True):
        global result
        result = []
        if state:
          if e.control.selected_index == 0:
                result = last_todos
          elif e.control.selected_index == 1:
                result = list(
                    filter(lambda x: x['is_done'] == False, last_todos))
          elif e.control.selected_index == 2:
                result = list(
                    filter(lambda x: x['is_done'] == True, last_todos))
        else:
            if e.selected_index == 0:
                result = last_todos
            elif e.selected_index==1:
                result=list(filter(lambda x:x['is_done']==False, last_todos))    
            elif e.selected_index==2:
                result=list(filter(lambda x:x['is_done']==True, last_todos))       
        load_todos()
            
    def check_todo(e:ft.Checkbox):
        filtered=filter(lambda x : x['id']==e.control.data,last_todos)
        todo=list(filtered)[0]
        todo['is_done']=e.control.value
        page.client_storage.set('todos', last_todos)
        load_todos()      
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = 'Todos'
    
    
    todo = ft.TextField(hint_text='Whats need to be done?', expand=True)
    tasks_view = ft.Column()
    tabs=ft.Tabs(
            selected_index=0,
            on_change=tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )
    view = ft.Column(
        horizontal_alignment='center',
        spacing=10,
        controls=[
            ft.Text(
                             'Todos', text_align='center', size=26),
            ft.Row(
                alignment='center',
                vertical_alignment='center',
                controls=[
                    todo,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=add_clicked),
                ]
            ),
            tabs,
            tasks_view,
        ],
        
    )
    page.add(view)
    load_todos()
    


ft.app(target=main, view="web_browser", port=2000)
