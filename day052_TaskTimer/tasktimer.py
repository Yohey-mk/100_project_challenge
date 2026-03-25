# tasktimer.py

import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "TaskTracker"
    page.scroll = "auto"
    page.window.width = 300
    page.window.height = 400
    page.theme_mode = "LIGHT"
    page.window.always_on_top = True

    # 1. 状態管理(State)
    # 各タスクの経過時間を保存する辞書
    task_states = {"Coding": 0, "メール作業": 0, "休憩": 0}
    active_task = None # 現在計測中のタスク名（Noneなら停止中）

    # text uiの参照を保存する辞書（文字だけをピンポイントで書き換えるため）
    time_texts = {}

    # 2. タイマーFunction
    async def timer_tick():
        nonlocal active_task # 関数の中から外部の変数（active_task）を書き換える

        while True:
            if active_task is not None:
                # 1. アクティブタスクの時間を１秒増やす
                task_states[active_task] += 1
                # divmodを使って秒数をHHMMSSに変換
                m, s = divmod(task_states[active_task], 60)
                h, m = divmod(m, 60)
                time_formatted = f"{h:02d}:{m:02d}:{s:02d}"
                # 2. 該当するUIのテキストの値を書き換える
                time_texts[active_task].value = time_formatted
                # 3. テキストだけを最新化して描画
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

    # 4. レイアウト構築
    task_rows = []
    # 辞書のキーを使って、for文でUIを量産
    for task_name in task_states.keys():
        # 初期状態のテキストを作成、辞書に登録
        time_texts[task_name] = ft.Text("00:00:00", size=20)

        row = ft.Row(
            controls=[
                ft.Button(
                    content=ft.Text(f"{task_name}"),
                    data=task_name,
                    on_click=handle_task_click,
                    width=150
                ),
                time_texts[task_name]
            ]
        )
        task_rows.append(row)

    # functions conponents
    aot_switch = ft.Switch(label="Always On Top", value=True)
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

    # Page.add
    page.add(
        msg,
        aot_switch,
        btns_container,
    )

    # 5. アプリの裏側での仕様
    page.run_task(timer_tick)

ft.run(main)


# memo
# 将来的にエクセルなどに直接貼り付けられるように集計データをテーブル化
# 計測した時間の編集機能（一時停止などをし忘れた場合に編集できるようにする）