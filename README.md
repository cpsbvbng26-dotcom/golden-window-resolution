# golden-window-resolution

Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game（黄金比の窓の予想の解決と、穴の開いた β 変換についての関連する結果）の原稿・PDF・検査の台本を置いています。

[English](README.en.md)

稿は Figshare にあります。DOI は [`10.6084/m9.figshare.35050300`](https://doi.org/10.6084/m9.figshare.35050300) です。
このリポジトリの保存版（v1.0.0）は Zenodo にあります。DOI は [`10.5281/zenodo.24382288`](https://doi.org/10.5281/zenodo.24382288) で、すべての版に共通する DOI は [`10.5281/zenodo.24382287`](https://doi.org/10.5281/zenodo.24382287) です。
稿を引くときは、Zenodo ではなく Figshare の DOI を使います。
番号は 2026-11-18 に利用者から受け取りました。
番号が指す Figshare の記録の中身は、確かめていません。
2026-10-13 の Figshare の稿（`10.6084/m9.figshare.34419198`）の新しい版ではなく、別の項目です。

## 二つ目の稿：穴が 0 にあるときの同時連続性（β > 1）

`continuity/` に、二つ目の稿 "Joint Continuity in (β, t) of the Hausdorff Dimension of Survivor Sets of β-Transformations with a Hole at 0, for All β > 1" の原稿・PDF・台本・出力を置いています。
Figshare には出しません。一つ目の稿とほぼ同じ内容だと、2026-11-19 に所有者が判断しました。記録として、ここにだけ置きます。
DOI はまだ受け取っていません。
上の稿（`10.6084/m9.figshare.35050300`）の新しい版ではありません。
上の稿の原稿と PDF には手を入れていません。

上の稿の定理 E は、β ≤ 2 の範囲で、Lu・Steiner・Zou の定理 1.4 を仮定して同時連続性を示しました。
二つ目の稿は、有限の字母の辞書式シフトについて、内側からの近似（Theorem IA）を記号の側だけで示します。
証明の要は支えの補題です。
そこから、エントロピー h(Σ_{a,b}) が (a, b) について連続であること（Corollary C）と、(β, t) ↦ dim_H K_β(t) が (1, ∞) × [0, 1) で同時連続であること（Corollary E）を導きます。
Corollary E は条件付きです。
条件は三つあります。
一つ目は Allaart・Kong の補題 6.2 で、Raith から導けると書かれています（Raith の論文は読んでいません）。
二つ目は同じ論文の補題 4.1 と 4.2 です。
三つ目は上の稿の定理 7.1 で、外の査読をまだ通っていません。
Lu・Steiner・Zou の定理 1.4 には、もう依りません。

| 結果 | 状態 |
| --- | --- |
| Corollary C、M = 1 | 知られている（Lu・Steiner・Zou が引く Labarca・Moreira） |
| Corollary C、M ≥ 2 | おそらく知られている（Bandtlow・Rugh の定理 1.2 からおそらく従う。Raith は読んでいない） |
| β を固定したときの t についての連続性 | β ∈ (1, 2) では知られている（Kalle・Kong・Langeveld・Li の命題 2.5） |
| Theorem IA（支えの補題による証明） | 読んだ文献には見つからなかった |
| Corollary E（β > 1 での同時連続性） | 条件付き。読んだ文献には見つからなかった。Allaart・Kong の注意 1.2 は分からないとしている |

各結果が通った三つの検査は `continuity/REFEREE.md` に書いています。
紙面は 12 頁です。

## この稿について

三人の繰り返しゲームで、割引因子が 1/φ < δ < 2/3 の窓にあるとき、純戦略の均衡利得の集合がフラクタルになります。
Figshare の稿（`10.6084/m9.figshare.34419198`、2026-10-13）は、その集合について黄金比の窓の予想を述べました。
あちらは凍結してあり、予想は予想のまま残します。
この稿は、その予想を解決し、背後にある開いた力学系についての結果を足した別の記録です。

集合は、尺度を除けば、貪欲な β 変換 y ↦ βy mod 1（β = 1/δ）に穴 (t(β), 1)、t(β) = (2 − β)/(β − 1) を開けたときの生き残りの集合です。
この見方そのものは新しい数学ではありません。
測度零、次元の式、次元が 1 より小さいことは、Lu・Steiner・Zou の定理 1.2 と命題 2.5 の特別な場合です。
稿では初等的な証明を付け、結果はこの三人のものとして書いています。

## 何が知られていて、何が新しいか

紙面の状態の表（Status of each result）と同じです。
「新しい」は「読んだ文献には見つからなかった」という意味で、それ以上は主張しません。

| 結果 | 状態 |
| --- | --- |
| 測度零（命題 8） | 知られている（Lu・Steiner・Zou 命題 2.5、Rényi・Parry） |
| 次元の式と次元 < 1（命題 9 の前半） | 知られている（Lu・Steiner・Zou 定理 1.2） |
| 曲線に沿った単調性・連続性・両端の極限 | 読んだ文献には見つからなかった |
| 定理 A・B（両端での速さ）、定理 C（悪魔の階段と台地）、定理 D（1/φ が二度出る理由） | 読んだ文献には見つからなかった |
| 露出した辺への一般化、普遍の窓、線形ジレンマの窓 | 読んだ文献には見つからなかった（応用） |
| 定理 E（穴が 0 にあるときの同時連続性、β ≤ 2） | 条件付き（Lu・Steiner・Zou 定理 1.4 に依る） |
| 有限の字母の辞書式シフトのエントロピーの式 | 写像の形では Oliveira のもの。記号の側の証明を付けた |
| Trinity-Infinity の三篇の点検と Series II のゲーム | 紙面のその部分の表に、知られているもの・見つからなかったもの・九つの値でだけ証明したものを分けてある |

## 中身

| 場所 | 中身 |
| --- | --- |
| `paper/` | LaTeX の原稿と、組んだ PDF |
| `scripts/curve/` | 窓の曲線に沿った数（定理 A〜E、命題 9 の表） |
| `scripts/edges/` | 辺への一般化と窓の表 |
| `scripts/symbolic/`、`scripts/symbolic-referee/` | 有限の字母の辞書式シフトの節。後者は査読のために別に書いた台本です |
| `scripts/trinity/` | Trinity-Infinity の三篇の点検と Series II のゲームの節 |
| `expected/` | 各台本の出力。検査はこれと一字一句で比べます |
| `verification/` | 検査 |
| `figshare/` | Figshare に置く五つの品と、それを作る台本 |
| `continuity/paper/` | 二つ目の稿の LaTeX の原稿と、組んだ PDF |
| `continuity/scripts/`、`continuity/expected/` | 二つ目の稿の数を出す台本と、その出力 |
| `continuity/REFEREE.md` | 二つ目の稿の査読の記録 |

`verification/check_numbers.py` は、表に載せた紙面の数を、それぞれの台本の出力と突き合わせます。
紙面にある小数点以下三桁以上の数で、突き合わせの行が無いものがあれば落ちます。
小数点以下が二桁までの数と整数は、表に載せたものだけを突き合わせます。
二つ目の稿は `verification/check_numbers_continuity.py` が同じことをします。
こちらは m·10^{e} の形の数も、行が無ければ落ちます。

```
python3 -m pip install -r requirements.txt
python3 verification/run_scripts.py
python3 verification/check_numbers.py
python3 verification/check_numbers_continuity.py
python3 verification/check_text.py
python3 verification/check_copies.py
python3 verification/check_figshare.py
```

## Figshare に置く品（figshare/）

黄金比の窓の予想について、Figshare に置く五つの品を `figshare/` に置いています。
図、数表、台本の束、ポスター、スライドです。
どれも `figshare/build.py` が作ります。
手では直しません。
数表は 11 の CSV です。
どの値も、`expected/` にある台本の出力の文字列をそのまま写しています。
台本の束は、commit `c2a47fd` を `git archive` で固めた zip で、95 のファイルを含みます。
ポスターは A0 の縦で 1 頁です。
スライドは 11 枚です。
ポスターとスライドの書き方は、紙面の状態の表に合わせています。
Lu・Steiner・Zou の特別な場合にあたる結果は、彼らのものとして書いています。
曲線に沿った結果と応用は「読んだ文献には見つからなかった」と書き、それ以上は主張しません。
定理 E は条件付きと書いています。
Figshare の欄に貼る文面は `figshare/METADATA.md` にあります。
Figshare への登録は所有者のアカウントで行うもので、Claude には触れられません。
五つの品は、2026-11-24 に所有者が Figshare に出しました。
DOI は、同じ日に DataCite で読み、所有者が書くことを認めました。

| 品 | Figshare の種別 | DOI |
| --- | --- | --- |
| 図 | Figure（Image） | [`10.6084/m9.figshare.35094328`](https://doi.org/10.6084/m9.figshare.35094328) |
| 数表 | Dataset | [`10.6084/m9.figshare.35094355`](https://doi.org/10.6084/m9.figshare.35094355) |
| 台本の束 | Software | [`10.6084/m9.figshare.35094370`](https://doi.org/10.6084/m9.figshare.35094370) |
| ポスター | Poster | [`10.6084/m9.figshare.35094385`](https://doi.org/10.6084/m9.figshare.35094385) |
| スライド | Presentation | [`10.6084/m9.figshare.35094490`](https://doi.org/10.6084/m9.figshare.35094490) |

`verification/check_figshare.py` は、作り直して一字一句同じになること、CSV が `expected/` と合うこと、文面の語と数を確かめます。

## 各結果が通った三つの検査

紙面の査読（決めごと 18）で、各部分を三つの検査に掛けました。
一つ目は証明の導き直しです。
二つ目と三つ目は、下の台本です。

| 結果 | 二つ目（式の評価） | 三つ目（式を使わない計算） |
| --- | --- | --- |
| β 変換への帰着 | `curve/membership.py`（厳密な有理数） | `edges/examples.py`（三つの根と語の数え上げ） |
| 測度零（命題 8） | `edges/check_misc.py`（穴の大きさ） | `edges/check_dichotomy.py`（長さの減少） |
| 命題 9 | `edges/examples.py`（更新方程式と LSZ の根） | `curve/check_count.py`（柱の数え上げ）、`edges/monotone.py` |
| 定理 A | `curve/t1_lower.py` | `curve/check_count2.py` |
| 定理 B | `curve/t2_upper.py`、`curve/t2_parry.py` | `curve/check_count2.py` |
| 定理 C | `curve/t3_plateaus.py` | `curve/check_count.py`（台地の上の値） |
| 定理 D | `curve/t4_why_phi.py`（記号計算） | `curve/t4_why_phi.py`（割引和の直接の模擬と二分法） |
| 辺への帰着・普遍の窓 | `edges/check_reduction.py`、`edges/check_universal.py` | `edges/check_misc.py`（命題 5 の再現） |
| 線形ジレンマの窓・単調性 | `edges/examples.py`（閉じた形） | `edges/edges.py`（全探索）、`edges/monotone.py` |
| 定理 E（条件付き） | `curve/t5_hole0.py` | `curve/t5_jump.py` |
| 辞書式シフトの式 | `symbolic/check1_series.py` | `symbolic-referee/bf.py`（別に書いた総当たり） |
| 系と β 有理数の修正 | `symbolic-referee/cases.py` | `symbolic-referee/theta.py`、`symbolic-referee/empty.py` |
| Trinity-Infinity の主張の点検 | `trinity/s2_claims.py` | `trinity/s1_s3_claims.py` |
| 面の上の均衡集合・利得差の上界 | `trinity/face_check.py` | `trinity/run_diff_check.py`（自己生成の作用素の外側からの近似） |
| 一度も支えられない点 | `trinity/run_aps_test.py` | `trinity/run_aps_face1.py` |
| δ ≤ 1/√2 での全体 | `trinity/run_p23_exact.py`・`trinity/run_p23_infeas.py`（厳密な有理数の証明書） | `trinity/run_p23_scan.py`・`trinity/run_p23_gen.py`・`trinity/run_p23_facets.py` |
| 作用素の切り替え | `trinity/jsr_check.py` | `trinity/jsr_cycle.py` |
| 多人数の輪番の閾値 | `trinity/rot_asym.py`（200 桁） | `trinity/rot_asym.py`（割引和の直接の和） |

## 文献の読み方

文献の確認は 2026-11-18 に行いました。
arXiv で読めたものは本文を読み、読めなかったものは要旨だけ、または記憶によるものとして、紙面の文献の節（Literature, and how each item was read）に区別して書いています。
Berg・Kitti と Mailath・Obara・Sekiguchi の本文は読めていません。
二つ目の稿の読み方は、その紙面の文献の節にあります。
上の稿の系 7.2 の証明は、Allaart・Kong の補題 6.2 の出どころを Raith の 1989 年の論文としています。
Allaart・Kong が挙げているのは Raith の 1994 年の論文です。
この食い違いは、二つ目の稿の文献の節と `continuity/REFEREE.md` に書きました。

## 言語モデルの利用

Claude Code（Anthropic）を使いました。
文献を探して読むこと、証明の下書きと確認、検査の台本、文章の下書きに使っています。
内容の責任は著者が負います。
Claude は著者ではありません。

## 誤りの知らせと個人の情報

誤りは、issue の様式「誤りの知らせ」で受けます。
2026-12-01 から、その issue は突き合わせの受付で確かめます。
受付の道具とワークフロー（`.github/checked-intake/verify.js`、`.github/workflows/checked-intake.yml`）は、運営者のほかのリポジトリと一字一句同じ写しです。
issue で届いた個人の情報の扱いと、開示・訂正・利用の停止・消去の求め方は、運営者の[免責事項](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/DISCLAIMER.md)の「情報の扱い」の節にあります。
その節は、このリポジトリにも掛かります。
題と本文を言語モデルに渡すときの扱いは、同じ免責事項の「issue の中身と言語モデル」の節にあります。

`SECURITY.md` も、運営者のほかのリポジトリと一字一句同じ写しです。
その中の「免責事項」は、上の免責事項のことです。
その中の「2026-11-12 に確かめました」は、写しのもとのリポジトリで確かめた日です。
このリポジトリは 2026-11-18 に作りました。
このリポジトリでも GitHub の非公開の脆弱性報告が有効でないことを、2026-11-19 に GitHub の API で確かめました。

## ライセンス

稿と散文は CC BY 4.0（`LICENSE`）、台本と検査は MIT（`LICENSE-CODE`）です。
稿が引く他の著者の文（定理・補題・注意などの文）は、CC BY 4.0 でも MIT でも許諾しておらず、それぞれの権利者のものです。
