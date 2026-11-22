import json
import subprocess
from pathlib import Path

SCENES = [
    {
        "id": "s01",
        "title": "什麼是速率？怎麼比快慢？",
        "text": (
            "各位六年級的小朋友大家好！歡迎來到數學小教室。今天我們要一起破解「速率」的秘密！"
            "操場上，介文和清吉都跑了 60 公尺，介文花 10 秒，清吉花 9 秒，時間越短跑得越快！"
            "那如果距離和時間都不一樣呢？我們只要算出「平均 1 秒鐘移動幾公尺」，就能公平比快慢，這就是「速率」！"
        ),
    },
    {
        "id": "s02",
        "title": "速率三兄弟：秒速、分速、時速",
        "text": (
            "認識速率三兄弟！平均每秒鐘移動的距離叫「秒速」，例如鴕鳥每秒跑 18 公尺，記作 18 公尺斜線秒。"
            "平均每分鐘移動的距離叫「分速」，像散步或騎腳踏車。"
            "平均每小時移動的距離叫「時速」，像開車或高鐵時速 300 公里！"
            "要記住喔，課本說的速率，指的都是「平均速率」！"
        ),
    },
    {
        "id": "s03",
        "title": "神奇公式金字塔",
        "text": (
            "算速率有三個黃金公式，記不住怎麼辦？快來畫一個「神奇金字塔」！距離住在最頂端，速率和時間住在下面。"
            "想算誰，就用手把它遮起來！遮住速率，上面距離除以時間，就是「速率等於距離除以時間」。"
            "遮住距離，下面相乘，就是「距離等於速率乘以時間」。"
            "遮住時間，就是「時間等於距離除以速率」。超簡單吧！"
        ),
    },
    {
        "id": "s04",
        "title": "大魔王一：單位換算怎麼算？",
        "text": (
            "接下來是同學最容易卡關的「單位換算」！記住口訣：時間變小用除法，時間變大用乘法！"
            "時速換成 1 分鐘走多遠，時間變 60 分之一，所以要除以 60；分速換秒速，再除以 60！"
            "反過來，秒速換分速、分速換時速，就要乘以 60！"
            "如果碰到公里和公尺，別忘了 1 公里等於 1000 公尺喔！"
            "例如時速 7.2 公里，先乘 1000 變成 7200 公尺，再連除兩次 60，答案就是秒速 2 公尺！"
        ),
    },
    {
        "id": "s05",
        "title": "大魔王二：必考兩大陷阱！",
        "text": (
            "寫考卷時一定要小心這兩個超級陷阱！第一，比快慢之前，「單位一定要統一」！"
            "時速 75 公里和分速 1200 公尺，不能直接比大小，要把分速乘以 60 換成時速 72 公里，才能比出誰比較快！"
            "第二，算「平均速率」，千萬不可以把兩個速率加起來除以 2！"
            "一定要先算出總距離和總時間，再用「總距離除以總時間」，才不會掉進陷阱裡！"
        ),
    },
    {
        "id": "s06",
        "title": "生活應用：追趕與相遇問題",
        "text": (
            "最後來看兩種常考的應用題。如果兩個人從同一個地方「同方向」出發，因為都在往前面跑，"
            "距離是慢慢拉開的，所以要先把「兩個人的速率相減」，再乘以時間！"
            "那如果是「面對面相向而行」，或是「背對背往反方向跑」，兩人會一起縮短或拉開距離，"
            "這時候就要把「兩個人的速率相加」來計算喔！"
        ),
    },
    {
        "id": "s07",
        "title": "總複習與通關秘訣",
        "text": (
            "恭喜你！三分鐘速率大冒險破關啦！最後一起複習四個重點："
            "一、認識秒速、分速、時速；二、善用距離在上的公式金字塔；"
            "三、單位換算要看清時間和長度；四、平均速率等於總距離除以總時間！"
            "只要多練習課本和習作的題目，你一定能成為速率小達人，加油！"
        ),
    },
]

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "audio"
OUT_DIR.mkdir(exist_ok=True)


def synth_windows_sapi():
    meta = []
    total_dur = 0.0

    for scene in SCENES:
        wav_path = OUT_DIR / f"{scene['id']}.wav"
        mp3_path = OUT_DIR / f"{scene['id']}.mp3"
        # Clean text for SAPI (replace 斜線 with 每, etc. for natural reading)
        spoken = scene["text"].replace("斜線", "每")
        ps_script = f"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft Hanhan Desktop')
$synth.Rate = 2
$synth.SetOutputToWaveFile('{str(wav_path)}')
$synth.Speak('{spoken.replace("'", "''")}')
$synth.Dispose()
"""
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            check=True,
        )
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                str(wav_path),
                "-ar",
                "44100",
                "-b:a",
                "128k",
                str(mp3_path),
            ],
            check=True,
        )
        wav_path.unlink(missing_ok=True)

        res = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(mp3_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        dur = float(res.stdout.strip())
        total_dur += dur
        meta.append(
            {
                "id": scene["id"],
                "title": scene["title"],
                "text": scene["text"],
                "audio": f"audio/{scene['id']}.mp3",
                "duration": round(dur, 2),
            }
        )
        print(f"[{scene['id']}] {dur:.2f}s - {scene['title']}")

    print(f"\nTotal voiceover duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")
    (BASE_DIR / "scenes_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    synth_windows_sapi()
