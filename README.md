# Designing Filters using Python and VHDL

This guide runs through designing a filter using *python* and then using this to create a *VHDL* version and co simulating these in *coco-tb*.

## Requirements
* Anaconda/Conda this covers Python and all of the required packages. 
* [Cocotb](https://cocotb.readthedocs.io/en/latest/introduction.html)
* [GHDL](https://ghdl.readthedocs.io/en/latest/)
* [PyFDA](https://github.com/chipmuenk/pyfda) Optional. Note the pip and conda version (at the time this was written were well behind and did not include all the functionality required for the following tutorial).

## Filter Design

### PyFDA

Using PyFDA it is easy to design a filter with the following parameters. 
```
Low pass FIR
Sampling rate: FS: 1.92MHz
Pass Band: FPB : 20kHz
Stop Band: FSB : 100kHz
Pass Band Ripple : APB : 0.3 dB
Stop Band Suppression: ASB : 60 
```


This generates a filter with the following responce.

![pyFDA output](documentation\imageSource\pyFDAoutput.png)


### Python

Alternativaly *python* the coefficents can be found using the following code exmple:

```python
def CalculateFIR(fs,stopband, fcutoff,pass_ripple,stop_supression): 
n = (2/3)*np.log10(1/(10*pass_ripple*stop_supression))*(fs/(stopband-fcutoff)) 
n = int(np.ceil(math.sqrt(n**2)))
b = signal.firwin(n, cutoff = (fcutoff/(fs/2)), window = "hamming")
return b
```

The design can then be verified using:

```python
def PlotFilterFunction(b,fs):
  w_filter, h_filter = signal.freqz(b) 
  w_filterAsHz = w_filter*fs/(2*np.pi)
  plt.semilogx(w_filterAsHz, 20 * np.log10(abs(h_filter)))
  plt.title('Filter frequency response') 
  plt.xlabel('Frequency [Hz]') 
  plt.ylabel('Amplitude [dB]') 
  plt.margins(0, 0.1)
  plt.show()
```

Which plots:
![Filter created in Python](documentation\imageSource\pythonFilter.png)

## Python Filter implementation

Scipy includes *flitfilt* and other methods to filter the signal but in this excercise we will perform this mathmaticaly using the direct from of an FIR filter as documented in most text books. 


```python
def MathsFIRFilter(numtaps,b,signal):
  #Zero pad to match the tap lenght 
  zeros = np.zeros(numtaps)
  SignalToFilter = np.concatenate([zeros,signal])
  outputSignal = np.zeros(len(signal))
  #Loop to do the filtering
  for i in range((numtaps_fir + 1),len(signal)):
    FilterResult = np.multiply((SignalToFilter[i-numtaps_fir: i]),b)
    outputSignal[i-numtaps_fir] = np.sum(FilterResult) end = time.time()
  return outputSignal
```

## Validating the filter

While the responce can be plotted exciting the signal with white noise and inspecting the FFT is a good way to prove the filter. 

### White noise

The following function can be used to generate white noise for 0.1 seconds over the range of a number of bits:

```python
def WhiteNoiseGen(fs,bits):
  low = (2**(bits-1))*-1
  high = (2**(bits-1))
  noise = np.random.randint(int(low),int(high),size=int(fs/10)) 
  return noise
```

### FFT 

This simple FFT form is all that is required in this example:

```python
def fft(x, fs, SegmentLength):
  f, Pxx_spec = signal.welch(x, fs, 'hanning', nperseg=SegmentLength, noverlap=None plt.figure()
  plt.loglog(f, np.sqrt(Pxx_spec))
  plt.xlabel('Frequency [Hz]')
  plt.ylabel('Spectrum [Bits RMS]') 
  plt.show()
```

This generates the following responce which is of the correct form:

![Filtered white noise](documentation\imageSource\filteredWhiteNoise.png)


# Creating a VHDL filter

Many IDEs include functions for this or there is a [script](https://opencores.org/projects/fir_filter_generator) on opencores for this. Once the FIR filter compiles with *GHDL* then you can progress to co simulation. 


# Cocotb

In *python* create a coco-tb marker.
```python
@cocotb.test()
def filterTest(dut):
```

## Inputs and outputs
As with any VHDL test bench we will initially want to set up some entry states, a clock and then reset the system for a while before begining the test.
Values can be assigned to inputs using the form:

```
dut.data_i_value = 0
```
where data is the input port at the top level of the VHDL module. This is part of the cocotb class dut which is the VHDL module. Values can also be maped back to python.

## Resets

```
n_Reset = dut.n_Reset
```

Cocotb functions can be used to control the test bench for example:

```python
yield reset_dut(n_Reset, 1000)
```
Functions can also be created from this:

```python
@cocotb.coroutine
def reset_dut(n_Reset, duration):
  n_Reset <= 0
  yield Timer(duration, 'ns')
  n_Reset <= 1 
  n_Reset._log.debug("Reset complete") 
  print("Out of Reset")
```

Using the `<=` assignment makes the cocotb act liek a 'wait for ' on VHDL. 


## Clocks
```python
c = Clock(dut.clk, clock_period, 'ns')
cocotb.fork(c.start())
```
Using 'fork' the clock is created on a seperate thread and so the script can continue. 

Clocks can also me interacted with like they would in HDL.

```
clockedge = RaisingEdge(dut.clk)

yield clockedge
```

# Co-simulation

All of the above functions can be combined to simulate both the python and VHDL filters.

THe white noise function is used to generate the input the FFT to analyse it and the cocotb functions to drive the test using a simple for loop acting on the clock.

```python
inputSignal = [] 
Output = []
for i in range(len(Stimulus)): 
  yield clkedge
  inputSignal.append(Stimulus[i]) 
  dut.data_i.value = int(Stimulus[i]) 
  Output.append(dut.data_o.value.signed_integer)
```

Cocotb is then run using a simple make file with the lines
```
make SIM=ghdl TOPLEVEL_LANG=vhdl
```

Which generates:
![HDLoutput](documentation\imageSource\HDLoutput.png)
