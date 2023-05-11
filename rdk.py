from psychopy import visual, event, core, data
import random
import numpy as np

# Experiment parameters
n_trials = 5
n_dots = 800
coherences = [1, 30, 60, 90]
length_coherences = len(coherences)
dot_speed = 10 # in pixels per frame
dot_size = 5  # in pixels
bg_color = 'black'
fixation_color = 'white'
dot_color = 'white'
fixation_size = 2  # in pixels
fixation_thickness = 2  # in pixels
frames_per_second = 60
stimulus_duration = 0.5  # in seconds
response_keys = ['left', 'right']
escape_key = 'escape'

# Create window
win = visual.Window(size=[1280, 720], units='pix', color=bg_color, fullscr=True)

# Create stimuli
fixation = visual.GratingStim(win, tex=None, mask='circle', size=fixation_size,
                              pos=[0, 0], sf=0, color=fixation_color)
dots_xys = [(random.uniform(-150, 150), random.uniform(-150, 150)) for i in range(n_dots)]
dots = visual.ElementArrayStim(win, nElements=n_dots,
                               sizes=dot_size, colors=dot_color, elementTex=None,
                               xys=dots_xys, fieldPos=(0, 0),
                               fieldSize=(300, 300), fieldShape='Circle')

# Instructions
instructions = """
In this experiment, you will see a field of white dots on a black background. 
Your task is to judge whether the dots are moving to the left or to the right. 
If you think the dots are moving to the left, press the LEFT arrow key. 
If you think the dots are moving to the right, press the RIGHT arrow key. 
Try to respond as accurately and quickly as possible. 
There will be {} trials in total. 
Press the SPACEBAR to begin.
""".format(n_trials)

# Show instructions
visual.TextStim(win, text=instructions, color=fixation_color, height=20).draw()
win.flip()
event.waitKeys(keyList=['space'])

correct_responses = 0
participant_data = []
# Trial loop
for coherence in coherences:
    print(coherence)
    for trial in range(n_trials):
        dots.direction = random.choice([-1, 1]) * coherence
        dots_speed = dots.direction * dot_speed
        dots.xys += dots_speed / frames_per_second
        dots.xys += np.random.normal(scale=0.01, size=(n_dots, 2))

        # Draw stimuli
        dots.draw()
        fixation.draw()

        # Show stimuli
        win.flip()

        # Wait for response
        response = event.waitKeys(keyList=response_keys+[escape_key])
        if response == [escape_key]:
            win.close()
            core.quit()
        elif (dots.direction < 0 and response[0] == 'left') or \
             (dots.direction > 0 and response[0] == 'right'):
            correct_responses += 1
            participant_data.append("[{}, 1]".format(coherence))
        else:
            participant_data.append("[{}, 0]".format(coherence))

        # Clear the screen
        win.flip()

        # Pause before the next trial
        core.wait(stimulus_duration)


with open('results.txt', 'w') as f:
    f.write(" ".join(participant_data))

# Print the accuracy
print("Participant's accuracy: {}%".format((correct_responses/(n_trials*(len(coherences)))*100)))

# Close the window and quit the program
win.close()
core.quit()



