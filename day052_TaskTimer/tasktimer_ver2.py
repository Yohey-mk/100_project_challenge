# tasktimer_ver2.py

# for packaging
# pyinstaller --onefile --noconsole --name TaskTracker --collect-all flet_desktop --clean --noconfirm tasktimer_ver2.py

import flet as ft
import asyncio
import json
from datetime import datetime, date

async def main(page: ft.Page):
    page.title = "TaskTracker"
    page.window.width = 300
    page.window.height = 550
    page.theme_mode = "LIGHT"
    page.window.always_on_top = True

    # --- 1. 状態管理 ---
    task_history = []
    active_session = None
    current_seconds = 0
    # 内部ステータス: "READY", "RUNNING", "PAUSED"
    app_status = "READY"
    task_items = []

    # --- 💾 データのロード ---
    async def load_data():
        nonlocal task_history, task_items, summary_task_field
        saved_str = await ft.SharedPreferences().get("task_history")
        saved_task_items = await ft.SharedPreferences().get("task_items")

        if saved_str:
            task_history = json.loads(saved_str)

        if saved_task_items:
            loaded_items = json.loads(saved_task_items)
            # 読み込んだデータがリスト型かチェックする
            if isinstance(loaded_items, list):
                task_items = loaded_items
            else:
                task_items = [] #文字列などおかしなデータの場合はリセット
    
    await load_data()

    # --- 🕰️ ヘルパー関数 ---
    def get_formatted_time(seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    # --- 🔄 タイマーロジック ---
    async def timer_tick():
        nonlocal current_seconds
        while True:
            if app_status == "RUNNING":
                current_seconds += 1
                timer_text.value = get_formatted_time(current_seconds)
                page.update()
            await asyncio.sleep(1)

    # --- 🎮 ボタン制御ロジック ---
    def update_ui_state():
        # ステータスに応じてボタンの有効・無効を切り替え
        start_btn.visible = (app_status == "READY")
        pause_btn.visible = (app_status == "RUNNING")
        resume_btn.visible = (app_status == "PAUSED")
        finish_btn.visible = (app_status in ["RUNNING", "PAUSED"])
        
        task_dropdown.disabled = (app_status != "READY")
        status_label.value = f"Status: {app_status}"
        page.update()

    async def handle_start(e):
        nonlocal active_session, current_seconds, app_status
        if task_dropdown.value == "Select task":
            page.show_dialog(ft.SnackBar(ft.Text("タスクを選択してください")))
            return
        
        now = datetime.now()
        active_session = {
            "date": now.strftime("%Y-%m-%d"),
            "task": task_dropdown.value,
            "start_time": now.strftime("%H:%M:%S"),
            "pauses": [],
            "end_time": "",
            "duration_seconds": 0
        }
        current_seconds = 0
        app_status = "RUNNING"
        update_ui_state()

    async def handle_pause(e):
        nonlocal app_status
        if active_session is None: return

        now = datetime.now().strftime("%H:%M:%S")
        active_session["pauses"].append({"start": now, "end": ""})
        print("PAUSE追加:", active_session["pauses"])
        app_status = "PAUSED"
        update_ui_state()

    async def handle_resume(e):
        nonlocal app_status
        if active_session is None: return

        now = datetime.now().strftime("%H:%M:%S")
        if active_session["pauses"]:
            active_session["pauses"][-1]["end"] = now
        print("END追加:", active_session["pauses"])
        app_status = "RUNNING"
        update_ui_state()

    async def handle_finish(e):
        nonlocal active_session, app_status, task_history
        now = datetime.now()
        if active_session is None: return
        
        # もし一時停止中にFINISHされたら、最後のPAUSEを閉じる
        if app_status == "PAUSED" and active_session["pauses"]:
            active_session["pauses"][-1]["end"] = now.strftime("%H:%M:%S")
            
        active_session["end_time"] = now.strftime("%H:%M:%S")
        active_session["duration_seconds"] = current_seconds
        
        # 履歴に保存
        task_history.append(active_session)
        await ft.SharedPreferences().set("task_history", json.dumps(task_history))
        
        # リセット
        app_status = "READY"
        active_session = None
        timer_text.value = "00:00:00"
        page.show_dialog(ft.SnackBar(ft.Text("記録を完了しました！")))
        update_ui_state()

    # --- 📊 UIコンポーネント ---
    aot_switch = ft.Switch(label="Always On Top", value=True, scale=0.9)
    def toggle_aot(e):
        page.window.always_on_top = e.control.value
        page.update()
    aot_switch.on_change = toggle_aot

    # Options for Dropdown
    initial_options = task_items if task_items else ["SE", "Reporting", "External_Meeting", "Internal_Meeting", "Training", "Other tasks", "Short Break"]

    task_dropdown = ft.Dropdown(
        value="Select task",
        options=[ft.DropdownOption(task) for task in initial_options],
        width=250
    )

    set_task = ft.TextField(hint_text="Enter task name")
    #task_list = ft.Container(content=[task_items])
    summary_task_field = ft.TextField(
        value="\n".join(task_items),
        multiline=True, read_only=True, visible=True, height=300)
    
    # 編集モード切替用のボタン
    edit_list_btn = ft.Button("EDIT", icon=ft.Icons.EDIT)
    save_list_btn = ft.Button("SAVE", icon=ft.Icons.SAVE, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, visible=False)
    cancel_list_btn = ft.Button("CANCEL", icon=ft.Icons.CANCEL, visible=False)

    async def handle_task_list(e):
        task = set_task.value

        # 空文字の場合は処理を中断する（ガード処理）
        if not task:
            return
        
        if task not in task_items:
            task_items.append(task)
            task_dropdown.options = [ft.DropdownOption(t) for t in task_items]

        # task_items全体をJSON化して保存する
        await ft.SharedPreferences().set("task_items", json.dumps(task_items))
        # task_itemsの中身を改行で結合して表示する
        summary_task_field.value = "\n".join(task_items)
        set_task.value = ""
        page.update()

    async def handle_edit(e):
        summary_task_field.read_only = False
        edit_list_btn.visible = False
        save_list_btn.visible = True
        cancel_list_btn.visible = True
        page.update()
    
    async def handle_cancel(e):
        #キャンセル時は保存されている元のtask_itemsに表示を戻す
        summary_task_field.value = "\n".join(task_items)
        #閲覧モードに戻す
        summary_task_field.read_only =True
        edit_list_btn.visible = True
        save_list_btn.visible = False
        cancel_list_btn.visible = False
        page.update()

    async def handle_save(e):
        nonlocal task_items

        raw_text = summary_task_field.value
        # 新しいリストを作成
        new_task_list = [x for x in raw_text.split("\n") if x != ""]
        # task_list自体を新しいリストで上書き
        task_items = new_task_list
        # ローカルストレージに保存
        await ft.SharedPreferences().set("task_items", json.dumps(new_task_list))
        # 最新のtask_itemsを使ってドロップダウンを更新
        task_dropdown.options = [ft.DropdownOption(t) for t in task_items]
        page.show_dialog(ft.SnackBar(ft.Text("タスクリストを更新しました！")))

        summary_task_field.read_only = True
        edit_list_btn.visible = True
        save_list_btn.visible = False
        cancel_list_btn.visible = False
        page.update()


    edit_list_btn.on_click = handle_edit
    save_list_btn.on_click = handle_save
    cancel_list_btn.on_click = handle_cancel

#    async def edit_task_list(e):
#        for task in task_items:
#            btn = ft.TextButton(
#                content=ft.Text(task),
#                on_click=lambda e, t=task: None,
#                icon_color=ft.Colors.RED,
#            )
#            file_list_column.controls.append(btn)
#
#        page.update()
#
#    # task編集スペース
#    edit_textfield = ft.TextField(label="新しいタスク名")
#    editing_index = -1 #現在編集しているタスクのリスト内番号を記録する変数
#
#    async def save_edited_task(e):
#        nonlocal editing_index
#        new_task_name = edit_textfield.value
#        task_items[editing_index].value = new_task_name
#        await ft.SharedPreferences().set("task_items", new_task_name)
#        task_dropdown.options = [ft.DropdownOption(t) for t in task_items]
#        await render_task_list()
#        page.update()
#
#    async def render_task_list():
#        file_list_column.controls.clear()
#
#        for i, task in enumerate(task_items):
#            task_row = ft.Row(controls=[
#                ft.Text(f"{i}: "),
#                ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_task_list)
#            ])
#        file_list_column.controls.append(task_row)
#
#        page.update()
#
#    file_list_column = ft.Column(scroll="auto", expand=True, tight=True)
#    file_list_container = ft.Container(
#        content=ft.Column(
#            controls=[file_list_column],
#            scroll=ft.ScrollMode.ALWAYS,
#        ),
#        height=100,
#        #width=500,
#        padding=10,
#        border=ft.Border.all(2, ft.Colors.GREY_600),
#        border_radius=ft.BorderRadius.all(10),
#        expand=True,
#    )

    set_task_btn = ft.TextButton("Set", on_click=handle_task_list)
#    edit_task_btn = ft.Button("EDIT", icon=ft.Icons.EDIT, on_click=edit_task_list)

    timer_text = ft.Text("00:00:00", size=45, weight="bold")
    status_label = ft.Text("Status: READY", color=ft.Colors.GREY_700)

    start_btn = ft.Button("START", icon=ft.Icons.PLAY_ARROW, on_click=handle_start, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, width=200)
    pause_btn = ft.Button("PAUSE", icon=ft.Icons.PAUSE, on_click=handle_pause, bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE, width=200, visible=False)
    resume_btn = ft.Button("RESUME", icon=ft.Icons.PLAY_CIRCLE, on_click=handle_resume, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=200, visible=False)
    finish_btn = ft.Button("FINISH", icon=ft.Icons.CHECK, on_click=handle_finish, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, width=200, visible=False)

    summary_text_field = ft.TextField(multiline=True, read_only=True, visible=True, height=100, text_size=11)

    async def toggle_summary(e):
        summary_text_field.visible = summary_text_field.visible
        if summary_text_field.visible:
            lines = ["Date\tTask\tStart\tEnd\tPauses\tDuration"]
            for s in task_history:
                pauses_str = ", ".join(
                    f"{p['start']}\t{p['end'] if p['end'] else '...'}"
                    for p in s.get("pauses", [])
                )
                lines.append(f"{s['date']}\t{s['task']}\t{s['start_time']}\t{s['end_time']}\t{pauses_str}\t{get_formatted_time(s['duration_seconds'])}")
            summary_text_field.value = "\n".join(lines)
            await ft.Clipboard().set(summary_text_field.value)
            page.show_dialog(ft.SnackBar(ft.Text("コピーしました！")))
        page.update()

    async def reset_history(e):
        task_history.clear()
        await ft.SharedPreferences().set("task_history", "[]")
        page.update()

    # Datetime / Calendar 関連
    today = date.today().strftime('%Y-%m-%d')
    date_display = ft.Text(today, size=20)

    # --- レイアウト ---

    tab_views = ft.SafeArea(
    expand=True,
    content=ft.Tabs(
        selected_index=0,
        length=3,
        content=ft.Column(
        controls=[
            ft.TabBar(
                tabs=[ft.Tab(label="Main", icon=ft.Icons.HOURGLASS_BOTTOM),
                      ft.Tab(label="Settings", icon=ft.Icons.SETTINGS),
                      ft.Tab(label="Calendar", icon=ft.Icons.CALENDAR_MONTH)]),
    
            ft.TabBarView(
                expand=True,
                controls=[
                    ft.Container(
                        content=ft.Column([
                            aot_switch,
                            date_display,
                            task_dropdown,
                            ft.Container(timer_text, padding=20),
                            status_label,
                            ft.Divider(),
                            start_btn,
                            pause_btn,
                            resume_btn,
                            ft.Container(finish_btn, margin=ft.Margin.only(top=10)),
                            ft.Divider(),
                            ft.Row([
                                ft.TextButton("📊 Log Copy", on_click=toggle_summary),
                                ft.TextButton("🗑️ Clear", on_click=reset_history)
                            ], alignment="center"),
                            summary_text_field,
                            ], horizontal_alignment="center")
                            ),
                    ft.Container(content=ft.Column([ft.Row(controls=[set_task, set_task_btn]),
                                                    ft.Row([edit_list_btn, save_list_btn, cancel_list_btn]),
                                                    summary_task_field,
                                                    ])),
                    ft.Container(content=ft.Text("Calendar Page"))
        ])])))
    
    page.add(
        tab_views,
    )

    # リセットダイアログ
    reset_dialog = ft.AlertDialog(
        title=ft.Text("履歴のリセット"),
        content=ft.Text("すべての履歴を削除しますか？"),
        actions=[
            ft.TextButton("削除", on_click=lambda _: (task_history.clear(), ft.SharedPreferences().set("task_history", "[]"), page.close(reset_dialog), page.update())),
            ft.TextButton("キャンセル", on_click=lambda _: page.close(reset_dialog))
        ]
    )

    page.run_task(timer_tick)
    update_ui_state() # 初期状態の反映

ft.run(main)