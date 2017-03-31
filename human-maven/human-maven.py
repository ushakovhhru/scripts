import fileinput
import sys
import enum

try:
    import colorama
    colorama.init()
except ImportError:
    None

machines_stack = []

class StateMachine:
    def __init__(self, context_processor, transitions, starting_state, context={}):
        self.state = starting_state
        self.context_processor = context_processor
        self.transitions = transitions
        self.context = context

    def to(self, newstate):
        if newstate not in self.transitions.get(self.state, []):
            sys.exit('BUG: No transition for ' + self.state + ' -> ' + newstate)
        self.state = newstate

    def process_context(self):
        return self.context_processor(self)

def out(line):
    sys.stdout.write(line)
    sys.stdout.flush()

def try_warning_transition(fsm, indent=7):
    global machines_stack
    global warning_machine
    line = fsm.context['line']
    fsm.context['indent'] = indent

    if line.startswith('[WARNING] '):
        warning_machine.state = 'process-begin'
        warning_machine.context = fsm.context
        machines_stack.insert(0, warning_machine)
        return True

def warning_machine_processor(fsm):
    global machines_stack
    line = fsm.context['line']
    indent = fsm.context['indent']
    state = fsm.state

    if state == 'process-begin':
        fsm.to('lf-end')
        message = line[10:].strip() + '\n'

        if len(message) < 2: return True
        if message.startswith('No sources found skipping'): return True

        out(' ' * indent + '\033[33mWARNING: ' + message + '\033[0m')
        return True

    if state == 'lf-end':
        if line.startswith('[WARNING] ') or line.startswith('[INFO] '):
            machines_stack.pop(0)
            return False
        out(' ' * indent + '\033[33m' + line + '\033[0m')
        return True

    sys.exit('BUG: unhandled state ' + state + ' for warning_machine')

def top_machine_processor(fsm):
    line = fsm.context['line']
    state = fsm.state

    if state == 'lf-reactor':
        if line.startswith('[INFO] Scanning for projects...'): fsm.to('lf-reactor-2')
        return True

    if state == 'lf-reactor-2':
        if line.startswith('[INFO] -----'):
            fsm.to('lf-reactor-end')
            return True
        if try_warning_transition(fsm, indent=0):
            return False
        return True

    if state == 'lf-reactor-end':
        if line.startswith('[INFO] -----'): fsm.to('lf-building-or-reactor-summary')
        return True

    if state == 'lf-building-or-reactor-summary':
        if line.startswith('[INFO] Building '):
            out('\033[32m=> ' + line[7:] + '\033[0m')
            fsm.to('lf-building-2')
            return True
        if line.startswith('[INFO] Reactor Summary'):
            fsm.to('lf-build-result')
            return True
        return True

    if state == 'lf-building-2':
        if line.startswith('[INFO] -----'): fsm.to('lf-building-end')
        return True

    if state == 'lf-building-end':
        if line.startswith('[INFO] -----'):
            fsm.to('lf-building-or-reactor-summary')
            return True

        if try_warning_transition(fsm):
            return False

        message = line[7:].strip() + '\n'

        if message.startswith('--- '): return True
        if len(message) < 2: return True
        if message.startswith('No sources to compile'): return True
        if message.startswith('No tests to run'): return True
        if message.startswith('Using \'UTF-8\' encoding to copy'): return True
        if message.startswith('skip non existing resourceDirectory'): return True
        if message.startswith('Kotlin Compiler version '): return True
        if message.startswith('Nothing to compile - all classes are up to date'): return True
        if message.startswith('Module name is '): return True
        if message.startswith('Installing '): return True
        if message.startswith('Deleting '): return True
        if message.startswith('Changes detected - recompiling'): return True

        out('       ' + line[7:])
        return True

    if state == 'lf-build-result':
        if not line.startswith('[INFO] BUILD '): return True
        fsm.to('lf-total-time')
        return True

    if state == 'lf-total-time':
        if not line.startswith('[INFO] Total time: '): return True
        sys.exit()

    sys.exit('BUG: Unknown state ' + repr(state))

top_machine = StateMachine(
        top_machine_processor,
        {
            'lf-reactor': [ 'lf-reactor-2' ],
            'lf-reactor-2': [ 'lf-reactor-end' ],
            'lf-building-or-reactor-summary': [ 'lf-building-2', 'lf-build-result' ],
            'lf-building-2': [ 'lf-building-end' ],
            'lf-building-end': [ 'lf-building-or-reactor-summary' ],
            'lf-build-result': [ 'lf-total-time' ],
            'lf-total-time': [],
            'lf-reactor-end': [ 'lf-building-or-reactor-summary' ]
        },
        'lf-reactor'
)

warning_machine = StateMachine(
        warning_machine_processor,
        {
            'process-begin': [ 'lf-end' ],
            'lf-end': []
        },
        ''
)

machines_stack.append(top_machine)

for line in fileinput.input():
    while True:
        machine = machines_stack[0]
        machine.context['line'] = line
        if machine.process_context():
            break
