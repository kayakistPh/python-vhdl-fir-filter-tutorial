TOPLEVEL_LANG ?= vhdl

PWD=$(shell pwd)

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(WPWD)/../model;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)
endif

SIM_ARGS= --vcd=coco_filter.vcd
VHDL_SOURCES = ./HDL/Filter.vhdl



TOPLEVEL := fir_filter
MODULE   := test_filter

include $(shell cocotb-config --makefiles)/Makefile.inc
include $(shell cocotb-config --makefiles)/Makefile.sim
