

class EndlessLakePlayer(object):

    # take in a model from tensorflow to play the game
    def __init__(self, model):
        self.model = model


    # provide key output based on some feature vector
    def run_player(self):
        pass


    # actually press the spacebar
    def press_spacebar(self):
        pass

    # need ironpython to generate keystrokes




# what do i want to minmize??? The difference between the actual and expected value of (seconds since single jump + seconds since double jump)
# what does this entail then - have to capture seconds since last single jump. and seconds since last double jumpa
# then the output element - if second since last single jump < x, then single jump, if seconds since last double jump < x, then double jmp