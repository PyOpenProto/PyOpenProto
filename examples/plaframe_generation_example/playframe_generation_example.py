import pandas as pd
import numpy as np
import random


# We will generate one playframe for one subject as example
# but should be a larger value than the number of subjects needed by the study
nb_subject = 1

# Let say we will play this list of stimulations
# corresponding to stim1.wav, stim2.wav, stim3.wav
play_list = ['stim1', 'stim2', 'stim3']

# Python dict of stimuli/triggers association
stim_trig = {
    'stim1': 1,
    'stim2': 2,
    'stim3': 3,
}


def get_playframe(i_sub):

    # Create the subject specific order. Will be a simple random here.
    random.shuffle(play_list)

    # Get trigger list corresponding to play_list random order
    trigger_list = [stim_trig[k] for k in play_list]

    # Get ISI corresponding to sequence, in ms, for example with normal
    # distribution around 300ms
    ISI_list = np.random.normal(300, 25, 3).astype(int)
    ISI_list.tolist()

    print(play_list)
    print(trigger_list)
    print(ISI_list)

    #Create and save playframe
    column_name = ['Stimulus', 'Trigger', 'ISI']
    df = pd.DataFrame(list(zip(play_list, trigger_list, ISI_list)),
               columns=column_name)
    csv_name =  './example_playframe_sub_' + str(i_sub) + '.csv'
    df.to_csv(csv_name)



if __name__ == '__main__':

    for i_sub in range(nb_subject):
        get_playframe(i_sub)
