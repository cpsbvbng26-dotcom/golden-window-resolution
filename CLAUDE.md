# golden-window-resolution

Figshare に出す稿 "Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game" の原稿・PDF・台本。
黄金比の窓の予想（Figshare `10.6084/m9.figshare.34419198`）の続き。10 リポジトリの外に置く（sophaxis・deposit-check と同じ扱い）。

## 決めごと

1. **DOI を推測で埋めない**。利用者から受け取った番号だけを書く。この稿の Figshare の番号は、受け取るまで書かない。
2. **公開した PDF を改変しない・再生成しない**。Figshare に載った版は凍結する。誤りは正誤表と `self-correction` に記録する。
3. **所属を書かない**。特定の大学名は、どの綴りでも書かない。`verification/check_text.py` が止める（語は符号で組んであり、ここには書き写さない）。
4. **知られている結果を自分の結果として書かない**。紙面の状態の表（known / not found in the texts read / conditional）と本文を食い違わせない。条件付きの定理（Theorem E）は条件を外さない。
5. **紙面に数を書いたら、出した台本と出力を置き、`check_numbers.py` に一行足す**。小数点以下三桁以上の数で行の無いものは落ちる。
6. **検査の期待値・乱数種を、通すために変えない**。`expected/` は台本の出力そのもの。落ちたら中身を直す。足した検査は壊して落ちることを確かめる（`--break`）。
7. **引用は、読んだものと読み方を紙面に書く**。DOI は文献の確認（lit-check）と査読の記録にある綴りのまま。番号を当てにいかない。
8. **言語モデル利用の開示は消さない。Claude を著者にしない**（紙面・CITATION.cff・README）。
9. 稿と散文は CC BY 4.0、台本は MIT。勝手に変えない。
10. `SECURITY.md` と `.github/ISSUE_TEMPLATE/error-report.yml` は cpsbvbng26-dotcom の正本と一字一句同じに置く。`check_copies.py` がハッシュで見る。
11. 枝を切って PR にする。コミットは種別ごとに分ける（原稿・PDF・台本・検査・文書）。マージの本文に開示の二行を入れる。
12. **Claude は利用者に命令しない**（cpsbvbng26-dotcom の決めごと 16）。返答・PR・文書に利用者の作業の一覧を書かない。Figshare・Sophaxis への登録のように Claude に触れられないものは、触れられないという事実だけを書く。利用者が自分から手順を求めたときだけ手順を書く。
13. **issue の中身を言語モデルに渡すのは、本人の同意がある題と本文だけ**（同じく決めごと 17）。同意の文を引用符で囲んで `search_issues` に渡し、`- [X]` の行がある issue の題と本文だけを読む。コメントは読まない。
14. **公開の前に、紙面全体に対して敵対的な査読を一度通す**（決めごと 18）。主な主張を導き直し、数を台本と突き合わせ、引用を文献の確認と突き合わせる。各部分がどの三つの検査を通ったかを記録に書く。

```
python3 verification/run_scripts.py [curve|edges|symbolic|symbolic-referee|trinity]   # 台本を回して expected/ と比べる（合わせて二十分ほど）
python3 verification/check_numbers.py      # 紙面の数と台本の出力（--break で壊して確かめる）
python3 verification/check_text.py         # 所属・使わない語・CITATION.cff（--break）
python3 verification/check_copies.py       # 正本の写し・題・PDF の題
cd paper && pdflatex golden-window-resolution.tex && pdflatex golden-window-resolution.tex
```
