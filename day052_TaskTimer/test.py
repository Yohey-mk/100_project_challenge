# test.py

import flet as ft
import asyncio
import json
from datetime import datetime

async def main(page: ft.Page):
    page.title = "TaskTracker Pro"
    page.window.width = 300
    page.window.height = 450
    page.theme_mode = "LIGHT"
    page.window.always_on_top = False

    # 1. 状態管理 (新しいデータ構造)
    task_history = []  # 過去の完了したタスク履歴のリスト
    active_session = None  # 現在計測中のセッション情報（Noneなら停止中）
    
    # 画面表示用の変数
    current_seconds = 0
    is_paused = False

    # --- 💾 データのロード ---
    async def load_data():
        nonlocal task_history
        saved_str = await ft.SharedPreferences().get("task_history")
        if saved_str:
            task_history = json.loads(saved_str)
    
    await load_data()

    # --- 🕰️ 時間フォーマット関数 ---
    def get_formatted_time(seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    # --- 🔄 タイマーの裏側処理 ---
    async def timer_tick():
        nonlocal current_seconds
        while True:
            if active_session is not None and not is_paused:
                current_seconds += 1
                timer_text.value = get_formatted_time(current_seconds)
                page.update()
            await asyncio.sleep(1)

    # --- 🎮 ボタンの処理 ---
    
    # START / STOP ボタン
    async def handle_start_stop(e):
        nonlocal active_session, current_seconds, is_paused
        
        # 【START処理】
        if active_session is None:
            if task_dropdown.value is None or task_dropdown.value == "Select task":
                page.show_dialog(ft.SnackBar(ft.Text("タスクを選択してください！")))
                return

            now = datetime.now()
            # 新しいセッションデータを作成
            active_session = {
                "date": now.strftime("%Y-%m-%d"),
                "task": task_dropdown.value,
                "start_time": now.strftime("%H:%M:%S"),
                "end_time": "",
                "pauses": [],
                "duration_seconds": 0
            }
            current_seconds = 0
            is_paused = False
            
            # UIの更新
            start_stop_btn.text = "STOP"
            start_stop_btn.icon = ft.Icons.STOP
            start_stop_btn.style = ft.ButtonStyle(color=ft.Colors.RED)
            pause_btn.disabled = False
            task_dropdown.disabled = True
            status_text.value = f"Running: {active_session['task']}"

        # 【STOP処理】
        else:
            now = datetime.now()
            # 終了処理を記録
            active_session["end_time"] = now.strftime("%H:%M:%S")
            active_session["duration_seconds"] = current_seconds
            
            # もし一時停止中のままSTOPを押されたら、一時停止の終了時間も記録
            if is_paused and active_session["pauses"]:
                active_session["pauses"][-1]["end"] = now.strftime("%H:%M:%S")

            # 履歴リストに追加して保存
            task_history.append(active_session)
            states_str = json.dumps(task_history)
            await ft.SharedPreferences().set("task_history", states_str)

            # リセット
            active_session = None
            is_paused = False
            current_seconds = 0
            
            # UIの更新
            start_stop_btn.text = "START"
            start_stop_btn.icon = ft.Icons.PLAY_ARROW
            start_stop_btn.style = ft.ButtonStyle(color=ft.Colors.BLUE)
            pause_btn.disabled = True
            pause_btn.text = "PAUSE"
            pause_btn.icon = ft.Icons.PAUSE
            task_dropdown.disabled = False
            timer_text.value = "00:00:00"
            status_text.value = "Ready"
            page.show_dialog(ft.SnackBar(ft.Text("記録を保存しました！")))

        page.update()

    # PAUSE / RESUME ボタン
    async def handle_pause(e):
        nonlocal is_paused, active_session
        if active_session is None: return

        now = datetime.now().strftime("%H:%M:%S")

        if not is_paused:
            # 【PAUSE処理】
            is_paused = True
            # ポーズの開始時間を記録
            active_session["pauses"].append({"start": now, "end": ""})
            pause_btn.text = "RESUME"
            pause_btn.icon = ft.Icons.PLAY_CIRCLE_FILL
            status_text.value = "Paused"
        else:
            # 【RESUME処理】
            is_paused = False
            # 最新のポーズの終了時間を記録
            if active_session["pauses"]:
                active_session["pauses"][-1]["end"] = now
            pause_btn.text = "PAUSE"
            pause_btn.icon = ft.Icons.PAUSE
            status_text.value = f"Running: {active_session['task']}"

        page.update()

    # --- 📊 UI構築 ---

    aot_switch = ft.Switch(label="Always On Top", value=False, scale=0.9)
    def toggle_aot(e):
        page.window.always_on_top = e.control.value
        page.update()
    aot_switch.on_change = toggle_aot

    task_dropdown = ft.Dropdown(
        value="Select task",
        options=[
            ft.DropdownOption(key="Coding", text="Coding"),
            ft.DropdownOption(key="メール作業", text="メール作業"),
            ft.DropdownOption(key="会議", text="会議"),
            ft.DropdownOption(key="休憩", text="休憩"),
        ],
        width=250
    )

    timer_text = ft.Text("00:00:00", size=20, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Ready", color=ft.Colors.GREY)

    start_stop_btn = ft.ElevatedButton("START", icon=ft.Icons.PLAY_ARROW, on_click=handle_start_stop, style=ft.ButtonStyle(color=ft.Colors.BLUE))
    pause_btn = ft.ElevatedButton("PAUSE", icon=ft.Icons.PAUSE, on_click=handle_pause, disabled=True)

    controls_row = ft.Row([start_stop_btn, pause_btn])

    # --- 📝 エクセル用出力機能 ---
    summary_text_field = ft.TextField(multiline=True, read_only=True, value="", text_size=12, visible=True, height=150)

    async def open_summary(e):
        is_visible = summary_text_field.visible
        summary_text_field.visible = is_visible

        if is_visible:
            # エクセルに貼り付けやすいようにタブ(\t)区切りでヘッダーを作成
            copy_lines = ["Date\tTask\tStart\tEnd\tDuration\tPauses"]
            
            for session in task_history:
                dur_str = get_formatted_time(session["duration_seconds"])
                # ポーズ履歴を文字列化（例: 09:30-09:35, 10:00-10:10）
                pauses_str = ", ".join([f"{p['start']}-{p['end']}" for p in session.get("pauses", [])])
                
                # タブ区切りでデータを結合
                line = f"{session['date']}\t{session['task']}\t{session['start_time']}\t{session['end_time']}\t{dur_str}\t{pauses_str}"
                copy_lines.append(line)

            summary_text_field.value = "\n".join(copy_lines)
            await ft.Clipboard().set(summary_text_field.value)
            page.window.height = 450
            page.show_dialog(ft.SnackBar(ft.Text("Excel用にコピーしました！(そのまま貼り付け可能)")))
        else:
            page.window.height = 450

        page.update()

    summary_btn = ft.Button("History＆Copy", on_click=open_summary)

    # 全リセット機能
    async def reset_history(e):
        nonlocal task_history
        task_history = []
        await ft.SharedPreferences().set("task_history", json.dumps([]))
        summary_text_field.value = ""
        #page.close(reset_dialog)
        page.show_dialog(ft.SnackBar(ft.Text("履歴を完全にリセットしました")))
        page.update()

    def close_reset_dialog(e):
        page.close(reset_dialog)

    reset_dialog = ft.AlertDialog(
        title=ft.Text("警告"),
        content=ft.Text("過去の履歴をすべて削除しますか？"),
        actions=[
            ft.TextButton("削除", on_click=reset_history, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ft.TextButton("キャンセル", on_click=close_reset_dialog)
        ]
    )

    reset_btn = ft.OutlinedButton("🗑️ RESET", on_click=reset_history)

    # コンポーネントの配置
    page.add(
        ft.Column([
            aot_switch,
            task_dropdown,
            ft.Container(content=timer_text),
            ft.Container(content=status_text),
            controls_row,
            ft.Divider(height=30),
            ft.Row([summary_btn, reset_btn]),
            summary_text_field,
        ])
    )

    page.run_task(timer_tick)

ft.run(main)