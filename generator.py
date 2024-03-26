from component_module.component import (
    page_style,
    page_tabs,
    init_crossgen_tab,
    init_chart_gen
)

page_style()
tab1, tab2 = page_tabs()

with tab1:
    init_crossgen_tab()
with tab2:
    init_chart_gen()