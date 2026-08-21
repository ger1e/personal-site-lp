#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
META_START='<!-- pimp-meta:start -->'; META_END='<!-- pimp-meta:end -->'; STYLE_START='/* pimp-cat-hero:start */'; STYLE_END='/* pimp-cat-hero:end */'
META=f'''{META_START}
<link rel="canonical" href="https://gergoilly.hu/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:url" content="https://gergoilly.hu/">
<meta property="og:image" content="https://gergoilly.hu/assets/social-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="GER1E — threat hunting, CTI and detection engineering">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://gergoilly.hu/assets/social-card.png">
{META_END}'''
STYLE=f'''{STYLE_START}
.cat-card{{width:min(460px,38vw);min-width:310px;aspect-ratio:4/5;right:clamp(18px,3.4vw,42px);bottom:clamp(18px,3.4vw,36px);box-shadow:0 24px 72px rgba(0,0,0,.46),0 0 56px rgba(89,255,155,.08)}}
.content{{max-width:680px}}.spotify{{width:min(490px,100%)}}
@media(max-width:1040px){{.hero-card{{padding-bottom:470px}}.cat-card{{width:min(430px,84vw);min-width:0}}}}
@media(max-width:620px){{.hero-card{{padding-bottom:430px}}.cat-card{{left:16px;right:16px;width:auto;aspect-ratio:4/5}}}}
{STYLE_END}'''
def _strip_block(text,start,end):
    if start not in text:return text
    return re.compile(r'\n?'+re.escape(start)+r'.*?'+re.escape(end)+r'\n?',re.S).sub('',text,count=1)
def transform(html):
    out=_strip_block(_strip_block(html,META_START,META_END),STYLE_START,STYLE_END)
    if '</head>' not in out or '</style>' not in out: raise ValueError('expected </style> and </head> in index.html')
    out=out.replace('</style>','\n'+STYLE+'\n</style>',1)
    out=out.replace('</head>','\n'+META+'\n</head>',1)
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--path',default='index.html');p.add_argument('--write',action='store_true');a=p.parse_args();path=Path(a.path);updated=transform(path.read_text(encoding='utf-8'))
    if a.write:path.write_text(updated,encoding='utf-8')
    else:print(updated)
    return 0
if __name__=='__main__':raise SystemExit(main())
