from component_module.component import (
    page_style,
    page_tabs,
    init_crossgen_tab,
    init_chart_gen
)
import logging

logging.basicConfig(
    filename='chart_generator.log',
    filemode='w',  # Overwrite the log file each time
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

page_style()
tab1, tab2 = page_tabs()

with tab1:
    init_crossgen_tab()
with tab2:
    init_chart_gen()