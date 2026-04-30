"""Generate a friendly PDF user-guide for the personal website."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable,
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from pathlib import Path

# ---------- palette (matches the website) ----------
CREAM       = HexColor("#FAF6EF")
CREAM_WARM  = HexColor("#F5EFE3")
INK         = HexColor("#2D2823")
INK_SOFT    = HexColor("#6B5E54")
INK_MUTED   = HexColor("#9C8E84")
CORAL       = HexColor("#E89B7E")
PINK_SOFT   = HexColor("#FBE3E5")
SAGE_SOFT   = HexColor("#DDE6CE")
BUTTER_SOFT = HexColor("#FAEAB8")
LINE        = HexColor("#E8DFD2")

# ---------- styles ----------
styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold", fontSize=26, leading=30,
    textColor=INK, spaceAfter=6, spaceBefore=0)

H2 = ParagraphStyle("H2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=15, leading=20,
    textColor=CORAL, spaceBefore=18, spaceAfter=6)

H3 = ParagraphStyle("H3",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=INK, spaceBefore=10, spaceAfter=2)

BODY = ParagraphStyle("Body",
    parent=styles["BodyText"],
    fontName="Helvetica", fontSize=10.5, leading=15.5,
    textColor=INK, spaceAfter=6, alignment=TA_LEFT)

LEAD = ParagraphStyle("Lead",
    parent=BODY,
    fontName="Helvetica-Oblique", fontSize=11, leading=17,
    textColor=INK_SOFT, spaceAfter=12)

SMALL = ParagraphStyle("Small",
    parent=BODY,
    fontSize=9, leading=13, textColor=INK_MUTED)

CODE = ParagraphStyle("Code",
    parent=styles["Code"],
    fontName="Courier", fontSize=9.2, leading=13,
    textColor=INK, leftIndent=10, rightIndent=10,
    spaceBefore=4, spaceAfter=4,
    backColor=CREAM_WARM, borderPadding=(8, 8, 8, 8))

LABEL = ParagraphStyle("Label",
    parent=BODY,
    fontName="Helvetica-Bold", fontSize=8.5, leading=11,
    textColor=CORAL, spaceAfter=4,
    alignment=TA_LEFT)


def code_block(text: str):
    """Wrap a multi-line code block in a soft cream rectangle."""
    safe = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>"))
    para = Paragraph(safe, CODE)
    tbl = Table([[para]], colWidths=[16 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM_WARM),
        ("BOX",        (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    return tbl


def callout(title: str, body_html: str, color=PINK_SOFT):
    p = Paragraph(
        f"<font name='Helvetica-Bold' color='#2D2823'>{title}</font>"
        f"<br/><font size='10'>{body_html}</font>",
        BODY,
    )
    tbl = Table([[p]], colWidths=[16 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX",        (0, 0), (-1, -1), 0, color),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ]))
    return tbl


def soft_divider():
    return HRFlowable(width="100%", thickness=0.7, color=LINE,
                      spaceBefore=10, spaceAfter=10)


# ---------- page decorations ----------
def on_page(canv: canvas.Canvas, doc):
    """Draw a tiny decorative element on every page."""
    canv.saveState()
    # cream tint at the top
    canv.setFillColor(CREAM)
    canv.rect(0, A4[1] - 1.2 * cm, A4[0], 1.2 * cm, stroke=0, fill=1)
    # tiny coral dot
    canv.setFillColor(CORAL)
    canv.circle(2 * cm, A4[1] - 0.6 * cm, 3, stroke=0, fill=1)
    # page number bottom right
    canv.setFont("Helvetica", 8)
    canv.setFillColor(INK_MUTED)
    canv.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"page {doc.page}")
    # tiny "behnaz" footer left
    canv.setFont("Helvetica-Oblique", 8)
    canv.drawString(2 * cm, 1.2 * cm, "behnaz · website guide")
    canv.restoreState()


# ---------- content ----------
def build():
    out_path = Path(r"C:/Users/goshayeshi.LAP-MIT-BG/Desktop/cava/website-guide.pdf")
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Your website — a small guide",
        author="behnaz",
    )

    flow = []

    # ===== Cover =====
    flow.append(Spacer(1, 1.5 * cm))
    flow.append(Paragraph("your website ✿", H1))
    flow.append(Paragraph("a small, friendly guide to using and updating it.", LEAD))
    flow.append(Spacer(1, 0.4 * cm))

    flow.append(callout(
        "your site is live at:",
        "<font name='Helvetica-Bold' color='#E89B7E' size='12'>"
        "https://behnaz-website-chi.vercel.app/</font><br/>"
        "<font color='#6B5E54' size='9'>"
        "every time you push code from your computer, vercel rebuilds and "
        "redeploys this URL automatically.</font>",
        color=BUTTER_SOFT,
    ))

    flow.append(Spacer(1, 0.6 * cm))
    flow.append(Paragraph("what this guide covers", H3))
    flow.append(Paragraph(
        "1. how the site was built (in plain words)<br/>"
        "2. where things live on your computer<br/>"
        "3. how to add a recipe, thought, or project<br/>"
        "4. how to preview before publishing<br/>"
        "5. how to change colors, the about page, the gallery<br/>"
        "6. a tiny markdown cheat sheet<br/>"
        "7. the handful of terminal commands you actually need<br/>"
        "8. what to do when something breaks", BODY))
    flow.append(PageBreak())

    # ===== How it works =====
    flow.append(Paragraph("how it works (simply)", H2))
    flow.append(Paragraph(
        "your website is a small machine with three pieces:", BODY))

    flow.append(Spacer(1, 0.2 * cm))

    pieces = [
        ("astro", "a tool that takes your content (markdown files) and a layout, "
                  "and turns them into plain HTML pages. nothing fancy on the "
                  "server — every page is pre-built and just sits there waiting "
                  "to be opened."),
        ("github", "a place online where your code is stored. think of it as "
                   "google drive, but for code, with a built-in time machine "
                   "(every change is saved with a label)."),
        ("vercel", "a free hosting service. it watches your github repository — "
                   "every time you push a change, vercel rebuilds the site and "
                   "puts the new version online in about 30 seconds."),
    ]
    for name, desc in pieces:
        flow.append(Paragraph(
            f"<font name='Helvetica-Bold' color='#E89B7E'>· {name}</font> &nbsp; {desc}",
            BODY))
        flow.append(Spacer(1, 0.15 * cm))

    flow.append(Spacer(1, 0.3 * cm))
    flow.append(Paragraph("the loop", H3))
    flow.append(Paragraph(
        "1. you write or edit a file on your computer<br/>"
        "2. you run three small git commands to save and upload<br/>"
        "3. vercel sees the upload, rebuilds, redeploys<br/>"
        "4. ~30 seconds later, your website shows the change", BODY))
    flow.append(Spacer(1, 0.2 * cm))
    flow.append(callout(
        "you don't need to know HTML or CSS to add content.",
        "<font color='#2D2823'>you only edit small markdown files. they look "
        "like a cleaner version of writing in word — `# heading`, `**bold**`, "
        "`*italic*`, that's most of it.</font>",
        color=SAGE_SOFT,
    ))

    flow.append(PageBreak())

    # ===== Where things live =====
    flow.append(Paragraph("where things live", H2))
    flow.append(Paragraph(
        "your project folder on your computer is here:", BODY))
    flow.append(code_block("C:\\Users\\goshayeshi.LAP-MIT-BG\\Desktop\\cava\\website"))

    flow.append(Spacer(1, 0.2 * cm))
    flow.append(Paragraph("inside, the folders that matter:", BODY))

    table_data = [
        ["folder", "what it holds"],
        ["src/content/posts/",   "every blog post — recipes, thoughts, notes (.md files)"],
        ["src/content/projects/", "every project card on the projects page (.md files)"],
        ["src/pages/",            "the main pages: home, about, cv, gallery, etc."],
        ["src/styles/global.css", "all the colors, fonts, and design tokens"],
        ["public/",               "static files: favicon, your CV pdf, etc."],
        ["public/gallery/",       "images shown in the gallery"],
    ]
    t = Table(table_data, colWidths=[5.2 * cm, 10.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), CORAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0), white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9.5),
        ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("FONTNAME",      (0, 1), (0, -1), "Courier"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, CREAM_WARM]),
        ("LINEBELOW",     (0, 0), (-1, 0), 0.5, CORAL),
        ("BOX",           (0, 0), (-1, -1), 0.5, LINE),
    ]))
    flow.append(t)

    flow.append(PageBreak())

    # ===== Add a post =====
    flow.append(Paragraph("how to add a recipe / thought / note", H2))
    flow.append(Paragraph(
        "every post on your site is a single markdown file. one file = "
        "one post. the URL of the post is just the filename.", BODY))

    flow.append(Paragraph("step 1 — make a new file", H3))
    flow.append(Paragraph(
        "create a new file in <b>src/content/posts/</b>. name it after the "
        "topic, all lowercase, words joined with dashes. for example: "
        "<font name='Courier'>lemon-cake.md</font> becomes the URL "
        "<font name='Courier'>/writing/lemon-cake</font>.", BODY))

    flow.append(Paragraph("step 2 — start with this template", H3))
    flow.append(code_block(
        "---\n"
        "title: lemon cake\n"
        "description: a sticky, very lemony cake\n"
        "date: 2026-05-15\n"
        "emoji: 🍋\n"
        "tags: [recipe]\n"
        "---\n\n"
        "your text here, in markdown.\n\n"
        "## ingredients\n"
        "- 200g flour\n"
        "- 3 eggs\n"
        "- a lot of lemon zest\n\n"
        "## method\n"
        "1. mix everything\n"
        "2. bake until golden\n"
    ))

    flow.append(Paragraph("step 3 — pick a tag", H3))
    flow.append(Paragraph(
        "the <b>tags</b> field controls the colored chip that appears on the "
        "post. valid tags are:", BODY))
    flow.append(Paragraph(
        "<font name='Courier' color='#E89B7E'>recipe</font>, "
        "<font name='Courier' color='#E89B7E'>thought</font>, "
        "<font name='Courier' color='#E89B7E'>project</font>, "
        "<font name='Courier' color='#E89B7E'>art</font>, "
        "<font name='Courier' color='#E89B7E'>code</font>. "
        "you can use more than one: <font name='Courier'>tags: [recipe, thought]</font>.",
        BODY))

    flow.append(Paragraph("step 4 — preview locally (optional but recommended)", H3))
    flow.append(Paragraph("open a terminal in the website folder and run:", BODY))
    flow.append(code_block("npm run dev"))
    flow.append(Paragraph(
        "open <font name='Courier'>http://localhost:4321</font> in your "
        "browser. you'll see your new post immediately. when you save the "
        "file, the page auto-refreshes. press <b>Ctrl+C</b> in the terminal "
        "to stop the preview.", BODY))

    flow.append(Paragraph("step 5 — publish (3 commands)", H3))
    flow.append(code_block(
        "git add .\n"
        "git commit -m \"add lemon cake recipe\"\n"
        "git push"
    ))
    flow.append(Paragraph(
        "wait ~30 seconds. refresh your live website. the post is there.", BODY))

    flow.append(PageBreak())

    # ===== Other common tasks =====
    flow.append(Paragraph("other things you might want to do", H2))

    flow.append(Paragraph("change a color on the whole site", H3))
    flow.append(Paragraph(
        "open <font name='Courier'>src/styles/global.css</font>. at the top "
        "you'll see a <font name='Courier'>@theme {{ ... }}</font> block with "
        "lines like:", BODY))
    flow.append(code_block(
        "--color-coral: #E89B7E;\n"
        "--color-pink:  #F2BFC4;\n"
        "--color-sage:  #B5C4A0;\n"
        "--color-cream: #FAF6EF;"
    ))
    flow.append(Paragraph(
        "change any hex code (e.g. coral to <font name='Courier'>#FF6B9D</font>) "
        "and save. the dev server reloads instantly. push when you like the result.", BODY))

    flow.append(Paragraph("edit the about page", H3))
    flow.append(Paragraph(
        "open <font name='Courier'>src/pages/about.astro</font>. edit the text "
        "inside the <font name='Courier'>&lt;p&gt; ... &lt;/p&gt;</font> tags. "
        "save. push.", BODY))

    flow.append(Paragraph("add a photo to the gallery", H3))
    flow.append(Paragraph(
        "(1) save your image into <font name='Courier'>public/gallery/</font>, "
        "e.g. <font name='Courier'>morning-walk.jpg</font>.<br/>"
        "(2) open <font name='Courier'>src/pages/gallery.astro</font>. find "
        "the <font name='Courier'>items</font> array near the top.<br/>"
        "(3) add a new line:", BODY))
    flow.append(code_block(
        '{ src: "/gallery/morning-walk.jpg",\n'
        '  alt: "morning walk in the wald",\n'
        '  caption: "may, the wald" },'
    ))
    flow.append(Paragraph(
        "save. push. (the alt text helps screen readers and SEO.)", BODY))

    flow.append(Paragraph("add your real CV PDF for download", H3))
    flow.append(Paragraph(
        "save your CV as <font name='Courier'>public/cv.pdf</font>. that's it — "
        "the download button on the /cv page already points there.", BODY))

    flow.append(Paragraph("add a new project card", H3))
    flow.append(Paragraph(
        "create a new file in <font name='Courier'>src/content/projects/</font>, "
        "e.g. <font name='Courier'>my-new-project.md</font>:", BODY))
    flow.append(code_block(
        "---\n"
        "title: my new project\n"
        "description: a short description of what it is.\n"
        "year: \"2026\"\n"
        "role: side project\n"
        "stack: [python, pytorch]\n"
        "link: https://github.com/behnaazz/something\n"
        "emoji: ✦\n"
        "featured: true\n"
        "---\n"
    ))

    flow.append(PageBreak())

    # ===== Markdown cheatsheet =====
    flow.append(Paragraph("a tiny markdown cheat sheet", H2))
    flow.append(Paragraph(
        "everything you'll need 95%% of the time:", BODY))

    md_table = [
        ["you write",                        "you get"],
        ["# Big heading",                    "biggest section heading"],
        ["## Smaller heading",               "second-level heading"],
        ["**bold**",                         "bold text"],
        ["*italic*",                         "italic text"],
        ["[click me](https://example.com)",  "a link"],
        ["- item",                           "bullet list"],
        ["1. item",                          "numbered list"],
        ["![cake](/photos/cake.jpg)",        "an image"],
        ["> a quoted line",                  "indented quote"],
        ["`some code`",                      "monospace inline code"],
        ["---",                              "a horizontal divider line"],
    ]
    t2 = Table(md_table, colWidths=[7.5 * cm, 8.5 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0), CORAL),
        ("TEXTCOLOR",      (0, 0), (-1, 0), white),
        ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9.5),
        ("FONTNAME",       (0, 1), (0, -1), "Courier"),
        ("ALIGN",          (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
        ("TOPPADDING",     (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, CREAM_WARM]),
        ("LINEBELOW",      (0, 0), (-1, 0), 0.5, CORAL),
        ("BOX",            (0, 0), (-1, -1), 0.5, LINE),
    ]))
    flow.append(t2)

    flow.append(Spacer(1, 0.4 * cm))
    flow.append(Paragraph("the only commands you actually need", H2))

    flow.append(Paragraph("open a terminal inside the website folder. then:", BODY))

    cmd_table = [
        ["command",              "what it does"],
        ["npm run dev",          "preview the site at localhost:4321 (live reload)"],
        ["npm run build",        "build the production version (sanity check)"],
        ["git status",           "see which files you've changed"],
        ["git add .",            "stage all your changes"],
        ['git commit -m "..."',  "save a snapshot with a label"],
        ["git push",             "send your changes to github → vercel auto-deploys"],
    ]
    t3 = Table(cmd_table, colWidths=[6.0 * cm, 10.0 * cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0), CORAL),
        ("TEXTCOLOR",      (0, 0), (-1, 0), white),
        ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9.5),
        ("FONTNAME",       (0, 1), (0, -1), "Courier"),
        ("ALIGN",          (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
        ("TOPPADDING",     (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, CREAM_WARM]),
        ("LINEBELOW",      (0, 0), (-1, 0), 0.5, CORAL),
        ("BOX",            (0, 0), (-1, -1), 0.5, LINE),
    ]))
    flow.append(t3)

    flow.append(PageBreak())

    # ===== Troubleshooting =====
    flow.append(Paragraph("when something looks broken", H2))

    troubles = [
        ("the dev server shows an error and a red wall of text",
         "read the first error message — it usually tells you the file and "
         "line number. most often: a typo in frontmatter (missing date, wrong "
         "tag, missing quotes). fix that, save, the page recovers."),
        ("the local site looks fine but vercel says 'build failed'",
         "open vercel.com, click your project, click the failed deployment, "
         "scroll the build log. the error is the same kind you'd see locally — "
         "fix it on your computer, commit, push, vercel retries automatically."),
        ("i pushed but nothing changed",
         "wait one full minute. then check vercel.com — your latest deployment "
         "should be at the top. if it says 'building', it's just slow today."),
        ("the dev server won't start",
         "you might have closed the terminal. open a new one, navigate to "
         "the website folder, run `npm run dev` again."),
        ("i broke something and want to undo",
         "if you haven't pushed yet: `git checkout .` (discards uncommitted "
         "changes). if you already pushed and want to roll back to the previous "
         "version: tell me, i'll walk you through it without you accidentally "
         "deleting good work."),
    ]
    for q, a in troubles:
        flow.append(Paragraph(f"<b>{q}</b>", BODY))
        flow.append(Paragraph(a, BODY))
        flow.append(Spacer(1, 0.2 * cm))

    flow.append(soft_divider())

    flow.append(callout(
        "small, friendly reminder",
        "<font color='#2D2823'>your website is allowed to grow slowly. "
        "you don't have to fill every page on day one. add one recipe this "
        "month, one thought next month. the site will get richer over time, "
        "and that's the whole charm of it.</font>",
        color=PINK_SOFT,
    ))

    flow.append(Spacer(1, 0.6 * cm))
    flow.append(Paragraph("made with care for behnaz · april 2026", SMALL))

    # ===== Build =====
    doc.build(flow, onFirstPage=on_page, onLaterPages=on_page)
    print(f"OK: wrote {out_path}")


if __name__ == "__main__":
    build()
