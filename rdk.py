from psychopy import visual, event, core
import random
import numpy as np

# Experiment parameters
n_trials = 10
n_dots = 300
coherences = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
length_coherences = len(coherences)
dot_speed = 30 # in pixels per frame
dot_size = 5 # in pixels
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
                               fieldSize=(300, 300), fieldShape='Square')
clock = core.Clock()

# Instructions
instructions = """
Šiame eksperimente matyse vaizdus su atsitiktinai išdėliotais baltais taškais juodame fone.
Jūsų užduotis bus atsakyti, kur (lyginant su praėjusiu vaizdu) pajuda taškai. 

Jei atrodo, kad balti taškeliai pajuda į dešinę pusę - klaviatūroje spauskite rodykle į dešinę →.
Jei atrodo, kad balti taškeliai pajuda į kairę pusę - klaviatūroje spauskite rodykle į kairę ←.

Bandykite atsakyti tiksliai ir kiek įmanoma greičiau.

Iš viso reikės įvertinti {} vaizdus.

Pirmajame vaizde galite spausti bet kurią rodyklę - tai lyginamasis vaizdas antrajam vaizdui. 
Spauskite "SPACE" mygtuką, kad pradėtumėte eksperimentą.
""".format(n_trials * length_coherences)

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
        # Set coherence
        direction = random.choice([-1, 1])
        coherent_dots = int(n_dots * coherence / 100)
        direction_dots = [direction] * coherent_dots + [0] * (n_dots - coherent_dots)
        random.shuffle(direction_dots)

        # Update dot positions
        for i in range(n_dots):
            direction_dot = np.deg2rad(90 - i * 360/n_dots)
            x = dots_xys[i][0]
            y = dots_xys[i][1]
            x += dot_speed * np.cos(direction_dot) / frames_per_second
            y += dot_speed * np.sin(direction_dot) / frames_per_second
            dots_xys[i] = (x, y)

        # Update ElementArrayStim
        dots.xys = dots_xys

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
        elif (direction < 0 and response[0] == 'left') or \
            (direction > 0 and response[0] == 'right'):
            correct_responses += 1
            participant_data.append("[{}, 1]".format(coherence))
        else:
            participant_data.append("[{}, 0]".format(coherence))

# display end of experiment message
end = "Eksperimentas baigtas. Teisingų atsakymų: {}%. Ačiū už dalyvavimą!".format(round((correct_responses/(n_trials*length_coherences)*100)))
visual.TextStim(win, text=end, color=fixation_color, height=20).draw()
win.flip()
core.wait(5)
win.close()
core.quit()



# Save participant data
with open('results.txt', 'w') as f:
    f.write(" ".join(participant_data))

# Close the window and quit the program
win.close()
core.quit()