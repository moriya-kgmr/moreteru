# 流出チェッカー（moreteru.com）

https://moreteru.com のソースコードです。
あなたのパスワードが、過去に流出したデータに含まれていないかを確認できる無料ツールです。

このリポジトリは「入力したパスワードが本当に外部に送られていないか」を誰でも確かめられるように公開しています。

## パスワードはどう扱われるか

照合の処理はすべて `index.html` の中の JavaScript で、あなたのブラウザ上で行われます。

1. 入力されたパスワードを、ブラウザ内で SHA-1 ハッシュに変換します。
2. ハッシュの**先頭5文字だけ**を [Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) に送ります。
3. API は、先頭5文字が一致する数百件のハッシュ候補を返します。
4. 残りの照合はブラウザ内で行い、一致した場合はその漏洩回数を表示します。

パスワードそのものやハッシュの全体は、どこにも送信・保存されません（k-匿名性と呼ばれる方式です）。
該当するコードは `index.html` の `pw-form` の submit 処理です。

## 外部への通信

このページが通信する先は次のとおりです。

| 通信先 | 目的 |
| --- | --- |
| api.pwnedpasswords.com | パスワード照合（ハッシュの先頭5文字のみ） |
| haveibeenpwned.com | 最近の漏洩事例の一覧（公開データ） |
| fonts.googleapis.com / fonts.gstatic.com | 文字の表示（Google Fonts） |
| Cloudflare Web Analytics | アクセス数の計測（Cookie不使用） |

## データの提供元

漏洩データは [Have I Been Pwned](https://haveibeenpwned.com/)（CC BY 4.0）を利用しています。
当サイトは Have I Been Pwned の運営元とは関係ありません。

## 運営者

ネットの鍵守 守屋
お問い合わせ：https://docs.google.com/forms/d/e/1FAIpQLSf6xIEEqUGuoIKkTXFXBAXQe5ZmlmEewI4qRWO71FYooHPCmA/viewform
