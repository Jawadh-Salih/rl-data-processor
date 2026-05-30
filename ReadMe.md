We receive integer value sampled between 0-100. 
It's a continuos stream of data. 

The data is processed 100 samples at once. 
So we can collect a 100 samples and then start processing. and then wait for the next 100 to fill up 
and continue processing until done. 

We have to generate the data on our own. So a data generator is required to implement. 

When processing the sample we need to consider each 100 samples'

Max, Min, Mean, Std, Missing Samples (We have to mimic this as well),Number of corrupted samples (how to capture this)

We need to create a payload structure for what we receive.
