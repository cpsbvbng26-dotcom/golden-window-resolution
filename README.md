# golden-window-resolution

Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game（黄金比の窓の予想の解決と、穴の開いた β 変換についての関連する結果）の原稿・PDF・検査の台本を置いています。

[English](README.en.md)

稿は Figshare にあります。DOI は [`10.6084/m9.figshare.35050300`](https://doi.org/10.6084/m9.figshare.35050300) です。
番号は 2026-11-18 に利用者から受け取りました。
番号が指す Figshare の記録の中身は、確かめていません。
2026-10-13 の Figshare の稿（`10.6084/m9.figshare.34419198`）の新しい版ではなく、別の項目です。

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

紙面に印字した数は、すべてどれかの台本の出力にあります。
`verification/check_numbers.py` が、紙面の数と出力を突き合わせます。
小数点以下三桁以上の数で、突き合わせの行が無いものがあれば落ちます。

```
python3 -m pip install -r requirements.txt
python3 verification/run_scripts.py
python3 verification/check_numbers.py
python3 verification/check_text.py
python3 verification/check_copies.py
```

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

## 言語モデルの利用

Claude Code（Anthropic）を使いました。
文献を探して読むこと、証明の下書きと確認、検査の台本、文章の下書きに使っています。
内容の責任は著者が負います。
Claude は著者ではありません。

## ライセンス

稿と散文は CC BY 4.0（`LICENSE`）、台本と検査は MIT（`LICENSE-CODE`）です。
