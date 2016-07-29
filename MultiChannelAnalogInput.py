import time
import numpy

from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

class MultiChannelAnalogInput():
    """Class to create a multi-channel analog input
    
    Usage: AI = MultiChannelAnalogInput(physicalChannel)
        physicalChannel: a string or a list of strings
        
    optional parameter:  reset: Boolean
    """
    def __init__(self,physicalChannel, reset = False):
        if type(physicalChannel) == type(""):
            self.physicalChannel = [physicalChannel]
        else:
            physicalChannel.sort()
            self.physicalChannel  =physicalChannel
        self.numberOfChannel = physicalChannel.__len__()
        self.limit = (-10.0,10.0)
        self.configure()
        
    def configure(self,SampleRate=1000,SampsPerChan=1):
        #creates one task handle for all the channels
        taskHandle = TaskHandle()
        self.taskHandle = taskHandle
        DAQmxCreateTask('',taskHandle)
        for name in self.physicalChannel:
            DAQmxCreateAIVoltageChan(taskHandle,name,"",DAQmx_Val_RSE,
                                     self.limit[0],self.limit[1],
                                     DAQmx_Val_Volts,None)
        self.timing(SampleRate,SampsPerChan)
            
    '''Method to set the sampling rate for the DAQ to run at,
    along with the number of samples that will be taken'''
    def timing(self,SampleRate,SampsPerChan):
        taskHandle = self.taskHandle
        DAQmxCfgSampClkTiming(taskHandle,"",SampleRate,DAQmx_Val_Rising,
                              DAQmx_Val_FiniteSamps,SampsPerChan)
        
    '''Method to read multiple signals given the following variables:
    timelength of the test in seconds
    sample rate in Hz
    
    Returns a dictionary of all the channels, and a list of what they read,
    and also a 'time' list for the time sample rate
    
    Note the time list is of datatype:       numpy.float64
    while the rest are of the datatype:     float

    That this will stop the code that is running until the DAQ is done taking data
    '''
    def readMulti(self,timelength = 1,
                  samplerate = 1000,
                  ):
        numchannels = self.numberOfChannel
        SampsPerChan = int(timelength*samplerate)
        timeout_point = timelength* 100
        dt = 1/samplerate
        self.timing(samplerate,SampsPerChan)
        datapoints = SampsPerChan*numchannels
        datalist =  numpy.zeros((datapoints,)) 
        read = int32()
        taskHandle = self.taskHandle
        DAQmxStartTask(taskHandle)
        StartSample=time.clock()
        DAQmxReadAnalogF64(taskHandle,SampsPerChan,timeout_point,
                           DAQmx_Val_GroupByScanNumber,datalist,datapoints,byref(read),None)
        EndSample = time.clock()
        DAQmxStopTask(taskHandle)
    ##Indexes the data according to channel
        data = {}
        for name in self.physicalChannel:
            data[name] = []
        for n in range(datapoints):
            x = n%self.numberOfChannel
            data[self.physicalChannel[x]].append(float(datalist[n]))      
        data['time'] = list(numpy.linspace(StartSample,EndSample,SampsPerChan, dtype = float))
        assert type(data['time']) == type(list())
        assert type(data) == type(dict())
        return data

    '''
    Method to return a single value for each channel
    will sample at 1kHz.  You 
    returns a dictionary-- channel name: value
    The difference between this and readMulti is that readSingle
        does not return a dict with lists, returns a dict with floats instead  
    '''
    def readSingle(self):
        data=self.readMulti(timelength=0.002)
        for key in data:
            data[key]=float(data[key][0])
        return data

    'Also want to use this function: DAQmxGetAIConvMaxRate'
if __name__ == '__main__':
    from matplotlib import pyplot as plt
    MCAI = MultiChannelAnalogInput(["Dev1/ai2","Dev1/ai1"])
    data1=MCAI.readSingle()
    time.sleep(0.5)
    data2=MCAI.readSingle()
    plt.plot(data1['time'],data1['Dev1/ai2'],'ro')
    plt.plot(data2['time'],data2['Dev1/ai2'],'ro')
    plt.show()

