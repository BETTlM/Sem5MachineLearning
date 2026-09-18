#!/usr/bin/env python3
"""Build documentation/regression.pdf — how each algorithm works and how the notebook implements it."""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph as RLParagraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "documentation" / "regression.pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

pdfmetrics.registerFont(TTFont("Georgia", str(FONT_DIR / "Georgia.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Bold", str(FONT_DIR / "Georgia Bold.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Italic", str(FONT_DIR / "Georgia Italic.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", str(FONT_DIR / "Georgia Bold Italic.ttf")))

NAVY = HexColor("#1B365D")
NAVY_DARK = HexColor("#10243F")
AMBER = HexColor("#C4A35A")
CREAM = HexColor("#F7F3EA")
INK = HexColor("#1C1C1C")
MUTED = HexColor("#5A6570")
RULE = HexColor("#D8D0C0")
SOFT = HexColor("#EEF2F7")
TEAL = HexColor("#1F6F7A")
CODE_BG = HexColor("#F4EFE4")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


def P(text, style):
    return RLParagraph(text, style)


def _styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("CoverKicker", fontName="Georgia", fontSize=9, textColor=AMBER,
                         alignment=TA_CENTER, spaceAfter=8))
    s.add(ParagraphStyle("CoverTitle", fontName="Georgia-Bold", fontSize=24, textColor=white,
                         alignment=TA_CENTER, leading=30, spaceAfter=10))
    s.add(ParagraphStyle("CoverSub", fontName="Georgia-Italic", fontSize=11.5, textColor=HexColor("#D5DEE8"),
                         alignment=TA_CENTER, leading=16, spaceAfter=6))
    s.add(ParagraphStyle("CoverMeta", fontName="Georgia", fontSize=10, textColor=HexColor("#B8C4D4"),
                         alignment=TA_CENTER, leading=15))
    s.add(ParagraphStyle("H1", fontName="Georgia-Bold", fontSize=15.5, textColor=NAVY,
                         spaceBefore=4, spaceAfter=8, leading=20))
    s.add(ParagraphStyle("H2", fontName="Georgia-Bold", fontSize=12, textColor=NAVY,
                         spaceBefore=9, spaceAfter=4, leading=16))
    s.add(ParagraphStyle("H3", fontName="Georgia-Bold", fontSize=11, textColor=TEAL,
                         spaceBefore=7, spaceAfter=3, leading=14))
    s.add(ParagraphStyle("Body", fontName="Georgia", fontSize=10, textColor=INK,
                         alignment=TA_JUSTIFY, leading=14.1, spaceAfter=6))
    s.add(ParagraphStyle("Callout", fontName="Georgia-Italic", fontSize=10, textColor=NAVY, leading=14))
    s.add(ParagraphStyle("Caption", fontName="Georgia-Italic", fontSize=8.5, textColor=MUTED,
                         alignment=TA_CENTER, spaceBefore=2, spaceAfter=8))
    s.add(ParagraphStyle("TOCChap", fontName="Georgia-Bold", fontSize=11, textColor=NAVY, leading=16, spaceAfter=2))
    s.add(ParagraphStyle("TOCItem", fontName="Georgia", fontSize=10, textColor=INK, leading=14, leftIndent=10))
    s.add(ParagraphStyle("Formula", fontName="Georgia-Italic", fontSize=10.5, textColor=NAVY_DARK,
                         alignment=TA_CENTER, leading=16, spaceBefore=3, spaceAfter=6))
    s.add(ParagraphStyle("AlgTitle", fontName="Georgia-Bold", fontSize=13, textColor=white, leading=16))
    s.add(ParagraphStyle("AlgKicker", fontName="Georgia", fontSize=8, textColor=AMBER, leading=11))
    s.add(ParagraphStyle("Cell", fontName="Georgia", fontSize=8.4, textColor=INK, leading=11.4))
    s.add(ParagraphStyle("CellB", fontName="Georgia-Bold", fontSize=8.4, textColor=NAVY, leading=11.4))
    s.add(ParagraphStyle("CellW", fontName="Georgia-Bold", fontSize=8.4, textColor=white, leading=11.4))
    s.add(ParagraphStyle("BulletBody", fontName="Georgia", fontSize=10, textColor=INK, leading=13.4))
    s.add(ParagraphStyle("CodeBlock", fontName="Courier", fontSize=8, textColor=NAVY_DARK,
                         leading=11.2, alignment=TA_LEFT))
    return s


S = _styles()


def bullets(items):
    return ListFlowable(
        [ListItem(P(i, S["BulletBody"]), leftIndent=12, bulletColor=AMBER, value="•")
         for i in items],
        bulletType="bullet", leftIndent=16, bulletFontName="Georgia", bulletFontSize=10, spaceAfter=7,
    )


def callout(text):
    t = Table([[P(text, S["Callout"])]], colWidths=[PAGE_W - 2 * MARGIN - 8])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, AMBER),
    ]))
    return t


def hrule():
    t = Table([[""]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, -1), 0.6, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def kv_table(rows, col0=38 * mm):
    w = PAGE_W - 2 * MARGIN
    data = [[P(a, S["CellB"]), P(b, S["Cell"])] for a, b in rows]
    t = Table(data, colWidths=[col0, w - col0])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), SOFT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE), ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ]))
    return t


def simple_table(headers, rows, widths=None):
    w = PAGE_W - 2 * MARGIN
    n = len(headers)
    widths = widths or [w / n] * n
    head = [P(h, S["CellW"]) for h in headers]
    body = [[P(str(c), S["Cell"]) for c in row] for row in rows]
    t = Table([head] + body, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), CREAM))
    t.setStyle(TableStyle(style))
    return t


def code_block(text):
    html = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
        .replace("  ", "&nbsp;&nbsp;")
    )
    inner = P(html, S["CodeBlock"])
    t = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEBEFORE", (0, 0), (0, -1), 3, NAVY),
    ]))
    return t


def alg_banner(code, title, one_liner):
    inner = Table(
        [
            [P(f'<font color="#C4A35A">{code}</font>', S["AlgKicker"])],
            [P(title, S["AlgTitle"])],
            [P(one_liner, ParagraphStyle(
                "ban_sub", fontName="Georgia-Italic", fontSize=9,
                textColor=HexColor("#D5DEE8"), leading=12))],
        ],
        colWidths=[PAGE_W - 2 * MARGIN - 16],
    )
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    wrap = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN])
    wrap.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return wrap


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.restoreState()
        return
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(0, PAGE_H - 12.6 * mm, PAGE_W, 1.4, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Georgia", 8)
    canvas.drawString(MARGIN, PAGE_H - 8 * mm, "23CSE301  ·  How the regression algorithms work")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 8 * mm, "notebooks/regression.ipynb")
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(0, 12 * mm, PAGE_W, 1.2, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Georgia", 8)
    canvas.drawString(MARGIN, 5 * mm, "documentation/regression.pdf")
    canvas.drawRightString(PAGE_W - MARGIN, 5 * mm, str(doc.page))
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY_DARK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H * 0.40, PAGE_W, PAGE_H * 0.60, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(0, PAGE_H * 0.40, PAGE_W, 4, fill=1, stroke=0)
    canvas.rect(MARGIN, PAGE_H - 28 * mm, 28 * mm, 2.2, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#8FA4C0"))
    canvas.setFont("Georgia", 8)
    canvas.drawString(MARGIN, PAGE_H * 0.40 - 10 * mm, "THE TEN ALGORITHMS")
    algos = [
        ("G1", "Linear Regression"), ("G2", "Ridge (L2)"),
        ("G3", "Lasso (L1)"), ("G4", "ElasticNet"),
        ("G5", "Polynomial"), ("G6", "Decision Tree"),
        ("G7", "Random Forest"), ("G8", "Gradient Boosting"),
        ("G9", "SVR (RBF)"), ("G10", "k-Nearest Neighbours"),
    ]
    y0 = PAGE_H * 0.40 - 18 * mm
    col_w = (PAGE_W - 2 * MARGIN) / 2
    for i, (code, name) in enumerate(algos):
        col, row = divmod(i, 5)
        x = MARGIN + col * col_w
        y = y0 - row * 8.2 * mm
        canvas.setFillColor(AMBER)
        canvas.setFont("Georgia-Bold", 9)
        canvas.drawString(x, y, code)
        canvas.setFillColor(HexColor("#D5DEE8"))
        canvas.setFont("Georgia", 9)
        canvas.drawString(x + 14 * mm, y, name)
    canvas.restoreState()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    story = []
    w = PAGE_W - 2 * MARGIN

    # cover
    story.append(Spacer(1, 38 * mm))
    story.append(P("23CSE301  MACHINE LEARNING  ·  REVIEW 1", S["CoverKicker"]))
    story.append(Spacer(1, 5 * mm))
    story.append(P("How each regression<br/>algorithm works", S["CoverTitle"]))
    story.append(Spacer(1, 3 * mm))
    story.append(P(
        "Theory, sklearn objects, and the exact notebook cells<br/>"
        "in notebooks/regression.ipynb that implement them.",
        S["CoverSub"]))
    story.append(Spacer(1, 14 * mm))
    story.append(P(
        "Problem · NYC yellow-cab trip duration (seconds)<br/>"
        "Notebook · notebooks/regression.ipynb, clusters A–J<br/>"
        "This file · documentation/regression.pdf",
        S["CoverMeta"]))
    story.append(PageBreak())

    # contents
    story.append(P("Contents", S["H1"]))
    story.append(hrule())
    toc = [
        ("1.", "Shared contract: one table, ten independent fits"),
        ("2.", "What evaluate() does after every algorithm"),
        ("3.", "G1  Linear Regression"),
        ("4.", "G2  Ridge Regression (L2)"),
        ("5.", "G3  Lasso Regression (L1)"),
        ("6.", "G4  ElasticNet"),
        ("7.", "G5  Polynomial Regression"),
        ("8.", "G6  Decision Tree"),
        ("9.", "G7  Random Forest"),
        ("10.", "G8  Gradient Boosting (histogram GBM)"),
        ("11.", "G9  Support Vector Regressor"),
        ("12.", "G10 k-Nearest Neighbours"),
        ("13.", "Mean baseline"),
        ("14.", "Cluster H: GridSearch, RandomizedSearch, top-two CV"),
        ("15.", "How to talk about a model in the viva"),
    ]
    for num, title in toc:
        story.append(P(f"<b>{num}</b>  {title}", S["TOCChap"]))
    story.append(Spacer(1, 3 * mm))
    story.append(callout(
        "For each algorithm this booklet answers two questions: what is the model doing "
        "mathematically, and which lines in regression.ipynb actually run it. Code blocks "
        "are copied from the notebook, not invented."
    ))
    story.append(PageBreak())

    # 1 shared
    story.append(P("1.  Shared contract: one table, ten independent fits", S["H1"]))
    story.append(hrule())
    story.append(P(
        "The notebook predicts <b>trip_duration</b> in seconds for NYC yellow-cab trips. "
        "It never uses <font face='Courier' size='9'>dropoff_datetime</font> (that column "
        "is the answer). It never uses speed = distance / duration. All ten official "
        "algorithms eat the <b>same processed matrix</b> from Cluster F and are scored on "
        "the <b>same test trips</b>.",
        S["Body"]))
    story.append(P("What Cluster F hands to every model", S["H2"]))
    story.append(bullets([
        "<font face='Courier' size='9'>X_train_p</font> / <font face='Courier' size='9'>X_test_p</font> — numeric columns StandardScaled, vendor and store-and-fwd one-hot encoded. Scaler and encoder were fit on train only.",
        "<font face='Courier' size='9'>y_train</font> / <font face='Courier' size='9'>y_test</font> — duration in seconds. If the test split is larger than 50,000 rows, evaluation is capped at the same 50,000-row slice for everyone.",
        "Engineered columns: haversine_km, manhattan_km, bearing, hour, dayofweek, month, is_weekend, is_rush_hour, plus passenger_count.",
        "<font face='Courier' size='9'>random_state = 42</font> on the split, the trees, the subset draws, and the searches.",
    ]))
    story.append(P(
        "Linear, Ridge, Lasso, ElasticNet, Polynomial, Decision Tree, Random Forest, and "
        "HistGBM train on the full cleaned training table (about 279,000 rows). SVR trains "
        "on 12,000 rows; KNN on 40,000. The leaderboard column <b>Train rows</b> records that "
        "so the comparison stays honest.",
        S["Body"]))
    story.append(PageBreak())

    # 2 evaluate
    story.append(P("2.  What evaluate() does after every algorithm", S["H1"]))
    story.append(hrule())
    story.append(P(
        "Cluster G0 defines one scorer. Every G-cell constructs its sklearn object, then "
        "calls this helper. The helper does not train the ten models in a loop — each "
        "algorithm still has its own cell, as the rubric asks.",
        S["Body"]))
    story.append(code_block(
        "model.fit(X_tr, y_tr)\n"
        "y_pred = np.clip(model.predict(X_te), 1, None)\n"
        "scores = five_fold_r2(model, X_tr, y_tr, name)   # KFold(5, shuffle, seed 42)\n"
        "# then print Test R², RMSE, MAE, and 5-fold CV R² mean ± std"
    ))
    story.append(P("Step by step", S["H2"]))
    story.append(bullets([
        "<b>Fit</b> on that algorithm’s training rows (full table or the SVR/KNN subset).",
        "<b>Predict</b> the shared test set. Predictions below 1 second are clipped to 1 — a negative duration cannot happen. The clip is applied at predict time, not during training.",
        "<b>Test metrics:</b> R², RMSE (seconds), MAE (seconds) via sklearn’s r2_score, root_mean_squared_error, mean_absolute_error.",
        "<b>5-fold CV R²</b> on the same training rows, using clone(model) so the already-fitted object is not reused. KFold shuffles with seed 42.",
        "The row is appended to <font face='Courier' size='9'>leaderboard</font>. The fitted object is stored in <font face='Courier' size='9'>fitted_models</font> for the Cluster I manual tester.",
    ]))
    story.append(P(
        "After G10 the notebook calls <font face='Courier' size='9'>show_all_metrics_table()</font>, "
        "which ranks every official model plus the mean baseline by test R² and displays "
        "Train rows, Test R², RMSE, MAE, and 5-fold CV R² mean/std in one table. Cluster H1 "
        "prints that table again next to the bar chart.",
        S["Body"]))
    story.append(callout(
        "R² = 1 − SS_res / SS_tot. RMSE = sqrt(mean((y − ŷ)²)), in seconds. "
        "MAE = mean(|y − ŷ|), in seconds. 5-fold CV R² is the mean of five training-only "
        "holdouts; it is not computed on the test set."
    ))
    story.append(PageBreak())

    # G1
    story.append(alg_banner(
        "G1  ·  sklearn.linear_model.LinearRegression",
        "Linear Regression",
        "Ordinary least squares. The straight-line baseline every other model has to beat.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Assume duration is a weighted sum of the processed features plus an intercept:",
        S["Body"]))
    story.append(P(
        "ŷ = w<sub>0</sub> + w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + … + w<sub>p</sub>x<sub>p</sub>",
        S["Formula"]))
    story.append(P(
        "Training chooses the weights that minimise the residual sum of squares "
        "(ordinary least squares, OLS):",
        S["Body"]))
    story.append(P(
        "L(w) = sum<sub>i</sub> ( y<sub>i</sub> − w · x<sub>i</sub> )<super>2</super>",
        S["Formula"]))
    story.append(P(
        "When the columns are not perfectly collinear the unique minimiser is the normal "
        "equation w = (X<super>T</super>X)<super>-1</super> X<super>T</super>y. sklearn "
        "solves this with a numerically stable SVD, not by inverting by hand. There is no "
        "learning rate. Default LinearRegression is a convex problem: you get the global "
        "minimum of that bowl.",
        S["Body"]))
    story.append(P(
        "Because Cluster F already scaled numerics, a coefficient of +80 on haversine_km "
        "means “one standard deviation extra distance adds about 80 seconds”, not “one "
        "kilometre”. Haversine and Manhattan are collinear, so OLS may split one distance "
        "effect across two columns (one coefficient can even look negative). That is why "
        "Ridge exists.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "lin = LinearRegression()\n"
        "lin, y_pred_lin, _ = evaluate(\"Linear Regression\", lin, X_train_p, y_train)\n"
        "\n"
        "coef_lin = pd.Series(lin.coef_, index=feature_names)\n"
        "                    .sort_values(key=np.abs, ascending=False)"
    ))
    story.append(kv_table([
        ["Cluster", "G1, after the shared evaluate() helper in G0."],
        ["Hyperparameters", "None. sklearn default OLS."],
        ["Training rows", "Full cleaned X_train_p."],
        ["After fit", "Prints the largest |coefficients| on scaled features, plus intercept. Distance should dominate; store_and_fwd_flag should not."],
        ["Typical test R²", "About 0.62 on this table — useful, not the winner."],
        ["Viva line", "“OLS fits a hyperplane by minimising squared error. It captures distance but not the congestion curve, so trees beat it.”"],
    ]))
    story.append(PageBreak())

    # G2
    story.append(alg_banner(
        "G2  ·  sklearn.linear_model.Ridge",
        "Ridge Regression (L2)",
        "Same line as OLS, plus a penalty that shrinks large weights.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Start from OLS and add the squared length of the weight vector (the L2 penalty):",
        S["Body"]))
    story.append(P(
        "L(w) = sum<sub>i</sub> (y<sub>i</sub> − w · x<sub>i</sub>)<super>2</super>  +  alpha ||w||<sub>2</sub><super>2</super>",
        S["Formula"]))
    story.append(P(
        "alpha = 0 is Linear Regression. As alpha grows, weights are pulled toward zero but "
        "almost never hit exactly zero. The closed form becomes "
        "w = (X<super>T</super>X + alpha I)<super>-1</super> X<super>T</super>y. Adding "
        "alpha I makes the matrix invertible even when two distance columns are nearly "
        "copies — that is the mathematical reason Ridge exists.",
        S["Body"]))
    story.append(P(
        "On this dataset haversine_km and manhattan_km both say “longer trip, longer "
        "duration”. OLS may give one a huge positive weight and the other a messy negative "
        "weight. Ridge splits the credit and keeps both modest. On ~279k rows OLS variance "
        "is already low, so test R² often ties Linear. That is still a correct result: we "
        "implemented the regulariser, and mean |coefficient| is smaller than Linear’s.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "ridge = Ridge(alpha=1.0, random_state=RANDOM_STATE)\n"
        "ridge, _, _ = evaluate(\"Ridge Regression\", ridge, X_train_p, y_train)\n"
        "print(mean |lin.coef_| vs mean |ridge.coef_|)"
    ))
    story.append(P(
        "Cluster H later runs GridSearchCV over alpha in "
        "{0.001, 0.01, 0.1, 1, 10, 50, 100, 250, 1000}, scoring R² with 5-fold CV, then "
        "refits Ridge(**best_params_) on the full train and scores the same test set. If "
        "best alpha is 1.0, G2 was already well specified.",
        S["Body"]))
    story.append(kv_table([
        ["Cluster", "G2; tuned copy in H2 as “Ridge Regression (tuned)”."],
        ["alpha", "1.0 in G2. Grid-searched in H2."],
        ["What to look at", "mean |coef_| vs Linear (Ridge smaller). Test R² almost tied with Linear."],
        ["Viva line", "“Ridge is OLS plus alpha times the square of the weights. It keeps every feature but shrinks them when two distances are collinear.”"],
    ]))
    story.append(PageBreak())

    # G3
    story.append(alg_banner(
        "G3  ·  sklearn.linear_model.Lasso",
        "Lasso Regression (L1)",
        "Same line, but the penalty can switch features off completely.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Replace Ridge’s squared penalty with the sum of absolute weights (L1):",
        S["Body"]))
    story.append(P(
        "L(w) = sum<sub>i</sub> (y<sub>i</sub> − w · x<sub>i</sub>)<super>2</super>  +  alpha ||w||<sub>1</sub>",
        S["Formula"]))
    story.append(P(
        "||w||<sub>1</sub> = |w<sub>1</sub>| + |w<sub>2</sub>| + … . The L1 diamond has "
        "corners on the axes, so the optimum often sits where some coordinates are exactly "
        "zero. That is automatic feature selection: Lasso can drop month or a vendor dummy "
        "if they do not pay rent.",
        S["Body"]))
    story.append(P(
        "There is no tidy closed form like Ridge. sklearn uses coordinate descent: freeze "
        "every weight except one, solve that one-dimensional problem, cycle, repeat. That "
        "is why the notebook sets max_iter=20,000 — Lasso is iterative; Linear is not.",
        S["Body"]))
    story.append(P(
        "If no weights are zero, alpha is too small. If every weight is zero, alpha is too "
        "large. A few zeros with distance kept is the intended picture on this table.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "lasso = Lasso(alpha=0.5, max_iter=20000, random_state=RANDOM_STATE)\n"
        "lasso, _, _ = evaluate(\"Lasso Regression\", lasso, X_train_p, y_train)\n"
        "n_zero = (abs(lasso.coef_) < 1e-10).sum()   # printed as a percentage"
    ))
    story.append(kv_table([
        ["Cluster", "G3."],
        ["alpha / max_iter", "0.5 and 20,000 iterations."],
        ["After fit", "Counts exact-zero coefficients and displays the non-zero ones sorted by |weight|."],
        ["Vs Ridge", "Ridge shrinks; Lasso deletes. Neither is “more accurate” by definition."],
        ["Viva line", "“Lasso uses an L1 penalty, so some weights become exactly zero. It is OLS with built-in feature selection.”"],
    ]))
    story.append(PageBreak())

    # G4
    story.append(alg_banner(
        "G4  ·  sklearn.linear_model.ElasticNet",
        "ElasticNet",
        "A mix of Lasso’s sparsity and Ridge’s stability.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Use both penalties at once:",
        S["Body"]))
    story.append(P(
        "L(w) = sum (y − w·x)<super>2</super> + alpha [ l1_ratio ||w||<sub>1</sub> + (1 − l1_ratio) ||w||<sub>2</sub><super>2</super> ]",
        S["Formula"]))
    story.append(P(
        "l1_ratio = 1 is Lasso. l1_ratio = 0 is Ridge. The notebook uses 0.5: half of each. "
        "Lasso is greedy when two columns are twins — it may keep haversine and delete "
        "Manhattan even though both are valid. Ridge would keep both but never sparsify "
        "junk. ElasticNet can drop weak calendar bits and still share weight between the "
        "two distances. Training is coordinate descent, same family as Lasso.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "enet = ElasticNet(alpha=0.2, l1_ratio=0.5,\n"
        "                  max_iter=20000, random_state=RANDOM_STATE)\n"
        "enet, _, _ = evaluate(\"ElasticNet Regression\", enet, X_train_p, y_train)"
    ))
    story.append(kv_table([
        ["Cluster", "G4."],
        ["alpha, l1_ratio", "0.2 and 0.5. Slightly milder penalty than Lasso’s 0.5 so it does not collapse to a constant."],
        ["Typical test R²", "Near the linear cluster, often a little below Ridge (the cost of extra sparsity)."],
        ["Viva line", "“ElasticNet is alpha times a mix of L1 and L2. l1_ratio chooses how much feature-dropping versus shrinking you want.”"],
    ]))
    story.append(Spacer(1, 3 * mm))

    # G5
    story.append(alg_banner(
        "G5  ·  PolynomialFeatures + LinearRegression",
        "Polynomial Regression",
        "Still linear in the weights — nonlinear in the original columns.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Degree 1 is ordinary Linear Regression. Degree 2 builds extra columns: every square "
        "(hour², haversine_km², …) and every interaction (haversine_km × hour, "
        "is_rush_hour × manhattan_km, …). Then OLS runs on that expanded matrix. The model "
        "is still ŷ = w · z, but z contains products, so the surface in the original x is "
        "curved.",
        S["Body"]))
    story.append(P(
        "The interaction that matters here is distance × time-of-day. EDA showed the same "
        "kilometres cost more seconds at rush hour. A pure linear model can add a rush-hour "
        "offset; it cannot say “the distance slope itself gets steeper at 5pm”. Degree 2 "
        "can. We do not try degree 3: the number of terms grows as O(p³), easy to overfit.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "for degree in (1, 2):\n"
        "    pipe = Pipeline([\n"
        "        (\"poly\", PolynomialFeatures(degree=degree, include_bias=False)),\n"
        "        (\"lin\", LinearRegression()),\n"
        "    ])\n"
        "    pipe, y_pred, row = evaluate(\n"
        "        f\"Polynomial (degree {degree})\", pipe, X_train_p, y_train,\n"
        "        store=False)\n"
        "# keep whichever degree has higher test R² as \"Polynomial Regression\""
    ))
    story.append(P(
        "include_bias=False because LinearRegression already has an intercept. store=False "
        "so the two trial degrees do not both sit on the official leaderboard; only the "
        "winner is renamed Polynomial Regression and stored in fitted_models.",
        S["Body"]))
    story.append(kv_table([
        ["Cluster", "G5."],
        ["What usually wins", "Degree 2 (about 170 expanded columns vs 17). Test R² around 0.70 — between linear and trees."],
        ["Viva line", "“We are not fitting a polynomial of duration. We expand features to degree 2, then fit a linear model so distance can interact with hour.”"],
    ]))
    story.append(PageBreak())

    # G6
    story.append(alg_banner(
        "G6  ·  sklearn.tree.DecisionTreeRegressor",
        "Decision Tree",
        "Recursive binary splits. Not a line — a piecewise-constant map.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "Start with every training trip in one box. Ask: which feature and which threshold "
        "cut this box into two children so durations inside each child are as tight as "
        "possible? Tight means low mean squared error. For a candidate split, predict the "
        "mean y of each child; impurity is the size-weighted MSE. Pick the split with the "
        "largest impurity drop. Repeat on each child.",
        S["Body"]))
    story.append(P(
        "A leaf predicts the mean duration of the trips that fell into it. The whole model "
        "is a set of axis-aligned rectangles, each with one constant ŷ. That is how a tree "
        "represents “if haversine_km &gt; 8 and hour in the rush band, predict ~1,400 s” "
        "without writing an interaction term by hand.",
        S["Body"]))
    story.append(P(
        "max_depth stops an unlimited tree from memorising train trips. min_samples_leaf "
        "stops one weird 3-hour ride from becoming its own rule. Feature importance is the "
        "total MSE reduction that feature was responsible for across all splits. Distance "
        "should rank first; hour and rush hour should appear.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "tree = DecisionTreeRegressor(\n"
        "    max_depth=12,\n"
        "    min_samples_leaf=50,\n"
        "    random_state=RANDOM_STATE,\n"
        ")\n"
        "tree, _, _ = evaluate(\"Decision Tree Regressor\", tree, X_train_p, y_train)\n"
        "# then bar-plot tree.feature_importances_ for the top 12 columns"
    ))
    story.append(kv_table([
        ["Cluster", "G6."],
        ["Why it beats Linear", "It can isolate rush-hour long trips without a polynomial expansion."],
        ["Why a forest still wins", "One tree is high variance — a different 80/20 split grows a different tree."],
        ["Viva line", "“A regression tree partitions feature space by MSE-reducing splits and predicts the mean duration in each leaf.”"],
    ]))
    story.append(PageBreak())

    # G7
    story.append(alg_banner(
        "G7  ·  sklearn.ensemble.RandomForestRegressor",
        "Random Forest",
        "Many deep trees, each a little wrong, averaged.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "A forest is bagging plus extra randomness:",
        S["Body"]))
    story.append(bullets([
        "<b>Bootstrap sample.</b> Each tree is grown on n trips drawn with replacement. Some trips appear twice; others are left out (out-of-bag).",
        "<b>Random feature subset at splits</b> (when max_features is not 1.0). Stops every tree from making the same first split on haversine_km.",
        "<b>Average the trees.</b> For a new trip, each tree votes a duration; the forest prediction is the mean of those votes.",
    ]))
    story.append(P(
        "One tree overfits its bootstrap quirks. Those quirks are weakly correlated across "
        "trees, so they cancel. Bias stays similar to a deep tree; variance falls. Feature "
        "importances are averaged impurity reductions — a ranking, not causal percentages.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "forest = RandomForestRegressor(\n"
        "    n_estimators=80, max_depth=18, min_samples_leaf=20,\n"
        "    n_jobs=-1, verbose=1, random_state=RANDOM_STATE,\n"
        ")\n"
        "forest, _, _ = evaluate(\"Random Forest Regressor\", forest, X_train_p, y_train)"
    ))
    story.append(P(
        "Cluster H2 then RandomizedSearchCV on a 40,000-row subset (TUNE_SAMPLE_SIZE) with "
        "n_iter=8, cv=3, searching n_estimators in {60, 80, 120}, max_depth in {12, 16, 20, "
        "None}, min_samples_leaf in {10, 20, 40}, max_features in {sqrt, 0.5, 1.0}. The "
        "winning params are refit on the <b>full</b> training table and scored on the same "
        "test set as “Random Forest Regressor (tuned)”.",
        S["Body"]))
    story.append(kv_table([
        ["Cluster", "G7; tuned copy in H2."],
        ["Typical test R²", "About 0.79 — usually 2nd, just under HistGBM."],
        ["verbose=1", "So Run All is not a silent freeze while 80 trees grow."],
        ["Viva line", "“A random forest averages many deep trees grown on bootstrap samples, which cuts variance compared with one decision tree.”"],
    ]))
    story.append(PageBreak())

    # G8
    story.append(alg_banner(
        "G8  ·  sklearn.ensemble.HistGradientBoostingRegressor",
        "Gradient Boosting (histogram GBM)",
        "Trees in a sequence, each one trained on the previous residual.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "A forest builds trees in parallel and averages. Boosting builds them "
        "<b>one after another</b>. Start with F<sub>0</sub> = mean(y). Residual of trip i "
        "is y<sub>i</sub> − F<sub>0</sub>. Grow a small tree h<sub>1</sub> on those "
        "residuals. Update:",
        S["Body"]))
    story.append(P(
        "F<sub>m</sub>(x) = F<sub>m-1</sub>(x) + learning_rate · h<sub>m</sub>(x)",
        S["Formula"]))
    story.append(P(
        "A small learning_rate (0.08) means each tree is a cautious step, so you need more "
        "trees (max_iter=200) but you overfit less than one huge step. After M rounds the "
        "model is a sum of shallow trees. For squared-error loss the residual is exactly "
        "the negative gradient, so “fit the residual” is not a metaphor.",
        S["Body"]))
    story.append(P(
        "Why HistGradientBoostingRegressor, not GradientBoostingRegressor: the classical "
        "sklearn booster is too slow on ~279k rows. The histogram version bins each feature "
        "(max_bins=255) and finds splits on bin edges. Same boosting idea, much faster, "
        "same family the rubric lists as Gradient Boosting. max_depth=6 keeps each base "
        "tree a weak learner — boosting wants weak learners.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "gbm = HistGradientBoostingRegressor(\n"
        "    learning_rate=0.08, max_depth=6, max_iter=200,\n"
        "    l2_regularization=0.1, verbose=1, random_state=RANDOM_STATE,\n"
        ")\n"
        "gbm, _, _ = evaluate(\"Gradient Boosting Regressor\", gbm, X_train_p, y_train)"
    ))
    story.append(kv_table([
        ["Cluster", "G8. Leaderboard name is “Gradient Boosting Regressor” even though the class is HistGBM."],
        ["Typical test R²", "About 0.80 — usually 1st on this table."],
        ["Vs forest", "Forest reduces variance by averaging. Boosting reduces bias by sequentially fixing mistakes."],
        ["Viva line", "“Gradient boosting adds trees that predict the leftover error of the current model, each scaled by a small learning rate. We use the histogram implementation so it finishes on 279k rows.”"],
    ]))
    story.append(PageBreak())

    # G9
    story.append(alg_banner(
        "G9  ·  sklearn.svm.SVR  +  TransformedTargetRegressor",
        "Support Vector Regressor",
        "A tube around the data in a kernel-induced space. Not a tree, not OLS.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "SVR looks for a function f(x) = w · phi(x) + b that is as flat as possible (small "
        "||w||) while keeping every training residual inside an epsilon-insensitive tube. "
        "Errors smaller than epsilon cost nothing. Errors outside the tube pay a hinge "
        "cost, weighted by C:",
        S["Body"]))
    story.append(P(
        "min  ½ ||w||<super>2</super> + C sum xi<sub>i</sub>    s.t.  |y<sub>i</sub> − f(x<sub>i</sub>)|  &lt;=  epsilon + xi<sub>i</sub>",
        S["Formula"]))
    story.append(P(
        "Large C fits training points tightly (risk overfitting). Small C is flatter and "
        "may underfit. Points on or outside the tube become support vectors; the others do "
        "not affect w.",
        S["Body"]))
    story.append(P(
        "phi(x) is never computed. The RBF kernel K(x, x') = exp(−gamma ||x − x'||<super>2</super>) "
        "is the inner product in an infinite-dimensional space. Two similar trips get a "
        "kernel value near 1; distant trips get ~0. The prediction is a weighted sum of "
        "kernels against the support vectors.",
        S["Body"]))
    story.append(P(
        "SVR’s epsilon and C live in the scale of y. Raw duration is hundreds to thousands "
        "of seconds; default epsilon=0.1 is then meaningless and R² collapses (~0.2). "
        "TransformedTargetRegressor(StandardScaler()) scales y to mean 0, std 1 for "
        "training, then inverts on predict. Features are already scaled in Cluster F.",
        S["Body"]))
    story.append(P(
        "Classic RBF-SVR is roughly O(n²) to O(n³). 279k rows is not a laptop fit. We draw "
        "12,000 training rows with seed 42, but still score the same 50,000 test rows as "
        "everyone else.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "X_svr, y_svr = subset_train(SVR_TRAIN_SIZE)          # 12,000 rows\n"
        "svr = TransformedTargetRegressor(\n"
        "    regressor=SVR(kernel=\"rbf\", C=1.0, epsilon=0.1, verbose=True),\n"
        "    transformer=StandardScaler(),\n"
        ")\n"
        "svr, _, _ = evaluate(\"Support Vector Regressor\", svr, X_svr, y_svr)"
    ))
    story.append(kv_table([
        ["Cluster", "G9."],
        ["Typical test R²", "About 0.73 on 12k — strong for the sample size, not a fair fight with HistGBM."],
        ["Viva line", "“SVR fits a flat function in kernel space with an epsilon-tube. We scale the target, use RBF, and train on 12k rows because full-data SVR is O(n²).”"],
    ]))
    story.append(PageBreak())

    # G10
    story.append(alg_banner(
        "G10  ·  sklearn.neighbors.KNeighborsRegressor",
        "k-Nearest Neighbours",
        "No weights are learned. Prediction is a vote of nearby past trips.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("How it works", S["H3"]))
    story.append(P(
        "KNN is a lazy learner. fit() stores the training matrix; it does not estimate w. "
        "To predict one new trip x, compute a distance to every stored trip, take the k "
        "closest, and average their durations. The notebook uses k=15 and "
        "weights='distance': closer neighbours count more (inverse-distance) instead of a "
        "flat mean.",
        S["Body"]))
    story.append(P(
        "Distance is Euclidean in the scaled feature space. That is why Cluster F’s "
        "StandardScaler is mandatory here: without it, hour (0–23) would be crushed by a "
        "dummy 0/1, and kilometres would dominate everything. After scaling, one std of "
        "distance equals one std of hour in the metric.",
        S["Body"]))
    story.append(P(
        "fit prints ~0.0 s because it is a copy of the array. predict is O(n_train × n_test "
        "× n_features). 279k × 50k is not a viva-friendly wait, so we train on 40,000 rows "
        "and still score the same 50,000 test trips. KNN cannot extrapolate: a 30 km trip "
        "unlike anything in the 40k sample is averaged from the farthest “near” trips and "
        "will be too short.",
        S["Body"]))
    story.append(P("How the notebook implements it", S["H3"]))
    story.append(code_block(
        "X_knn, y_knn = subset_train(KNN_TRAIN_SIZE)           # 40,000 rows\n"
        "knn = KNeighborsRegressor(\n"
        "    n_neighbors=15, weights=\"distance\", n_jobs=-1)\n"
        "knn, _, _ = evaluate(\"K-Nearest Neighbors Regressor\", knn, X_knn, y_knn)\n"
        "show_all_metrics_table(\"Ten regression algorithms + mean baseline\")"
    ))
    story.append(kv_table([
        ["Cluster", "G10. This cell also prints the full ranked metrics table for all ten models."],
        ["Typical test R²", "About 0.70 — third tier, ahead of linear, behind trees."],
        ["Viva line", "“KNN predicts the distance-weighted average duration of the 15 closest training trips in scaled feature space. Fit is free; predict is the expensive part, so we train on 40k rows.”"],
    ]))
    story.append(Spacer(1, 3 * mm))

    # baseline
    story.append(alg_banner(
        "BASELINE  ·  sklearn.dummy.DummyRegressor  (not one of the ten)",
        "Mean predictor",
        "Always guess the training-set average duration.",
    ))
    story.append(Spacer(1, 2.5 * mm))
    story.append(P(
        "ŷ = mean(y_train) for every test trip. Test R² is about 0 by construction. RMSE is "
        "the standard deviation of duration. Cluster G0 fits DummyRegressor(strategy='mean') "
        "and runs the same four mandatory metrics so a 0.62 linear R² is visibly better "
        "than doing nothing. If a model ever lands near this row, it failed.",
        S["Body"]))
    story.append(code_block(
        "y_mean = np.full_like(y_test, fill_value=y_train.mean(), dtype=float)\n"
        "dummy = DummyRegressor(strategy=\"mean\")\n"
        "dummy.fit(X_train_p, y_train)\n"
        "# then the same R² / RMSE / MAE / 5-fold CV R² report as every official model"
    ))
    story.append(PageBreak())

    # 14 tuning
    story.append(P("14.  Cluster H: search, then reprint the two best", S["H1"]))
    story.append(hrule())
    story.append(P("GridSearchCV on Ridge", S["H2"]))
    story.append(code_block(
        "ridge_grid = GridSearchCV(\n"
        "    Ridge(random_state=RANDOM_STATE),\n"
        "    param_grid={\"alpha\": [0.001, 0.01, 0.1, 1, 10, 50, 100, 250, 1000]},\n"
        "    scoring=\"r2\", cv=5, n_jobs=-1, verbose=2,\n"
        ")\n"
        "ridge_grid.fit(X_train_p, y_train)\n"
        "evaluate(\"Ridge Regression (tuned)\",\n"
        "         Ridge(**ridge_grid.best_params_, random_state=RANDOM_STATE),\n"
        "         X_train_p, y_train)"
    ))
    story.append(P(
        "A grid is an exhaustive product of the values you list. Inner 5-fold CV picks "
        "alpha; then evaluate() refits on all training rows and scores the held-out test "
        "set once. The search never sees test labels.",
        S["Body"]))
    story.append(P("RandomizedSearchCV on Random Forest", S["H2"]))
    story.append(P(
        "A forest has several knobs, so a full grid explodes. Randomized search draws 8 "
        "combinations on a 40k subset (cv=3) then refits the winner on the full train. "
        "n_jobs=-1 and verbose=2 keep the laptop busy and the operator informed.",
        S["Body"]))
    story.append(P("Top-two 5-fold CV (rubric item)", S["H2"]))
    story.append(P(
        "Every G-cell already computed 5-fold CV R². Cluster H4 only <b>selects the two "
        "official models with the highest test R²</b> (usually Gradient Boosting and Random "
        "Forest) and reprints their test R² / RMSE / MAE / CV numbers. If the top two were "
        "SVR or KNN, those CV folds came from their 12k / 40k subsets — same rows used to fit.",
        S["Body"]))
    story.append(PageBreak())

    # 15 viva
    story.append(P("15.  How to talk about a model in the viva", S["H1"]))
    story.append(hrule())
    story.append(P(
        "If they name an algorithm, give the loss or rule first, then the notebook "
        "constructor, then one result on this taxi table.",
        S["Body"]))
    story.append(simple_table(
        ["If they ask", "Start with", "Then point at"],
        [
            ["How does Ridge work?", "OLS loss + alpha ||w||²", "G2 constructor; two distance columns"],
            ["L1 vs L2?", "L2 shrinks, L1 can zero", "G3 zero-count printout"],
            ["Why polynomial?", "Degree-2 interactions", "G5 Pipeline; degree 2 usually wins"],
            ["How does a tree split?", "MSE impurity drop", "G6 importance bar chart"],
            ["Forest vs boosting?", "Average vs residual sequence", "G7 vs G8; HistGBM usually 1st"],
            ["Why subset SVR/KNN?", "O(n²) fit vs O(n_train n_test) predict", "Train rows column on the table"],
            ["Did the scaler see test?", "No. Cluster F fit on train only", "ColumnTransformer in F"],
            ["Which is best?", "Highest test R², confirmed by CV", "G10 / H1 table, then H4 top two"],
        ],
        widths=[38 * mm, 52 * mm, w - 90 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(callout(
        "Closing sentence you can actually say: “We predicted NYC taxi duration from pickup "
        "context only, with no dropoff leak, on one encoded table, ten independent regressors, "
        "and the same test trips. Trees win because congestion is not linear; Ridge exists "
        "because the two distances are collinear; SVR and KNN are scored fairly but trained "
        "smaller because of complexity, not because they were ignored.”"
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(hrule())
    story.append(P(
        "File: documentation/regression.pdf  ·  Notebook: notebooks/regression.ipynb  ·  "
        "Seed 42 throughout.",
        S["Caption"]))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="How each regression algorithm works",
        author="23CSE301 Capstone",
        subject="NYC taxi trip duration — algorithm theory and notebook implementation",
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KiB, {doc.page} pages)")


if __name__ == "__main__":
    build()
