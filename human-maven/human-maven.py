import fileinput
import sys
import enum

try:
    import colorama
    colorama.init()
except ImportError:
    None

def trywarning(line, indent=7):
    if line.startswith('[WARNING] '):

        message = line[10:].strip() + '\n'

        if len(message) < 2: return True
        if message.startswith('No sources found skipping'): return True

        sys.stdout.write(' ' * indent)
        sys.stdout.write('\033[33mWARNING: ')
        sys.stdout.write(message)
        sys.stdout.write('\033[0m')
        sys.stdout.flush()
        return True
    return False

class State(enum.Enum):
    LF_REACTOR_1 = enum.auto()
    LF_REACTOR_2 = enum.auto()
    LF_REACTOR_END = enum.auto()
    LF_BUILDING_1_OR_REACTOR_SUMMARY = enum.auto()
    LF_BUILDING_2 = enum.auto()
    LF_BUILDING_END = enum.auto()
    LF_BUILD_RESULT = enum.auto()
    LF_TOTAL_TIME = enum.auto()

state = State.LF_REACTOR_1

for line in fileinput.input():

    if state == State.LF_REACTOR_1:
        if line.startswith('[INFO] Scanning for projects...'): state = State.LF_REACTOR_2
        continue

    if state == State.LF_REACTOR_2:
        if line.startswith('[INFO] -----'):
            state = State.LF_REACTOR_END
            continue
        trywarning(line, indent=0)
        continue

    if state == State.LF_REACTOR_END:
        if line.startswith('[INFO] -----'): state = State.LF_BUILDING_1_OR_REACTOR_SUMMARY
        continue

    if state == State.LF_BUILDING_1_OR_REACTOR_SUMMARY:
        if line.startswith('[INFO] Building '):
            sys.stdout.write('\033[32m=> ')
            sys.stdout.write(line[7:])
            sys.stdout.write('\033[0m')
            sys.stdout.flush()
            state = State.LF_BUILDING_2
            continue
        if line.startswith('[INFO] Reactor Summary'):
            state = State.LF_BUILD_RESULT
            continue
        continue

    if state == State.LF_BUILDING_2:
        if line.startswith('[INFO] -----'): state = State.LF_BUILDING_END
        continue

    if state == State.LF_BUILDING_END:
        if line.startswith('[INFO] -----'):
            state = State.LF_BUILDING_1_OR_REACTOR_SUMMARY
            continue

        if trywarning(line): continue

        message = line[7:].strip() + '\n'

        if message.startswith('--- '): continue
        if len(message) < 2: continue
        if message.startswith('No sources to compile'): continue
        if message.startswith('No tests to run'): continue
        if message.startswith('Using \'UTF-8\' encoding to copy'): continue
        if message.startswith('skip non existing resourceDirectory'): continue
        if message.startswith('Kotlin Compiler version '): continue
        if message.startswith('Nothing to compile - all classes are up to date'): continue
        if message.startswith('Module name is '): continue
        if message.startswith('Installing '): continue
        if message.startswith('Deleting '): continue
        if message.startswith('Changes detected - recompiling'): continue

        sys.stdout.write('       ')
        sys.stdout.write(line[7:])
        sys.stdout.flush()
        continue

    if state == State.LF_BUILD_RESULT:
        if not line.startswith('[INFO] BUILD '): continue
        state = State.LF_TOTAL_TIME
        continue

    if state == State.LF_TOTAL_TIME:
        if not line.startswith('[INFO] Total time: '): continue
        #sys.stdout.write('\n')
        #sys.stdout.write(line[7:])
        sys.exit()

    sys.stderr.write('ERROR: Unknown state ' + repr(state))
