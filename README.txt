#Potato_Gun
'''
This project is a work in progress.

The core modules behind this are pyDAQmx, 
  which provides an interface to NI DAQ modules (I use a USB-6009), 
  as well as PyQt4, for the app interface.
  
Within pyDAQmx module, I modified the MultiChannelAnalogInput script(already given by pyDAQmx), 
  and created an app for potato gun testing Using this modified script, 
  I created an app that takes voltages on the AI pins and plots them on graphs, 
  both animated(real-time) as well as plots of previous tests.




