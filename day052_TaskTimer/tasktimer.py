# tasktimer.py

import flet as ft
import asyncio
import json
from datetime import datetime

async def main(page: ft.Page):
    page.title = "TaskTracker"
    page.scroll = "auto"
    page.window.width = 250
    page.window.height = 400
    page.theme_mode = "LIGHT"
    page.window.always_on_top = True

    # 1. 状態管理(State)
    # 各タスクの経過時間を保存する辞書
    task_states = {"Coding": 0, "メール作業": 0, "休憩": 0}
    task_list = ft.Dropdown(value="Select task",
                            options=[
                                ft.DropdownOption(key="Coding", text="Coding"),
                                ft.DropdownOption(key="メール作業", text="メール作業"),
                                ft.DropdownOption(key="休憩", text="休憩"),])
    active_task = None # 現在計測中のタスク名（Noneなら停止中）
    # text uiの参照を保存する辞書（文字だけをピンポイントで書き換えるため）
    time_texts = {}

    # データのロード
    async def load_data():
        nonlocal task_states
        saved_str = await ft.SharedPreferences().get("task_states")
        if saved_str:
            task_states = json.loads(saved_str)
    
    await load_data()

    # format time
    def get_formatted_time(seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    # 文字列を計算用の秒(int)に戻す関数
    def time_to_seconds(time_str: str) -> int:
        try:
            #':'で分割し、h/m/sの数字に変換
            h, m, s = map(int, time_str.split(":"))
            return h * 3600 + m * 60 + s
        except ValueError:
            return -1 # フォーマットが間違っている場合は-1を返す

    # 2. タイマーFunction
    async def timer_tick():
        nonlocal active_task # 関数の中から外部の変数（active_task）を書き換える
        while True:
            if active_task is not None:
                # 1. アクティブタスクの時間を１秒増やす
                task_states[active_task] += 1
                time_formatted = get_formatted_time(task_states[active_task])
                # 2. 該当するUIのテキストの値を書き換える
                time_texts[active_task].value = time_formatted
                # 3. テキストだけを最新化して描画
                states_str = json.dumps(task_states)
                await ft.SharedPreferences().set("task_states", states_str)
                page.update()
            await asyncio.sleep(1)

    # 3. ボタンを押した時の処理
    def handle_task_click(e:ft.Event[ft.Button]):
        nonlocal active_task
        clicked_task = e.control.data
        # 同じボタンをもう一度押したら停止、違うボタンなら切り替え
        if active_task == clicked_task:
            active_task = None
            page.title = "TaskTracker - Stopped"
        else:
            active_task = clicked_task
            page.title = f"TaskTracker - {active_task}"
        page.update()

    # 編集機能の実装
    edit_target_task = None
    edit_time_field = ft.TextField("00:00:00", text_size=12, width=100, height=35, border_radius=10)
    # 保存ボタンが押された時の処理
    async def save_edited_time(e):
        nonlocal edit_target_task
        new_seconds = time_to_seconds(edit_time_field.value)
        if new_seconds >= 0:
            task_states[edit_target_task] = new_seconds
            time_texts[edit_target_task].value = get_formatted_time(new_seconds)
            page.show_dialog(ft.SnackBar(ft.Text(f"Edited: {edit_target_task}")))
            states_str = json.dumps(task_states)
            await ft.SharedPreferences().set("task_states", states_str)
            page.show_dialog(ft.SnackBar(ft.Text(f"Edited: {edit_target_task}")))
            page.update()
        else:
            page.show_dialog(ft.SnackBar(ft.Text("Invalid format!")))
            page.update()

    #def close_edit_dialog(e):
    #    edit_dialog.open = False
    #    page.update()

    save_btn = ft.IconButton(icon=ft.Icons.SAVE, icon_size=20, on_click=save_edited_time)
    #close_btn = ft.Button(ft.Text("Cancel"), on_click=close_edit_dialog)

    # 編集用ダイアログ
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit"),
        content=edit_time_field,
        actions=[
            ft.TextButton("Save", on_click=save_edited_time),
        ]
    )
    page.services.append(edit_dialog)

    def open_edit_dialog(e):
        nonlocal edit_target_task
        edit_target_task = e.control.data
        edit_time_field.value = time_texts[edit_target_task].value
        edit_dialog.title = ft.Text(f"Edit: {edit_target_task}")
        edit_dialog.open = True
        page.update()

    edit_text = ft.Text("EDIT: ")

    edit_and_save = ft.Row(
        controls=[
            edit_text,
            edit_time_field,
            save_btn,
        ]
    )

    async def reset_all_tasks(e):
        for task in task_states:
            task_states[task] = 0
            time_texts[task].value = "00:00:00"
        states_str = json.dumps(task_states)
        await ft.SharedPreferences().set("task_states", states_str)
        page.show_dialog(ft.SnackBar(ft.Text("記録をリセットしました")))
        page.update()

    def close_reset_dialog(e):
        page.close(reset_warning)

    reset_warning = ft.Container(
        content=ft.Row(controls=[
            ft.TextButton("RESET", on_click=reset_all_tasks, style=ft.ButtonStyle(color=ft.Colors.RED))
        ])
    )

    # 4. レイアウト構築
    task_rows = []
    # 辞書のキーを使って、for文でUIを量産
    for task_name, seconds in task_states.items():
        # 初期状態のテキストを作成、辞書に登録
        time_texts[task_name] = ft.Text(get_formatted_time(seconds), size=12, selectable=True)

        row = ft.Row(
            controls=[
                ft.Button(
                    content=ft.Text(f"{task_name}"),
                    data=task_name,
                    on_click=handle_task_click,
                    width=100,
                    scale=0.9,
                ),
                time_texts[task_name],

                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    data=task_name,
                    on_click=open_edit_dialog,
                    icon_size=16
                )
            ]
        )
        task_rows.append(row)

    # functions conponents
    aot_switch = ft.Switch(label="Always On Top", value=True, scale=0.9)
    def toggle_aot(e):
        page.window.always_on_top = e.control.value
        page.update()
    aot_switch.on_change = toggle_aot

    # Layout
    msg = ft.Text("Welcome to Task Tracker!")
    btns_container = ft.Container(
        content=ft.Column(controls=task_rows),
        margin=ft.Margin(top=20)
        )
    
    # DataTable & Excel用コピー機能
    summary_text_field = ft.TextField(
        multiline=True,
        read_only=True,
        value="",
        text_size=12,
        visible=True
    )

    # 集計データをコピーに集約
    #async def copy_to_clipboard():
    #    await ft.Clipboard().set(summary_text_field.value)
    #    page.show_dialog(ft.SnackBar("Text copied to clipboard"))
    #copy_btn = ft.Button("Copy", on_click=copy_to_clipboard, visible=True)

    # 1. 画面に表示するDataTableの枠組みを作る
    async def open_summary(e):
        is_visible = summary_text_field.visible
        summary_text_field.visible = is_visible

        if is_visible:
            copy_lines = []

            for task_name, seconds in task_states.items():
                formatted_time = get_formatted_time(seconds)
                copy_lines.append(f"{task_name}\t{formatted_time}")

            summary_text_field.value = "\n".join(copy_lines)
            await ft.Clipboard().set(summary_text_field.value)
            page.show_dialog(ft.SnackBar(ft.Text("Copied!")))
        else:
            page.window.height = 400

        page.update()

    # 6. 集計データをコピー
    summary_btn = ft.Button("集計データをCopy", on_click=open_summary)
    reset_btn = ft.Button("ALL RESET", on_click=reset_all_tasks, style=ft.ButtonStyle(color=ft.Colors.RED))

    # Page.add
    page.add(
        msg,
        aot_switch,
        btns_container,
        edit_and_save,
        summary_btn,
        summary_text_field,
        reset_btn,
    )

    # 5. アプリの裏側での仕様
    page.run_task(timer_tick)

ft.run(main)


# memo（段階的実装プラン）
# ①将来的にエクセルなどに直接貼り付けられるように集計データをテーブル化
# ②計測した時間の編集機能（一時停止などをし忘れた場合に編集できるようにする）
# ③アプリを間違って消しても前回の記録から再開する / 確認ポップアップ付きでリセットする
# ④タスク選択をフォルダ化（タスクが多岐に渡る場合は「レポート業務」「実務」「その他」の大カテゴリから小カテゴリ（実務などの詳細）のボタンで計測開始する）
