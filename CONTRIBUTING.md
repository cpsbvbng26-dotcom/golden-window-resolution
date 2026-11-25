# 手を入れるときに

Issue も pull request も歓迎する。登録は要らない。

## ここに何があるか

Figshare に置いた稿（`10.6084/m9.figshare.35050300`）の LaTeX の原稿・組んだ PDF・紙面の数を出す台本と、その出力と検査である。
二つ目の稿は `continuity/` に、Figshare に置く品とそれを作る台本は `figshare/` にある。
どこに何があるかは [README.md](README.md) の「中身」の表にある。

## 何を知らせてほしいか

<https://github.com/cpsbvbng26-dotcom/golden-window-resolution/issues> に立てる。
紙面の誤りは、issue の様式「誤りの知らせ」で受ける。

1. 証明の誤り。どの稿の、どの命題・定理・補題か
2. 紙面の数が、台本の出力と合わないこと。走らせた環境を添えてほしい
3. 紙面の状態の表（known / not found in the texts read / conditional）と、文献との食い違い
4. 引用の誤り。紙面が書く文献の読み方と、文献そのものとの食い違い

## 変更を出す

```
python3 -m pip install -r requirements.txt
python3 verification/run_scripts.py          # 台本を回して expected/ と比べる（合わせて二十分ほど）
python3 verification/check_numbers.py        # 紙面の数と台本の出力
python3 verification/check_numbers_continuity.py   # 二つ目の稿の数
python3 verification/check_text.py           # 所属・使わない語・CITATION.cff
python3 verification/check_copies.py         # 正本の写し・題・PDF のハッシュ
python3 verification/check_figshare.py       # Figshare に置く品
```

通ってから出す。`run_scripts.py` のほかの検査は、`--break` で壊して落ちることを確かめられる。

## 検査を足すときは、壊す試験も一緒に足す

通ることでは信用できない。通る状態を壊して、その検査がちょうど落ちることを確かめる。
紙面に数を書いたら、出した台本と出力を置き、`check_numbers.py` に一行足す。

## 手で編集してはいけないもの

`expected/` は台本の出力そのものである。`figshare/` の品と `figshare/METADATA.md`・`SHA256SUMS` は `figshare/build.py` の生成物である。
どちらも、台本を直して作り直す。

## 通らない変更

- Figshare に置いた稿（`paper/`）の原稿と PDF の変更。凍結した版であり、誤りは PDF ではなく記録の側で扱う
- 検査の期待値（`expected/`）を、通すために変えること。落ちたら中身を直す
- 所属の記載
- 知られている結果を、自分の結果として書くこと。紙面の状態の表と本文を食い違わせること
- 条件付きの定理から、条件を外すこと
- 推測で埋めた DOI
- 言語モデル利用の開示を消すこと

## 支えの範囲と、これからの見込み

- 維持しているのは著者一人である（根本卓哉）。組織の後ろ盾は無い
- issue への返答は数日から一週間を目安とする。約束ではない

## ライセンス

稿と散文は [CC BY 4.0](LICENSE)、台本と検査は [MIT](LICENSE-CODE)。手を入れたぶんも同じ条件で扱われる。
稿が引く他の著者の文は、どちらの条件でも許諾しておらず、それぞれの権利者のものである。

## 突き合わせの受付 / Checked intake

2026-12-01 から、誤りの知らせ（`error-report.yml`）は「突き合わせの受付」で確かめる。
人が嘘をつくこと一般は、仕組みでは止められない。受けるのは、申し立てた人がその場で書けない出どころと突き合わせられる申し立てだけで、通らないものと確かめられないものは自動で退ける。
確かめるのは一つだけである。「書いてあること」の語が、「どこか」の欄に書いた所（このリポジトリのファイル、配っている頁、このリポジトリが写しを持つ DOI の PDF か翻刻）に、そのとおりにあること。空白の違いと文字の幅は見ない。頁や節は確かめず、文書の全体を探す。
あればラベル「quote verified」を付ける。それが誤りかどうかは、人が読んで決める。なければ、ラベル「not verified」と決まった文のコメントを付け、その申し立ては受け付けない。本文を直すか、新しい issue で出し直せば、もう一度確かめる。
突き合わせの受付は、どの issue も閉じず、鍵も掛けない。どの issue も人が読む。言葉の並びでは、法令が受けて扱うことを求める求め（削除・権利・個人の情報・人についての記述・同意の撤回。どの言語でも）を、誤りの知らせと見分けきれないためである（2026-11-15）。
そう読める語を含む issue には、ラベル「needs a person」も付ける。人への目印で、これに頼って何かを決めることはない。
持ち主が開き直したり直したりしたときは、何もしない。
コメントと実行の記録は、決まった語と issue の番号だけを書き、issue に書かれたことを写さない。
道具は `.github/checked-intake/verify.js`、確かめる先は `.github/checked-intake/config.json` にある。

From 2026-12-01, error reports (`error-report.yml`) are checked by the checked intake.
No system can stop a person from lying in general. Only claims that can be checked against a source that the claimant does not write at the moment of claiming are accepted; a claim that fails, or cannot be checked, is turned away automatically.
One thing is checked: that the words under "What it says" occur, as written, at the location under "Where" (a file of this repository, a page that it serves, or the PDF or transcription of a DOI of which it holds a copy). Differences of white space and character width are ignored. The page or section is not checked; the whole document is searched.
If they occur, the label "quote verified" is added, and whether it is an error is decided by a person. If they do not, the label "not verified" and a fixed comment are added, and the claim is not accepted; editing the issue, or opening a new one, runs the check again.
The checked intake never closes or locks an issue; a person reads every one. No list of words can tell every request that the law requires the operator to receive (removal, rights, personal data, statements about a person, the withdrawal of a consent, in any language) from an error report (2026-11-15).
An issue with words that read as such a request also gets the label "needs a person": a signal for the person, never relied on.
When the owner of the repository reopens or edits an issue, nothing is done.
Comments and logs carry only fixed words and the issue number, never what the issue says.
The script is `.github/checked-intake/verify.js`; what it checks against is in `.github/checked-intake/config.json`.
