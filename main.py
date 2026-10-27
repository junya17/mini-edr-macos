import time
from datetime import datetime

import psutil
from rich.console import Console

console = Console()


def get_processes():
    """
    実行中のプロセスを取得する。

    PIDだけでなく開始時刻も組み合わせ、
    PIDの再利用による誤認を減らす。
    """
    processes = {}

    for proc in psutil.process_iter(
        ["pid", "ppid", "name", "create_time", "exe"]
    ):
        try:
            info = proc.info

            # PIDと開始時刻でプロセスを識別
            key = (info["pid"], info["create_time"])

            processes[key] = info.copy()

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes


def monitor():
    """
    前回と現在のプロセス一覧を比較し、
    START / EXITを検出する。
    """

    previous = get_processes()

    console.print(
        "[bold green]MINI EDR V2 STARTED[/bold green]"
    )

    try:
        while True:
            time.sleep(1)

            current = get_processes()

            # 集合の差分から新規・終了プロセスを推定
            started = current.keys() - previous.keys()
            exited = previous.keys() - current.keys()

            for key in sorted(started):
                info = current[key]

                start_time = datetime.fromtimestamp(
                    key[1]
                ).strftime("%H:%M:%S")

                console.print(
                    f"[green]START[/green] "
                    f"[{start_time}] "
                    f"PID={info['pid']} "
                    f"PPID={info['ppid']} "
                    f"NAME={info['name']}"
                )

                console.print(
                    f"    PATH={info['exe'] or 'unknown'}"
                )

            for key in sorted(exited):
                info = previous[key]

                # EXITは終了を検出した時刻
                exit_time = datetime.now().strftime(
                    "%H:%M:%S"
                )

                console.print(
                    f"[red]EXIT[/red]  "
                    f"[{exit_time}] "
                    f"PID={info['pid']} "
                    f"NAME={info['name']}"
                )

            previous = current

    except KeyboardInterrupt:
        console.print(
            "\n[yellow]MONITOR STOPPED[/yellow]"
        )


if __name__ == "__main__":
    monitor()
import time
import psutil

from datetime import datetime
from rich.console import Console

# Richを使ってターミナルに色付きで表示する
console = Console()


def get_processes():
    """
    現在実行中のプロセス一覧を取得する。
    PIDと開始時刻を組み合わせて識別する。
    """

    processes = {}

    for proc in psutil.process_iter(["pid", "name", "create_time"]):
        try:
            info = proc.info

            # PIDは再利用されるため開始時刻も保持
            key = (info["pid"], info["create_time"])

            processes[key] = info["name"]

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes


def monitor():
    """
    1秒ごとにプロセスを取得し、
    前回との差分から起動・終了を検出する。
    """

    previous = get_processes()

    console.print("[bold green]MINI EDR STARTED[/bold green]")

    try:
        while True:
            time.sleep(1)

            current = get_processes()

            # 集合演算で新しく増えたプロセスを検出
            started = current.keys() - previous.keys()

            # 前回存在したが現在はないプロセス
            exited = previous.keys() - current.keys()

            for key in sorted(started):
                pid = key[0]
                name = current[key]

                # プロセスの実際の起動時刻
                start_time = datetime.fromtimestamp(key[1]).strftime("%H:%M:%S")

                console.print(
                    f"[green]START[/green] [{start_time}] PID={pid} NAME={name}"
                )

            for key in sorted(exited):
                pid = key[0]
                name = previous[key]

                # 終了を検出した現在時刻
                exit_time = datetime.now().strftime("%H:%M:%S")

                console.print(f"[red]EXIT[/red]  [{exit_time}] PID={pid} NAME={name}")

            # 次の比較のために現在の状態を保存
            previous = current

    except KeyboardInterrupt:
        console.print("\n[yellow]MONITOR STOPPED[/yellow]")


if __name__ == "__main__":
    monitor()
