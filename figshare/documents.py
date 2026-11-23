"""The Poster and Presentation items: LaTeX sources written from templates, then compiled.

Every number with three or more decimals is taken from expected/ (through tables.py), never typed here.
The wording of the status of each result follows the table "Status of each result" of the paper, with
"new (not found in texts read)" written as "not found in the texts read" and nothing more claimed.

The PDFs are reproducible: SOURCE_DATE_EPOCH and FORCE_SOURCE_DATE fix the dates, \\pdftrailerid{} drops the
file identifier, and \\pdfsuppressptexinfo drops the path of the included figure.
"""
import os
import shutil
import subprocess
import tempfile

EPOCH = "1795392000"  # 2026-11-24 00:00:00 UTC
FIGSHARE_PAPER = "10.6084/m9.figshare.35050300"
FIGSHARE_CONJECTURE = "10.6084/m9.figshare.34419198"
REPO = "https://github.com/cpsbvbng26-dotcom/golden-window-resolution"
ORCID = "0009-0000-1406-0547"

PREAMBLE_COMMON = r"""\pdftrailerid{}
\pdfsuppressptexinfo=-1
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{graphicx}
<<HYPERREF>>\hypersetup{pdfauthor={Takuya Nemoto},pdftitle={<<PDFTITLE>>},pdfsubject={CC BY 4.0},pdfcreator={},pdfproducer={}}
\newcommand{\dimH}{\dim_{\mathrm H}}
"""

STATUS_ROWS = [
    (r"Reduction to $T_\beta$ with the hole $(t(\beta),1)$", r"elementary; the observation is not new mathematics; the game form was not found in the texts read"),
    (r"Theorem 3.1: measure zero", r"known: Lu--Steiner--Zou, Prop.~2.5; R\'enyi--Parry ergodicity"),
    (r"Theorem 3.2(1) formula, (2) $\dim<1$", r"known: Lu--Steiner--Zou, Thm.~1.2 with Lemma~2.7 and Prop.~2.5; entropy also Kuang--Li--Xiao, Thm.~4.3"),
    (r"Theorem 3.2(1) $\dim_{\mathrm B}=\dimH$", r"not found in the texts read (standard methods)"),
    (r"Theorem 3.2(3) monotone, continuous, end limits", r"not found in the texts read (along the coupled curve)"),
    (r"Theorems A and B (rates at both ends)", r"not found in the texts read; the mechanism of B is classical (recalled)"),
    (r"Theorem C (devil's staircase, plateaus)", r"not found in the texts read along the curve; fixed-$\beta$ analogues are known"),
    (r"Theorem D (the two thresholds coincide)", r"not found in the texts read (application inside the model)"),
    (r"Prop.~5.1 (edge reduction)", r"instance of the framework of Berg and Kitti (abstract read)"),
    (r"Props.~5.2--5.4 (windows, monotonicity)", r"not found in the texts read (application)"),
    (r"Theorem E (joint continuity, $\beta\le2$)", r"conditional on Lu--Steiner--Zou, Thm.~1.4"),
    (r"Theorem 7.1 (entropy identity)", r"known at map level (Oliveira); a symbolic proof is given"),
]

DISCLOSURE_EN = (
    "This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. "
    "The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, "
    "to draft and check the proofs, to write and run the verification scripts, and to draft the text. "
    "The author is responsible for the content. Claude is not an author.")


def prefix(value, digits):
    """The printed value cut after `digits` decimals (a prefix of the string in expected/)."""
    whole, frac = value.split(".")
    return whole + "." + frac[:digits]


def values(tables):
    """Numbers for the poster and the slides, all from the built tables (strings from expected/)."""
    t = {fname: rows for fname, _, rows, _ in tables}
    const = {r["name"]: r["value"] for r in t["constants.csv"]}
    lower = {r["k"]: r for r in t["theorem_A_lower_end.csv"]}
    upper = {r["k"]: r for r in t["theorem_B_upper_end.csv"]}
    return {
        "C": prefix(const["C"], 13), "M": prefix(const["M"], 13),
        "PL": const["plateau_1_4_left"], "PR": const["plateau_1_4_right"], "PH": const["plateau_1_4_entropy"],
        "NA": const["distinct_finite_A"],
        "A10": lower["10"]["dim"], "N10": lower["10"]["N"], "A80": lower["80"]["dim"], "N80": lower["80"]["N"],
        "B6": upper["6"]["ratio_to_C"], "B10": upper["10"]["ratio_to_C"],
        "T5": t["prop9_dimension.csv"],
    }


def table5_tex(rows, short=False):
    head = r"$\delta$ & renewal & LSZ & counts\\" if short else r"$\delta$ & renewal equation & root of LSZ Thm.~1.2 & word counts\\"
    out = [r"\begin{tabular}{lccc}", r"\toprule", head, r"\midrule"]
    for r in rows:
        out.append(f"{r['delta']} & {r['dim_renewal']} & {r['dim_lsz']} & {r['dim_word_count']}\\\\")
    out += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def status_tex(width_a, width_b):
    out = [rf"\begin{{tabular}}{{>{{\raggedright}}p{{{width_a}}}>{{\raggedright\arraybackslash}}p{{{width_b}}}}}", r"\toprule", r"Result & Status\\", r"\midrule"]
    out += [f"{a} & {b}\\tabularnewline" for a, b in STATUS_ROWS]
    out += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def fill(template, v, extra):
    s = template
    for k, val in {**{k: x for k, x in v.items() if isinstance(x, str)}, **extra}.items():
        s = s.replace(f"<<{k}>>", val)
    assert "<<" not in s, s[s.index("<<"):s.index("<<") + 40]
    return s


POSTER = r"""\documentclass[25pt,a0paper,portrait,margin=0mm,innermargin=18mm,blockverticalspace=9mm,colspace=18mm]{tikzposter}
<<PREAMBLE>>
\usetheme{Simple}
\definecolor{ink}{HTML}{1F3A5F}
\definecolor{accent}{HTML}{B5532A}
\definecolor{paper}{HTML}{FFFFFF}
\colorlet{titlebgcolor}{ink}
\colorlet{blocktitlebgcolor}{ink}
\colorlet{blocktitlefgcolor}{ink}
\colorlet{backgroundcolor}{paper}
\colorlet{blockbodybgcolor}{paper}
\colorlet{framecolor}{ink}
\settitle{\centering\vbox{\color{white}{\fontsize{78}{90}\selectfont\bfseries Resolution of the Golden-Window Conjecture\par}
\vspace{6mm}{\Large survivor sets of a $\beta$-transformation whose hole moves with the base\par}
\vspace{10mm}{\large Takuya Nemoto \quad ORCID <<ORCID>>\par}
\vspace{4mm}{\normalsize Poster of the preprint DOI <<PAPER>> (Figshare, 2026). Not peer reviewed.\par}}}
\tikzposterlatexaffectionproofoff
\begin{document}
\maketitle[width=0.94\linewidth]
\begin{columns}
\column{0.5}
\block{The game and the conjecture}{
Three players repeat a game in which each chooses C or D; a player with $k$ cooperating co-players gets $k+1$ for C and $k+2$ for D.
Payoffs are discounted by $\delta$, and strategies are pure with no public randomization.
$T_\delta$ is the set of $t\in(0,1]$ such that $(2+t,4-t,2+t)$ is a pure-strategy equilibrium payoff.

\medskip
The preprint DOI <<CONJ>> (Figshare, 13 October 2026) found the window $1/\varphi<\delta<2/3$, $\varphi$ the golden ratio, and stated the
\textbf{golden-window conjecture}: in the window, (a) $T_\delta$ has Lebesgue measure zero; (b) its Hausdorff dimension is below $1$,
continuous and non-decreasing in $\delta$, and runs from $0$ to $1$. That preprint is frozen and keeps the conjecture as a conjecture.
}
\block{The reduction}{
With $\beta=1/\delta$ and $t(\beta)=(2-\beta)/(\beta-1)$, the set is, up to scaling, the survivor set
\[
K_\delta=\{y\in[0,1):\ T_\beta^n(y)\le t(\beta)\ \text{for all } n\ge0\},\qquad T_\beta(y)=\beta y-\lfloor\beta y\rfloor ,
\]
of the greedy $\beta$-transformation with the hole $(t(\beta),1)$. This observation is not new mathematics.
On the curve $t=t(\beta)$ the base and the hole move together.
}
\block{Resolution: known results, elementary proofs}{
Measure zero (Theorem 3.1), the dimension formula
\[
\dimH T_\delta=s,\qquad \Sigma_{n\in A_\delta}\,\delta^{ns}=1,
\]
with $A_\delta$ the first-return times of a forced path, and the bound $\dim<1$ (Theorem 3.2(1)--(2)) are special cases of a theorem of
\textbf{Lu, Steiner and Zou} (Theorem 1.2, Lemma 2.7, Proposition 2.5). The credit for these statements is theirs.
The paper gives elementary, self-contained proofs.
}
\block{Survivor sets across the window}{
\begin{center}\includegraphics[width=0.8\linewidth]{golden-window-figure.pdf}\end{center}
\small (a) $K_\delta$ at 480 values of $\delta$, drawn to within $10^{-3}$ (a finite computation, not the limit set itself).
(b) $\dimH K_\delta$ from the renewal equation; the points are Table 5 of the paper.
}
\block{Table 5: $\dimH T_\delta$ three ways}{
\begin{center}
<<TABLE5>>
\end{center}
}
\column{0.5}
\block{Along the curve: not found in the texts read}{
``Not found in the texts read'' is the strongest claim made here; the literature search was limited.

\medskip
\textbf{Theorem 3.2(3).} $\delta\mapsto\dimH T_\delta$ is strictly increasing and continuous on the window, with limit $0$ at $1/\varphi$ and $1$ at $2/3$.

\medskip
\textbf{Theorem A (lower end).} With $L=\log(1/(\delta-1/\varphi))$, $\dim(\delta)=W(L/\log\varphi)/L+O((\log L)^2/L^2)$, $W$ the Lambert function.
At $\delta=1/\varphi+10^{-10}$ ($N=<<N10>>$) the dimension is <<A10>>; at $\delta=1/\varphi+10^{-80}$ ($N=<<N80>>$) it is <<A80>>.

\medskip
\textbf{Theorem B (upper end).} $(1-\dim(\delta))/(2/3-\delta)\to C=9/(M\log(3/2))$, where $C=<<C>>\ldots$ and $M=<<M>>\ldots$;
at $\delta=2/3-10^{-10}$ the ratio to $C$ is <<B10>>.

\medskip
\textbf{Theorem C (devil's staircase).} The entropy $h$ is continuous, non-decreasing and has $h'=0$ almost everywhere.
Its plateaus are the parameter intervals with a fixed finite return set; the plateau with $A_\delta=\{1,4\}$ is
$[<<PL>>,\,<<PR>>]$ with $h=<<PH>>$. A scan of 20{,}000 parameters found <<NA>> distinct finite sets $A_\delta$.

\medskip
\textbf{Theorem D (why $1/\varphi$ appears twice).} In the linear dilemma with cost $c$ and benefit $b$, the threshold of the three-player
rotation and the lower end of the window both equal $(\sqrt{1+4r}-1)/2$, $r=c/b$: the continuation values of the two binding constraints differ by one discounted cycle.
}
\block{Applications: not found in the texts read}{
The reduction extends to exposed edges of repeated games (an instance of the framework of Berg and Kitti, abstract read),
gives a universal window, and gives closed-form windows $\theta_k(r)<\delta<U_k(r)$ for linear dilemmas (Propositions 5.2--5.4).
}
\block{Conditional}{
\textbf{Theorem E.} Assuming Theorem 1.4 of Lu, Steiner and Zou, $(\beta,t)\mapsto\dimH K_\beta(t)$ for the hole at $0$ is jointly continuous on $(1,2]\times[0,1)$.
The proof of that theorem was read but not re-verified line by line.
}
\block{Status of each result}{
<<STATUS>>
}
\block{Disclosure}{
<<DISCLOSURE>>
The paper also has a separate part on the Trinity-Infinity papers, not summarised here.
Scripts: <<REPO>> (MIT). Poster: CC BY 4.0.
}
\end{columns}
\end{document}
"""

SLIDES = r"""\documentclass[aspectratio=169,11pt]{beamer}
<<PREAMBLE>>
\usetheme{default}
\usecolortheme{default}
\definecolor{ink}{HTML}{1F3A5F}
\definecolor{accent}{HTML}{B5532A}
\setbeamercolor{frametitle}{fg=ink}
\setbeamercolor{title}{fg=ink}
\setbeamercolor{structure}{fg=ink}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{\hfill\scriptsize\color{gray} Takuya Nemoto \quad CC BY 4.0 \quad \insertframenumber/\inserttotalframenumber\hspace*{4mm}\vspace*{2mm}}
\title{Resolution of the Golden-Window Conjecture}
\subtitle{survivor sets of a $\beta$-transformation whose hole moves with the base}
\author{Takuya Nemoto\\[1mm]\small ORCID <<ORCID>>}
\date{\small Slides of the preprint DOI <<PAPER>> (Figshare, 2026)\\Not peer reviewed}
\begin{document}
\begin{frame}
\titlepage
\end{frame}

\begin{frame}{The game}
\begin{itemize}
\item Three players choose C or D; with $k$ cooperating co-players, C gives $k+1$ and D gives $k+2$.
\item Repeated with discount factor $\delta$; pure strategies, perfect monitoring, no public randomization.
\item $T_\delta$: the set of $t\in(0,1]$ such that $(2+t,\,4-t,\,2+t)$ is a pure-strategy equilibrium payoff.
\item Window: $1/\varphi<\delta<2/3$, $\varphi$ the golden ratio. There $T_\delta$ is a fractal.
\end{itemize}
\end{frame}

\begin{frame}{The golden-window conjecture}
Stated in the preprint DOI <<CONJ>> (Figshare, 13 October 2026). In the window:
\begin{enumerate}
\item[(a)] $T_\delta$ has Lebesgue measure zero;
\item[(b)] $\dimH T_\delta$ is below $1$, continuous and non-decreasing in $\delta$, and runs from $0$ to $1$.
\end{enumerate}
\medskip
That preprint is frozen and keeps the conjecture as a conjecture. The paper DOI <<PAPER>> is a separate record.
\end{frame}

\begin{frame}{The reduction}
With $\beta=1/\delta$ and $t(\beta)=(2-\beta)/(\beta-1)$, up to scaling $T_\delta$ is the survivor set
\[
K_\delta=\{y\in[0,1):\ T_\beta^n(y)\le t(\beta)\ \forall n\ge0\},\qquad T_\beta(y)=\beta y-\lfloor\beta y\rfloor .
\]
\begin{itemize}
\item The greedy $\beta$-transformation with the hole $(t(\beta),1)$.
\item This observation is not new mathematics.
\item On the curve $t=t(\beta)$ the base and the hole move together.
\end{itemize}
\end{frame}

\begin{frame}{Resolution: known results}
\begin{itemize}
\item Measure zero (Theorem 3.1).
\item $\dimH T_\delta=s$ with $\sum_{n\in A_\delta}\delta^{ns}=1$, and $\dim<1$ (Theorem 3.2(1)--(2)).
\end{itemize}
These are special cases of a theorem of \textbf{Lu, Steiner and Zou} (Theorem 1.2, Lemma 2.7, Proposition 2.5).
The credit for these statements is theirs. The paper gives elementary proofs.
\end{frame}

\begin{frame}{Survivor sets and dimension across the window}
\begin{columns}[T]
\column{0.5\textwidth}
\includegraphics[height=0.78\textheight]{golden-window-figure.pdf}
\column{0.46\textwidth}
\small
(a) $K_\delta$ at 480 values of $\delta$, drawn to within $10^{-3}$: a finite computation, not the limit set.

\medskip
(b) $\dimH K_\delta$ from the renewal equation. Points: Table 5 (renewal equation, root of Lu--Steiner--Zou Thm.~1.2, word counts).

\medskip
\scriptsize
<<TABLE5>>
\end{columns}
\end{frame}

\begin{frame}{Along the curve (not found in the texts read)}
\begin{itemize}
\item \textbf{Theorem 3.2(3).} $\delta\mapsto\dimH T_\delta$ is strictly increasing and continuous, with limits $0$ at $1/\varphi$ and $1$ at $2/3$.
\item \textbf{Theorem A.} $\dim(\delta)=W(L/\log\varphi)/L+O((\log L)^2/L^2)$, $L=\log(1/(\delta-1/\varphi))$.\\
At $\delta=1/\varphi+10^{-10}$: $N=<<N10>>$ and $\dim=<<A10>>$.
\item \textbf{Theorem B.} $(1-\dim)/(2/3-\delta)\to C=9/(M\log(3/2))=<<C>>\ldots$, $M=<<M>>\ldots$\\
At $\delta=2/3-10^{-6}$ the ratio to $C$ is <<B6>>.
\end{itemize}
\medskip
\small ``Not found in the texts read'' is the strongest claim made. The literature search was limited.
\end{frame}

\begin{frame}{Staircase and the golden ratio twice (not found in the texts read)}
\begin{itemize}
\item \textbf{Theorem C.} The entropy $h$ is a devil's staircase. Its plateaus are the parameter intervals with a fixed finite return set $A_\delta$.\\
$A_\delta=\{1,4\}$ on $[<<PL>>,\,<<PR>>]$, where $h=<<PH>>$.\\
A scan of 20{,}000 parameters found <<NA>> distinct finite sets.
\item \textbf{Theorem D.} In the linear dilemma with $r=c/b$, the threshold of the three-player rotation and the lower end of the window
both equal $(\sqrt{1+4r}-1)/2$. For $r=1$ this is $1/\varphi$.
\end{itemize}
\end{frame}

\begin{frame}{Applications and a conditional result}
\begin{itemize}
\item Exposed edges of repeated games, a universal window, closed-form windows for linear dilemmas (Propositions 5.2--5.4):
not found in the texts read (application). Proposition 5.1 is an instance of the framework of Berg and Kitti.
\item \textbf{Theorem E (conditional).} Assuming Theorem 1.4 of Lu, Steiner and Zou, $(\beta,t)\mapsto\dimH K_\beta(t)$ for the hole at $0$ is jointly
continuous on $(1,2]\times[0,1)$. That proof was read but not re-verified line by line.
\end{itemize}
\end{frame}

\begin{frame}{Status of each result}
\scriptsize
<<STATUS>>
\end{frame}

\begin{frame}{Disclosure and materials}
\small
<<DISCLOSURE>>

\medskip
The paper also has a separate part on the Trinity-Infinity papers, not summarised here.

\medskip
\begin{itemize}
\item Paper (resolution): DOI <<PAPER>>
\item Preprint that stated the conjecture: DOI <<CONJ>>
\item Scripts and outputs: \url{<<REPO>>} (MIT)
\item These slides: CC BY 4.0
\end{itemize}
\end{frame}
\end{document}
"""


def compile_pdf(tex_name, tex_text, figure_pdf, outdir):
    env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1", TZ="UTC")
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, tex_name), "w", encoding="utf-8") as fh:
            fh.write(tex_text)
        shutil.copy(figure_pdf, os.path.join(tmp, "golden-window-figure.pdf"))
        for _ in range(2):
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name],
                               cwd=tmp, env=env, capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(r.stdout[-3000:])
        log = open(os.path.join(tmp, tex_name[:-4] + ".log"), encoding="latin-1").read()
        shutil.copy(os.path.join(tmp, tex_name[:-4] + ".pdf"), os.path.join(outdir, tex_name[:-4] + ".pdf"))
        return log


def build(root_out, tables, figure_pdf):
    v = values(tables)
    common = {"ORCID": ORCID, "PAPER": FIGSHARE_PAPER, "CONJ": FIGSHARE_CONJECTURE, "REPO": REPO,
              "DISCLOSURE": DISCLOSURE_EN}
    out = {}
    for name, template, title, status_w in (
            ("poster", POSTER, "Resolution of the Golden-Window Conjecture (poster)", ("14cm", "23cm")),
            ("slides", SLIDES, "Resolution of the Golden-Window Conjecture (slides)", ("5.3cm", "7.7cm"))):
        d = os.path.join(root_out, name)
        os.makedirs(d, exist_ok=True)
        pre = PREAMBLE_COMMON.replace("<<PDFTITLE>>", title).replace(
            "<<HYPERREF>>", "\\usepackage[hidelinks]{hyperref}\n" if name == "poster" else "")
        tex = fill(template, v, dict(common, PREAMBLE=pre, STATUS=status_tex(*status_w),
                                         TABLE5=table5_tex(v["T5"], short=(name == "slides"))))
        tex_name = f"golden-window-{name}.tex"
        with open(os.path.join(d, tex_name), "w", encoding="utf-8") as fh:
            fh.write(tex)
        compile_pdf(tex_name, tex, figure_pdf, d)
        out[name] = os.path.join(d, tex_name[:-4] + ".pdf")
    return out
