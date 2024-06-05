

""" DOCTYPE, DOCTYPE NAME """

# DEED = ["DEED", "DEED"]
# RPTT_RETT = ["RPTT&RET", "BOTH RPTT AND RETT"]
# RETT = ["RETT", "NYC REAL PROPERTY TRANSFER TAX"]
# AGREEMENT = ["AGMT", "AGREEMENT"]
# MORTGAGE = ["MTGE", "MORTGAGE"]
# MTGE_AND_CONS = ["M&CON", "MORTGAGE AND CONSOLIDATION"]
#
# DROPDOWN_IDX_DEED = [0]
# DROPDOWN_IDX_DEED_2 = []
# DROPDOWN_OTHER = RPTT_RETT
# # DROPDOWN_MORTGAGE = ["MORTGAGES AND INSTRUMENTS"]
#
#
# ALL_DOC_TYPES = [DEED, RPTT_RETT, RETT, AGREEMENT,
#                  MORTGAGE, MTGE_AND_CONS]
#
# DEED_DOC_TYPES = [DEED, RPTT_RETT, RETT]
#
# MORTGAGE_DOC_TYPES = [AGREEMENT, MORTGAGE, MTGE_AND_CONS]

SLEEP = 1
URL_SEARCH_HOME = "https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType"


# generate the objects
# DEED = Constants("DEED")
# OTHER = Constants("OTHER")
# LOAN = Constants("LOAN")

def strip_zero(a: str) -> str:
    a = a.replace(".", "")
    a = a.replace("$", "")
    a = a.replace(",", "")
    return a
