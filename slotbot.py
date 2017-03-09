"""
slotbot.py
a command-line controller program for a robotic arm that takes commands that move blocks stacked in a series of slots

Daniel Slosky: March 9, 2017
"""
import time

class SlotBot(object):
    """
    A robotic arm that takes commands that move blocks stacked in a series of slots

    If I had more time:
        Implement print method instead of printing from each individual method
        Add an error method that prints a more visible string when there is invalid input
        Create tests for each method
        Run through pyLint and fix PEP-8 violations
    """
    def __init__(self):
        self.slots = {}
        self.slot_record = []

        # a dictionary of commands makes it easy to run functions from
        # string inputs
        self.commands = {'size': self.size,
                         'add': self.add,
                         'mv': self.mv,
                         'rm': self.rm,
                         'replay': self.replay,
                         'undo': self.undo}

    def __str__(self):
        return self.make_slots_string(self.slots)

    @staticmethod
    def make_slots_string(slots):
        """
        Returns a formatted output string for a slots input
        """
        slot_str = ''
        for slot,num in slots.iteritems():
            slot_str += '{}: {}\n'.format(slot,
                                           'X' * num)

        return slot_str

    def command(self, input):
        """
        Parses a string input and runs a command
        """
        split_command = input.split(' ')
        command_name = split_command[0]

        # turn arguments into integers
        args = []
        for arg in split_command[1:]:
            args.append(int(arg))

        # run the command
        self.commands[command_name](*args)

        # record the changes if the user does anything but replay
        if command_name != 'replay':
            self.record_slot()

    def record_slot(self):
        """
        Make a copy for the record if we change the slots
        """
        new_slot = {}
        for slot, count in self.slots.iteritems():
            new_slot[slot] = count

        self.slot_record += [new_slot]

    def size(self, num):
        """
        Adjusts the number of the slots
        """
        if len(self.slots.keys()) == 0:
            for i in range(num):
                self.slots[i+1] = 0

        elif len(self.slots.keys()) < num:
            # add the extra slots
            for i in range(num):
                if self.slots.get(i+1, None) is None:
                    self.slots[i+1] = 0

        elif len(self.slots.keys()) > num:
            new_slots = {}

            # remove extra slots and move extra blocks
            extra_blocks = 0
            for slot,count in self.slots.iteritems():
                if slot <= num:
                    new_slots[slot] = count
                else:
                    extra_blocks += count

            # redistribute extra blocks if new size is not 0
            if len(new_slots.keys()) > 0 and extra_blocks > 0:
                # this block redistribution could easily be optimized
                # if I had a bit more time
                while extra_blocks > 0:
                    for slot in new_slots.keys():
                        if extra_blocks > 0:
                            new_slots[slot] += 1
                            extra_blocks -= 1
            
            self.slots = new_slots

    def add(self, slot):
        """
        Adds a block to slot
        """
        self.slots[slot] += 1

    def mv(self, slot1, slot2):
        """
        Move block from slot1 to slot2
        """
        if self.slots[slot1] > 0:
            self.slots[slot1] -= 1
            self.slots[slot2] += 1
        else:
            print 'No blocks to move'

    def rm(self, slot):
        if self.slots[slot] > 0:
            self.slots[slot] -= 1
        else:
            print 'No blocks to remove'

    def replay(self, num):
        """
        Replays the last num of commands without altering the current
        slots
        """
        replay_pos = len(self.slot_record) - num - 1

        if replay_pos <= 0:
            print 'Can\'t replay that far.'
        else:
            while replay_pos < len(self.slot_record):
                slot = self.slot_record[replay_pos]
                slot_str = self.make_slots_string(slot)
                print slot_str

                replay_pos += 1

                time.sleep(.5)


    def undo(self, num):
        undo_pos = len(self.slot_record) - num - 1
        self.slots = self.slot_record[undo_pos]


class SlotBotInterface(object):
    """
    An interface to the SlotBot object

    If I had more time:
        Add an error method that prints a more visible string when there is invalid input
        Create validation unit tests
        Format 'help' code and move it into its own function
        Run through pyLint and fix PEP-8 violations
    """
    def __init__(self):
        self.commands = {'size': 1,
                         'add': 1,
                         'mv': 2,
                         'rm': 1,
                         'replay': 1,
                         'undo': 1}

    def validate(self,command):
        """
        Validates the user's input. Returns True for valid commands
        """
        split_command = command.split(' ')
        
        # check valid code
        if split_command[0] not in self.commands:
            # bad code word
            print '\nBad code word: {}'.format(split_command[0])
            return False

        elif self.commands[split_command[0]] != len(split_command) - 1:
            # wrong number of input arguments
            print '\nWrong number of input arguments'

            correct_arg_count = self.commands[split_command[0]]
            print '\n{} takes {} argument/s'.format(split_command[0],
                                                  correct_arg_count)

            return False

        else:
            for arg in split_command[1:]:
                try:
                    int(arg)
                except:
                    print '\n{} is not an integer'.format(arg)
                    # argument is not an integer
                    return False
        
        return True

    def run(self):
        """
        Runs the main UI loop
        """
        sb = SlotBot()

        # initialize
        init = False
        while init is False:
            input = raw_input('Input an integer size to '
                                'initialize your SlotBot: ')
            command = 'size {}'.format(input)
            validated = self.validate(command)

            if validated is True:
                print 'SlotBot initialized!'
                sb.command(command)
                init = True
        
        # main loop
        quit = False
        while quit is False:

            print '\nCurrent State:\n{}'.format(str(sb))

            command = raw_input('Next Command: ')

            if command != 'quit' and command != 'help':
                validated = self.validate(command)
                if validated is True:
                    sb.command(command)

            elif command == 'help':
                print """
SlotBot Help:

quit - Exits the user interface
size [int] - Adjusts the number of slots, resizing if necessary.
add [int] - Adds a block to the specified slot.
mv [int] [int] - Moves a block from slot1 to slot2.
rm [int] - Removes a block from the slot.
replay [int] - Replays the last n commands.
undo [int] - Undo the last n commands.
                """
            else:
                print 'Goodbye!'
                quit = True

if __name__ == '__main__':
    ui = SlotBotInterface()
    ui.run()