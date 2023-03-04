import tkinter as tk
import openai
import os, csv

def api_request(api_key, info_item_name, info_item_price, info_item_description, lang, item_name, item_price, item_description, use_item_price, use_item_description):
    info_item_name.delete(0, "end")
    info_item_price.delete(0, "end")
    info_item_description.delete("0.0", "end")

    item_description = item_description.replace("\n", "")
    prompt = "item."
    if item_name and item_price and item_description:
        info_item_name.insert(0, "All information are already filled")
        return
    if item_name:
        prompt += f" Let item name be {item_name}."
    if item_price:
        if int(item_price) < 100 or 3000 < int(item_price):
            info_item_name.insert(0, "price must be from 100 to 3000")
            return

        prompt += f" Let item price be {item_price}G."
    if item_description:
        prompt += f" Let item description be {item_description}."

    if not api_key:
        if os.path.isfile("api_key.txt"):
            with open("api_key.txt", mode="r", encoding="utf-8") as f:
                api_key = f.readline()
        else:
            info_item_name.insert(0, "Put in your api key")
            return
    print(api_key)
    openai.api_key = api_key
    res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {
                    "role": "system",
                    "content": f"When I send you \"item\", you generate a fantasy item information according to format. If I don't set the item name, think of a fantasy item name that sounds like it. reply with comma separated in {lang}. format: [a name of the item],[a price of the item from 100G to 3000G],[a RPG-like description of the item in 30 words]"
                    },
                {
                    "role": "user",
                    "content": prompt
                    }
                ]
            )
    res_content = res["choices"][0]["message"]["content"]
    res_content_sep = res_content.split(",")

    name = res_content_sep[0]
    price = res_content_sep[1]
    description = "".join(res_content_sep[2:])

    info_item_name.insert(0, name)
    if use_item_price:
        info_item_price.insert(0, price)
    if use_item_description:
        info_item_description.insert("0.0", description)

def save_csv(name, price, description, use_item_price, use_item_description):
    description = description.replace("\n", "")
    filename = "item_data.csv"

    if not use_item_price: price = None
    if not use_item_description: description = None

    exist_file = os.path.isfile(filename)
    with open(filename, mode="a", encoding="shift_jis", newline="") as f:
        writer = csv.writer(f)
        if not exist_file:
            writer.writerow(["Name", "Price", "Description"])
        writer.writerow([name, price, description])

def main():
    window_width = 650
    window_heignt = 600
    window_size = f"{window_width}x{window_heignt}"
    padding = 10

    #メイン画面の作成
    root = tk.Tk()
    root.title("Fantasy Item Maker")
    root.geometry(window_size)
    root.resizable(False, False)

    #タイトル
    label = tk.Label(root, text="Fantasy Item Maker", font=("Serif", 20), pady=20)
    label.pack()

    #ボタンエリア
    button_frame = tk.Frame(root)
    button_frame.pack(side="bottom", padx=padding, pady=padding)

    #インプットエリア
    input_form = tk.Frame(root, borderwidth=3, relief="groove")
    input_form.pack(side="left", anchor="nw", padx=padding, pady=padding)

    #アウトプットエリア
    output_form = tk.Frame(root, borderwidth=3, relief="groove")
    output_form.pack(side="right", anchor="nw", padx=padding, pady=padding)

    #インプットエリアの実装
    api_key_label = tk.Label(input_form, width=25, text="input your api key", font=("Arial", 15), padx=padding, pady=padding)
    api_key_label.pack()
    api_key = tk.Entry(input_form, width=35) #APIキーの入力場所
    api_key.pack()

    #言語設定
    lang_label = tk.Label(input_form, text="Language", font=("Arial", 15), padx=padding, pady=padding)
    lang_label.pack()
    lang = ["English", "Japanese"]
    selected_lang = tk.StringVar()
    selected_lang.set(lang[0])
    lang_menu = tk.OptionMenu(input_form, selected_lang, *lang)
    lang_menu.pack()

    select_contents_label = tk.Label(input_form, text="Contents", font=("Arial", 15), padx=padding, pady=padding)
    select_contents_label.pack()

    use_item_price = tk.BooleanVar(value=True)
    use_item_description = tk.BooleanVar(value=True)
    check_item_price = tk.Checkbutton(input_form, text="Price", variable=use_item_price) #アイテム価格を生成するかどうか
    check_item_description = tk.Checkbutton(input_form, text="Description", variable=use_item_description) #アイテム説明文を生成するかどうか
    check_item_price.pack()
    check_item_description.pack()

    set_contents_label = tk.Label(input_form, text="Setting", font=("Arial", 15), padx=padding, pady=padding)
    set_contents_label.pack()
    set_item_name = tk.Entry(input_form, width=35) #アイテム名の指定
    set_item_price = tk.Entry(input_form, width=35) #アイテム価格の指定
    set_item_description = tk.Text(input_form, width=30, height=8) #アイテム説明文の指定
    set_item_name_label = tk.Label(input_form, text="Name", font=("Arial", 10))
    set_item_name_label.pack()
    set_item_name.pack()
    set_item_price_label = tk.Label(input_form, text="Price", font=("Arial", 10))
    set_item_price_label.pack()
    set_item_price.pack()
    set_item_description_label = tk.Label(input_form, text="Descriptiopn", font=("Arial", 10))
    set_item_description_label.pack()
    set_item_description.pack()

    #アウトプットエリアの実装
    output_label = tk.Label(output_form, width=25, text="Item Information", font=("Arial", 15), padx=padding, pady=padding)
    output_label.pack()

    info_item_name = tk.Entry(output_form, width=35) #アイテム名の出力
    info_item_price = tk.Entry(output_form, width=35) #アイテム価格の出力
    info_item_description = tk.Text(output_form, width=30, height=22) #アイテム説明文の出力

    info_item_name_label = tk.Label(output_form, text="Name", font=("Arial", 10))
    info_item_name_label.pack()
    info_item_name.pack()
    info_item_price_label = tk.Label(output_form, text="Price", font=("Arial", 10))
    info_item_price_label.pack()
    info_item_price.pack()
    info_item_description_label = tk.Label(output_form, text="Description", font=("Arial", 10))
    info_item_description_label.pack()
    info_item_description.pack()

    #生成ボタンと保存ボタン
    button_generate = tk.Button(button_frame, text="Generate", command=lambda: api_request(
        api_key.get(),
        info_item_name,
        info_item_price,
        info_item_description,
        selected_lang.get(),
        set_item_name.get(),
        set_item_price.get(),
        set_item_description.get("0.0", "end"),
        use_item_price.get(),
        use_item_description.get()
        ))
    button_save_csv = tk.Button(button_frame, text="Save as CSV file", command=lambda: save_csv(
        info_item_name.get(),
        info_item_price.get(),
        info_item_description.get("0.0", "end"),
        use_item_price.get(),
        use_item_description.get()
        ))
    button_generate.pack(side="left", padx=padding, pady=padding)
    button_save_csv.pack(side="left", padx=padding, pady=padding)

    root.mainloop()

if __name__ == "__main__":
    main()
