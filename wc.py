def main():
    import args
    import log

    from memory.memory import Memory
    memory = Memory()

    from data.data import Data
    data = Data(memory.rom, args)

    from event.events import Events
    events = Events(memory.rom, args, data)

    from menus.menus import Menus
    menus = Menus(data.characters, data.dances)

    from battle import Battle
    battle = Battle()

    from settings import Settings
    settings = Settings()

    from bug_fixes import BugFixes
    bug_fixes = BugFixes()

    data.write()
    memory.write()

if __name__ == '__main__':
    main()
