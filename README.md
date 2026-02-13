# Manim Animation Study 🎨

這是一個學習製作動畫的專案，使用 [Manim](https://www.manim.community/) 引擎。

## 專案內容
- `scene.py`: 包含一個 15 秒的幾何變形動畫範例。
- `cartoon_scene.py`: 包含一個 15 秒的卡通史萊姆變形動畫範例。

## 如何測試
你可以使用 **GitHub Codespaces** 來快速測試：
1. 點擊 GitHub 儲存庫上方的 `Code` -> `Codespaces` -> `Create codespace on main`。
2. 在終端機執行：
   ```bash
   pip install manim
   # 測試幾何動畫
   manim -pql scene.py StudyAnimation
   # 測試卡通史萊姆動畫
   manim -pql cartoon_scene.py CartoonSlime
   ```
