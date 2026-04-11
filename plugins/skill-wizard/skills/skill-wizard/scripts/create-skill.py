#!/usr/bin/env python3
"""
新しいスキルの雛形を作成するスクリプト

使い方:
    python create-skill.py --skill-name my-skill --target-path /path/to/skills
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def create_skill(skill_name: str, target_path_str: str):
    """
    新しいスキルの雛形を作成する
    
    Args:
        skill_name: 作成するスキル名
        target_path_str: スキルを配置するパス
    """
    # スクリプトのディレクトリを取得
    script_dir = Path(__file__).parent
    skill_flow_root = script_dir.parent
    
    # ターゲットパスを絶対パスに変換
    target_path = Path(target_path_str).resolve()
    if not target_path.exists():
        print(f"❌ エラー: 指定されたターゲットパスが存在しません: {target_path}")
        sys.exit(1)
    
    # スキルフォルダのパス
    skill_path = target_path / skill_name
    
    # スキルフォルダが既に存在するかチェック
    if skill_path.exists():
        print(f"❌ エラー: スキルフォルダが既に存在します: {skill_path}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("スキル作成開始")
    print("="*50)
    print(f"スキル名: {skill_name}")
    print(f"配置先: {skill_path}")
    print()
    
    # 1. スキルフォルダを作成
    print("[1/5] スキルフォルダを作成中...")
    skill_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ 作成完了: {skill_path}")
    
    # 2. SKILL.mdテンプレートを作成
    print("[2/5] SKILL.mdテンプレートを作成中...")
    skill_md_path = skill_path / "SKILL.md"
    skill_md_content = f"""---
name: {skill_name}
description: （スキルの説明を記載してください。起動トリガーとなるフレーズを含めること）
---

# {skill_name}

## このスキルについて

（スキルの概要を記載）

---

## 前提知識

（必要に応じて前提知識を記載）

---

## 作業フロー

### ステップ1(メインメニュー)
条件: スキル起動時
入力: -
AI実施タスク:
  - （タスクを記載）
出力: （出力内容を記載）
選択肢:
  [1] 選択肢1
  [2] 選択肢2
  [3] その他（入力してください）

補足: （補足があれば記載）

---

## 設計思想

（このスキルの設計思想や重視する点を記載）
"""
    skill_md_path.write_text(skill_md_content, encoding='utf-8')
    print("  ✓ 作成完了: SKILL.md")
    
    # 3. sessions/ フォルダを作成
    print("[3/4] sessions/ フォルダを作成中...")
    sessions_path = skill_path / "sessions"
    sessions_path.mkdir(parents=True, exist_ok=True)
    print("  ✓ 作成完了: sessions/")
    
    # 4. sessions/.gitignore を作成
    print("[4/4] sessions/.gitignore を作成中...")
    gitignore_path = sessions_path / ".gitignore"
    gitignore_content = """# セッション履歴ファイルをGit管理対象外にする
*.md
"""
    gitignore_path.write_text(gitignore_content, encoding='utf-8')
    print("  ✓ 作成完了: sessions/.gitignore")
    
    print()
    print("="*50)
    print("スキル作成完了")
    print("="*50)
    print()
    print("作成されたファイル・フォルダ:")
    print(f"  📁 {skill_path}")
    print(f"  📄   SKILL.md")
    print(f"  📁   sessions/")
    print(f"  📄     .gitignore")
    print()
    print("次のステップ:")
    print(f"  1. {skill_path / 'SKILL.md'} を開く")
    print("  2. スキルの説明とステップを記載する")
    print("  3. descriptionに起動トリガーフレーズを含める")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='新しいスキルの雛形を作成します',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--skill-name',
        required=True,
        help='作成するスキル名（ケバブケース推奨）'
    )
    parser.add_argument(
        '--target-path',
        required=True,
        help='スキルを配置するパス'
    )
    
    args = parser.parse_args()
    
    try:
        create_skill(args.skill_name, str(args.target_path))
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
