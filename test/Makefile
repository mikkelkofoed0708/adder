TOPLEVEL_LANG = verilog

# Peg på din Verilog-kildefil
VERILOG_SOURCES = $(PWD)/../src/tt_um_mikkelkofoed0708_adder.v

# Modulnavn i Verilog-filen
TOPLEVEL = tt_um_mikkelkofoed0708_adder

# Python testmodul (uden .py)
MODULE = tt_um_mikkelkofoed0708_adder_tb

SIM = icarus
WAVE = 1

# SÅ GitHub Actions finder resultaterne:
COCOTB_RESULTS_FILE = $(PWD)/results.xml

include $(shell cocotb-config --makefiles)/Makefile.sim
