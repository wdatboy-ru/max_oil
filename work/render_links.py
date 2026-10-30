# Подстановка ссылок: {{КОД:стр}} → [КОД, стр. N](file:///…#page=N); {{КОД}} → [КОД](file:///…)
import re, sys, pathlib, urllib.parse

DOCS = {
    'WP03': '20070216-5-01-Pub_Public_Winningsplan_F2A_Hanze.pdf',
    'WP12': 'WIPLA F2a Hanze_AANGEPAST-PUB.pdf',
    'WP24': 'V-66176 - Winningsplan F02a Hanze - Openbaar_Geredigeerd.pdf',
    'MAP1': 'F2-A-Hanze.pdf',
    'MAP2': 'F02-A-HANZE_20080404.pdf',
    'F3-WCR': 'F02-03/!!! NLOG_GS_PUB_27031902_F02-03.PDF',
    'F3-CORE': 'F02-03/NLOG_GS_PUB_27031904_F02-03.PDF',
    'F3-CPI': 'F02-03/NLOG_GS_PUB_27031906_F02-03.PDF',
    'F3-CD': 'F02-03/NLOG_GS_PUB_Core descriptions F02- 3.pdf',
    'F3-OIL': 'F02-03/NLOG_GS_PUB_Crude Oil Analysis_F02-03.pdf',
    'F3-DST': 'F02-03/NLOG_GS_PUB_Drill Stem Tests 1, 2 and 2A_F02-03.pdf',
    'F3-ETR': 'F02-03/NLOG_GS_PUB_Engineering Test Report_F02-03.pdf',
    'F3-IG4': 'F02-03/NLOG_GS_PUB_IG7031004_F02-03.PDF',
    'F3-IG5': 'F02-03/NLOG_GS_PUB_IG7031005_F02-03.PDF',
    'F3-IG6': 'F02-03/NLOG_GS_PUB_IG7031006_F02-03.PDF',
    'F3-TR': 'F02-03/NLOG_GS_PUB_Test Report_F02-03.pdf',
    'F3-WTR': 'F02-03/NLOG_GS_PUB_Well Test Report_ F02-03.pdf',
    'R1': 'F02-05/!!! NLOG_GS_PUB_F02-05 Lab progress report I (1996-07).pdf',
    'R2': 'F02-05/!!! NLOG_GS_PUB_F02-05 Lab progress report II WL9607 (1996-10).pdf',
    'R3': 'F02-05/frac_scal NLOG_GS_PUB_F02-05 Lab progress report III WL9701 (1997-01).pdf',
    'OIL98': 'F02-05/NLOG_GS_PUB_19980617-2-05_F0504_goed_20080602160040.pdf',
    'F6-OIL': 'F02-06/NLOG_GS_PUB_19970818-1-03_F02-06.PDF',
    'F6-FWR': 'F02-06/NLOG_GS_PUB_19980617-1-09_F02-06.PDF',
    'F6-DST': 'F02-06/NLOG_GS_PUB_19980617-1-10_F0206_Goed-20080509-142525.PDF',
    'F6-ML': 'F02-06/NLOG_GS_PUB_19980617-1-12_F0206_Matig-20080509-140526.PDF',
    'F6-CA': 'F02-06/NLOG_GS_PUB_F02-06 Core Analysis (1997-08).pdf',
    'F6-CA0': 'F02-06/NLOG_GS_PUB_F02-06 Core Analysis first results (1997-06).pdf',
    'A2-EVAL': 'F02-A-02/NLOG_GS_PUB_F2-A2 Final  well evaluation report _FINAL.pdf',
    'A2-DRL': 'F02-A-02/NLOG_GS_PUB_Final Well report F2-A2 (drilling).pdf',
    'A2-MICK': 'F02-A-02/NLOG_GS_PUB_Final Geological Reports/figures/F2-A2mick.xls',
    'A2-HDR': 'F02-A-02/NLOG_GS_PUB_Final Geological Reports/Enclosures/F2-A2p Complog header.xls',
    'A2-TAB': 'F02-A-02/NLOG_GS_PUB_Final Geological Reports/tables/Tab6.5.3_F2A2zSum_all.doc',
    'A2-PT': 'F02-A-02/NLOG_GS_PUB_Final Geological Reports/figures/Fig 8.1.2  F2-A2z production test.ppt',
    'A3-EVAL': 'F02-A-03/NLOG_GS_PUB_F2-A3 Final evaluation well report.doc',
    'A3-SCAL': 'F02-A-03/NLOG_GS_PUB_F02-A-03 SCAL Report vea000392190.pdf',
    'A3-MDT': 'F02-A-03/NLOG_GS_PUB_MDTpretestsF2A3.xls',
    'A3-MDTF': 'F02-A-03/NLOG_GS_PUB_MDT Fluid sample sheet.xls',
    'A3-DRL': 'F02-A-03/NLOG_GS_PUB_Final well report F2-A3 (drilling).pdf',
    'A3-INJ': 'F02-A-03/NLOG_GS_PUB_Figures/fig 8.1.1 Injectivity A3y.ppt',
    'A3-CORE': 'F02-A-03/NLOG_GS_PUB_Figures/fig 5.5.1a-c cores 1 and 2.ppt',
    'TNO': 'F02-A-03/NLOG_GS_PUB_TNO-2017-R10364.pdf',
    'A4-DRL': 'F02-A-04/NLOG_GS_PUB_Final well report F2-A4 (drilling).pdf',
    'A4-FMI': 'F02-A-04/NLOG_GS_PUB_20010813-1-10_F02-A-04.PDF',
    'A5-FWR': 'F02-A-05/NLOG_GS_PUB_Final Well Report F2-A5.doc',
    'A5-DRL': 'F02-A-05/NLOG_GS_PUB_Final well report F2-A5 (drilling).pdf',
    'A6-DANA': 'F02-A-06/NLOG_GS_PUB_F2-A6_DANA_FINAL_WELL_REPORT_CD.pdf',
    'A6-GEO': 'F02-A-06-SIDETRACK3/NLOG_GS_PUB_HAEXP-INT3-GG-RPT-0095.00 Geological Final Well Report F02-A-06 (-S1S2S3).pdf',
    'A6-FWR': 'F02-A-06-SIDETRACK3/NLOG_GS_PUB_FWR F2-A-06.pdf',
    'A6-NMR': 'F02-A-06-SIDETRACK1/NLOG_GS_PUB_F02-A-06_S1_MEM_NMR_200MD_2388m.pdf',
    'A6-CPI': 'F02-A-06-SIDETRACK1/NLOG_GS_PUB_17-8-F02-A-06-S1_CPI500_MD (1).pdf',
    'B1-GEO': 'F02-B-01/NLOG_GS_PUB_HPEXP-INT3-GG-RPT-0002 F02-B-01 Geological FWR.pdf',
    'B1-GP': 'F02-B-01/NLOG_GS_PUB_20090519-6-01_HPWEC-INT3-DR-PRG-0002-03 F2-B-01 Gravel pack screen completion.pdf',
    'B1-GAS': 'F02-B-01/NLOG_GS_PUB_F02-B-01 gas analysis.pdf',
    'B1-FWR': 'F02-B-01/NLOG_GS_PUB_HPWEC-INT3-DR-RPT-0001.00 F2-B-01 Pliocene Project Final Well Report.pdf',
    'TOPS': 'Model/Well Tie wells/Lithostratigraphy',
    'WELLS': 'Model/Wells',
    'PRJ': 'F02a Hanze — параметры для геологической и гидродинамической модели.md',
    'REV': 'F02a Hanze — ревизия данных для модели (2026-10-28).md',
}
OUTER = {  # файлы в корне for_claude и мануалы
    'VALHALL': 'Valhall_Paper.pdf',
    'EKO-TOUB': '321.pdf',
    'KRAKA': 'Aaboe_Dramsch_Welch_Luethje_Fractures.pdf',
    'EKO-JSG': '1-s2.0-S0191814119303724-main.pdf',
    'TN-DFN': 'tNav_manuals/tutorials/COMMON1.9_HowToCreateDualPorosityModelsViaDFN/How_to_Create_DFN_and_DPDP_Models_English.pdf',
    'TN-DP': 'tNav_manuals/tutorials/SIM7.3_HowToUseDualPoro/How_to_Use_Dual_Porosity_English.pdf',
    'TN-MD': 'tNav_manuals/tutorials/MD3.1_HowToCreateDualPorosityModel/How_to_Create_Dual_Porosity_Models_in_MD_English.pdf',
    'PET-UPS': 'Petrel_manuals/HelpCenter/xml/Scale_up_fracture_network_properties=GUID-27C130E4-54AA-4B3B-8BB4-87B7500D9293=1=en-US=.html',
    'PET-WF': 'Petrel_manuals/HelpCenter/xml/Fracture_modeling_workflow=GUID-9641AD9D-EFF2-444B-A7F9-9670B530A797=1=en-US=.html',
    'PET-J': 'Petrel_manuals/HelpCenter/xml/Create_J-functions_to_scale_capillary_pressure=GUID-4B1332B7-1FAA-4A67-B19C-EBEF85535C0A=1=en-US=.html',
}
BASE = pathlib.Path(__file__).resolve().parent.parent.as_uri() + '/'


def url(code, page=None):
    if code in DOCS:
        rel = 'Hanze_docs/' + DOCS[code]
    elif code in OUTER:
        rel = OUTER[code]
    else:
        raise KeyError(code)
    u = BASE + urllib.parse.quote(rel, safe='/!,-_.=')
    if page and rel.lower().endswith('.pdf'):
        u += f'#page={page}'
    return u, rel.lower().endswith('.pdf')


def repl(m):
    code, pages = m.group(1), m.group(2)
    if pages is None:
        u, _ = url(code)
        return f'[{code}]({u})'
    first = re.match(r'\d+', pages).group(0)
    u, is_pdf = url(code, first)
    label = f'{code}, стр. {pages}' + ('' if is_pdf else ' (конв.)')
    return f'[{label}]({u})'


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    t = open(src, encoding='utf-8').read()
    t = re.sub(r'\{\{([A-Z0-9\-]+)(?::([0-9][0-9–\-, ]*))?\}\}', repl, t)
    left = re.findall(r'\{\{[^}]*\}\}', t)
    open(dst, 'w', encoding='utf-8').write(t)
    print('ok, unresolved:', left[:10])
