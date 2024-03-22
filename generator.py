from component_module.component import (
    page_style,
    page_tabs,
    crossgen_tab,
    chart_gen
)

page_style()
tab1, tab2 = page_tabs()

with tab1:
    crossgen_tab()
with tab2:
    chart_gen()