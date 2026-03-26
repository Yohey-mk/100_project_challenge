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

    # format time
    def get_formatted_time(seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

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
        time_texts[task_name] = ft.Text("00:00:00", size=12, selectable=True)

        row = ft.Row(
            controls=[
                ft.Button(
                    content=ft.Text(f"{task_name}"),
                    data=task_name,
                    on_click=handle_task_click,
                    width=100,
                    scale=0.9,
                ),
                time_texts[task_name]
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
        value="test",
        text_size=12,
        visible=False
    )

    async def copy_to_clipboard():
        await ft.Clipboard().set(summary_text_field.value)
        page.show_dialog(ft.SnackBar("Text copied to clipboard"))
    copy_btn = ft.Button("Copy", on_click=copy_to_clipboard, visible=True)

    # 1. 画面に表示するDataTableの枠組みを作る
    def open_summary(e):
        is_visible = not summary_text_field.visible
        summary_text_field.visible = is_visible
        copy_btn.visible = is_visible

        if is_visible:
            copy_lines = ["Task Name\tTime"]

            for task_name, seconds in task_states.items():
                formatted_time = get_formatted_time(seconds)
                copy_lines.append(f"{task_name}\t{formatted_time}")

            summary_text_field.value = "\n".join(copy_lines)
            page.window.height = 600
        else:
            page.window.height = 400

        page.update()

    # 6. 集計データを見る
    summary_btn = ft.Button("集計データを見る", on_click=open_summary)

    # Page.add
    page.add(
        msg,
        aot_switch,
        btns_container,
        summary_text_field,
        copy_btn,
        summary_btn
    )

    # 5. アプリの裏側での仕様
    page.run_task(timer_tick)

ft.run(main)


# memo（段階的実装プラン）
# ①将来的にエクセルなどに直接貼り付けられるように集計データをテーブル化
# ②計測した時間の編集機能（一時停止などをし忘れた場合に編集できるようにする）
# ③アプリを間違って消しても前回の記録から再開する / 確認ポップアップ付きでリセットする
# ④タスク選択をフォルダ化（タスクが多岐に渡る場合は「レポート業務」「実務」「その他」の大カテゴリから小カテゴリ（実務などの詳細）のボタンで計測開始する）
