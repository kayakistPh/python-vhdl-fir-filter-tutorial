import cocotb
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.monitors import Monitor
from cocotb.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess


import FilterAnaylserFunctions


@cocotb.coroutine
def reset_dut(n_Reset, duration):
    n_Reset <= 0
    yield Timer(duration, "ns")
    n_Reset <= 1
    n_Reset._log.debug("Reset complete")
    print("Out of Reset")


@cocotb.test()
def filterTest(dut):
    # Set up the clock
    fs = 2e6  # Hz

    # Generate the test waveforms
    Stimulus = FilterAnaylserFunctions.WhiteNoiseGen(fs, 18)

    # START Test

    n_Reset = dut.n_Reset
    dut.data_i.value = 0

    # Create a clock from which we start everything
    c = Clock(dut.clk, fs, "ns")
    cocotb.fork(c.start())

    clkedge = RisingEdge(dut.clk)

    # This will call reset_dut sequentially
    # Execution will block until reset_dut has completed
    yield reset_dut(n_Reset, 1000)
    dut._log.debug("Post reset")

    inputSignal = []
    Output = []

    # Wait for the clock edge
    for i in range(len(Stimulus)):
        yield clkedge
        inputSignal.append(Stimulus[i])
        dut.data_i.value = int(Stimulus[i])
        Output.append(dut.data_o.value.signed_integer)
    print("Applied signal now plotting.")
    FilterAnaylserFunctions.fft(Output, fs, 1028)
