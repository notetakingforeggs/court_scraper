import pytest
from bs4 import BeautifulSoup as bs
from scraper.parsers.daily_cause_list_parser import DailyCauseListParser
class DummySession:
        def get(self, url):
                return None
        

def create_parser_with_html(html):
    parser = DailyCauseListParser(html)
    return parser


def test_extract_city_normal():
    html = '''
    <html>
    <head>
    <title>CourtServe: Birmingham County Court, District Judge Drayson 28/04/25</title>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <meta name="Generator" content="Microsoft Word 15 (filtered)">
    </head>
        <body>
            <b>Birmingham County Court, District Judge Drayson 28/04/25</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Birmingham"

def test_extract_city_newcastle():
    html = '''
    <html>
        <head>
        <title>CourtServe: Newcastle County Court, District Judge Drayson 28/04/25</title>
        </head>
        <body>
            <b> In the County Court and Family Court at Newcastle</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Newcastle"


def test_extract_city_city_case_insensitive():
    html =  '''
    <html>
        <head>
        <title>CourtServe: manchester County Court, District Judge Drayson 28/04/25</title>
        </head>
        <body>
            <b>manchester crown court - Civil Division</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Manchester"

def test_extract_city_no_city_name():
    html =  '''
    <html>
        <body>
            <b>blimpt lompts largdne</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None
    
def test_extract_city_no_head_tag():
    html =  '''
    <html>
        <body>
            <p>Manchester</p>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None

def test_extract_city_no_html():
    html =  ""
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None


''' --- Extract Rows --- '''

def test_extract_rows_normal():
    html = '''
        <tr style="page-break-inside:avoid">
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="91" valign="top" style="width:68.6pt;border:solid black 1.0pt;     border-top:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">10:00 AM</span></p>
    </td>
    <td width="37" valign="top" style="width:27.5pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">30 minutes</span></p>
    </td>
    <td width="292" valign="top" style="width:218.9pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">AF25F00027 IMPEY v GAREZE </span></p>
    </td>
    <td width="102" valign="top" style="width:76.6pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">Family Law Injunction (ex-parte)</span></p>
    </td>
    <td width="124" valign="top" style="width:93.2pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">In Person</span></p>
    </td>
   </tr>
    '''
    parser = create_parser_with_html(html)
    row_texts_messy = parser.extract_case_rows()
    assert len(row_texts_messy) == 1

def test_extract_rows_no_AM_or_PM():
    html = '''
        <tr style="page-break-inside:avoid">
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="91" valign="top" style="width:68.6pt;border:solid black 1.0pt;     border-top:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">10:00 </span></p>
    </td>
    <td width="37" valign="top" style="width:27.5pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">30 minutes</span></p>
    </td>
    <td width="292" valign="top" style="width:218.9pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">AF25F00027 IMPEY v GAREZE </span></p>
    </td>
    <td width="102" valign="top" style="width:76.6pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">Family Law Injunction (ex-parte)</span></p>
    </td>
    <td width="124" valign="top" style="width:93.2pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">In Person</span></p>
    </td>
   </tr>
    '''
    parser = create_parser_with_html(html)
    row_texts_messy = parser.extract_case_rows()
    assert len(row_texts_messy) == 0


def test_extract_rows_AM_in_word():
    html = '''
        <tr style="page-break-inside:avoid">
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="3" valign="top" style="width:2.25pt;border:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt">&nbsp;</span></p>
    </td>
    <td width="91" valign="top" style="width:68.6pt;border:solid black 1.0pt;     border-top:none;padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">10:00 </span></p>
    </td>
    <td width="37" valign="top" style="width:27.5pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">30 minutes</span></p>
    </td>
    <td width="292" valign="top" style="width:218.9pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">AF25F00027 IMPEYAM v GAREZE </span></p>
    </td>
    <td width="102" valign="top" style="width:76.6pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">Family Law Injunction (ex-parte)</span></p>
    </td>
    <td width="124" valign="top" style="width:93.2pt;border-top:none;border-left:     none;border-bottom:solid black 1.0pt;border-right:solid black 1.0pt;     padding:1.95pt 1.95pt 1.95pt 1.95pt">
    <p class="MsoNormal" style="margin-bottom:0cm;line-height:normal"><span lang="EN-US" style="font-size:8.0pt;font-family:&quot;Segoe UI&quot;,sans-serif;     color:black">In Person</span></p>
    </td>
   </tr>
    '''
    parser = create_parser_with_html(html)
    row_texts_messy = parser.extract_case_rows()
    assert len(row_texts_messy) == 0

    #TODO more tests could include... no html, loads of rows?  lowecase, maybe more