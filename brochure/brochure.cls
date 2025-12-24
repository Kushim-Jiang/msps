\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{brochure}[2025/12/23 Custom book class with outer sidenotes]

% Base class：ctexbook
\LoadClass[
    UTF8,
    12pt,
    a4paper,
    twoside,
    openany
]{ctexbook}

% Page geometry
\RequirePackage{geometry}
\geometry{
    inner=28mm,
    outer=72mm,
    top=25mm,
    bottom=30mm,
    marginparsep=8mm,
    marginparwidth=48mm
}

% Line spacing
\RequirePackage{setspace}
\setstretch{1.35}

% Header and footer
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}

\fancyhead[LE]{\small\leftmark}
\fancyhead[RO]{\small\rightmark}
\fancyfoot[C]{\thepage}

% Prevent fancyhdr warning
\setlength{\headheight}{14pt}

% Chinese punctuation
\RequirePackage{CJKpunct}
\punctstyle{kaiming}

% Paragraph settings
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}

% sidenote system
\RequirePackage{marginnote}
\RequirePackage{ifoddpage}
\RequirePackage{ragged2e}

\newcommand{\sidenote}[1]{%
    \checkoddpage
    \ifoddpage
        \marginnote[]{% odd page
            \footnotesize
            \setlength{\parindent}{0pt}%
            \setlength{\parskip}{0pt}%
            \justifying
            #1%
        }%
    \else
        \marginnote[% even page
            \footnotesize
            \setlength{\parindent}{0pt}%
            \setlength{\parskip}{0pt}%
            \justifying
            #1%
        ]{}%
    \fi
}

% Title style
\RequirePackage{titlesec}

\titleformat{\chapter}
{\Large\bfseries}
{\thechapter}
{1em}
{}

\titleformat{\section}
{\large\bfseries}
{\thesection}
{1em}
{}

% Page vertical alignment
\raggedbottom
