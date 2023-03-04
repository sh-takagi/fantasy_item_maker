# Fantasy Item Maker
ファンタジー系のRPGに出てきそうなアイテムをGPT-3.5-Turboを使って生成するツールです。

# Demo


# Features
- ChatGPTのAPIを使用してファンタジーアイテムの名前、価格、説明文を生成します。
- 価格、説明文のどちらかのみを生成することも可能。
- 生成したアイテムをcsvファイルに保存可能。

# Requirement
- openai 0.27.0

# Installation
```bash
pip install openai
pip install --upgrade openai
```

# Usage
`python fantasy_item_maker.py`で起動
- Name, Price, Descriptionいずれも入力しなかった場合、完全にランダムに生成。
- Name, Price, Description全部に入力があると生成されない
- Priceには数字のみ入力（100から3000まで）
- チェックボックスはその要素を生成するかどうかの選択。
