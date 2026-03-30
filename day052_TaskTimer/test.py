# tasktimer.py

import flet as ft
import asyncio
import json
from datetime import datetime

async def main(page: ft.Page):
    page.title = "TaskTracker Pro"
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

    # --- 💾 データのロード ---
    async def load_data():
        nonlocal task_history
        saved_str = await ft.SharedPreferences().get("task_history")
        if saved_str:
            task_history = json.loads(saved_str)
    
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
        now = datetime.now().strftime("%H:%M:%S")
        active_session["pauses"].append({"start": now, "end": ""})
        app_status = "PAUSED"
        update_ui_state()

    async def handle_resume(e):
        nonlocal app_status
        now = datetime.now().strftime("%H:%M:%S")
        if active_session["pauses"]:
            active_session["pauses"][-1]["end"] = now
        app_status = "RUNNING"
        update_ui_state()

    async def handle_finish(e):
        nonlocal active_session, app_status, task_history
        now = datetime.now()
        
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
    task_dropdown = ft.Dropdown(
        value="Select task",
        options=[
            ft.DropdownOption("Coding"),
            ft.DropdownOption("メール作業"),
            ft.DropdownOption("休憩"),
        ], width=250
    )

    timer_text = ft.Text("00:00:00", size=45, weight="bold")
    status_label = ft.Text("Status: READY", color=ft.Colors.GREY_700)

    start_btn = ft.Button("START", icon=ft.Icons.PLAY_ARROW, on_click=handle_start, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, width=200)
    pause_btn = ft.Button("PAUSE", icon=ft.Icons.PAUSE, on_click=handle_pause, bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE, width=200, visible=False)
    resume_btn = ft.Button("RESUME", icon=ft.Icons.PLAY_CIRCLE, on_click=handle_resume, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=200, visible=False)
    finish_btn = ft.Button("FINISH", icon=ft.Icons.CHECK, on_click=handle_finish, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, width=200, visible=False)

    summary_text_field = ft.TextField(multiline=True, read_only=True, visible=False, height=100, text_size=11)

    async def toggle_summary(e):
        summary_text_field.visible = not summary_text_field.visible
        if summary_text_field.visible:
            lines = ["Date\tTask\tStart\tEnd\tDuration"]
            for s in task_history:
                lines.append(f"{s['date']}\t{s['task']}\t{s['start_time']}\t{s['end_time']}\t{get_formatted_time(s['duration_seconds'])}")
            summary_text_field.value = "\n".join(lines)
            await ft.Clipboard().set(summary_text_field.value)
            page.show_dialog(ft.SnackBar(ft.Text("コピーしました！")))
        page.update()

    reset_history = ft.TextButton("RESET HISTORY", on_click=lambda _: (task_history.clear(), ft.SharedPreferences().set("task_history", "[]"), page.update()))

    # --- レイアウト ---
    page.add(
        ft.Column([
            task_dropdown,
            ft.Container(timer_text, padding=20),
            status_label,
            ft.Divider(),
            start_btn,
            pause_btn,
            resume_btn,
            ft.Container(finish_btn, margin=ft.margin.only(top=10)),
            ft.Divider(),
            ft.Row([
                ft.TextButton("📊 Log Copy", on_click=toggle_summary),
                ft.TextButton("🗑️ Clear", on_click=reset_history)
            ], alignment="center"),
            summary_text_field
        ], horizontal_alignment="center")
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