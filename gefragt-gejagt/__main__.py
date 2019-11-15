import argparse
import eel


class GefragtGejagt(object):
    """docstring for GefragtGejagt."""

    def __init__(self, storage):
        super(GefragtGejagt, self).__init__()
        self.storage = storage


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Run the GefragtGejagt-Server',
        prog='python -m gefragt-gejagt')
    parser.add_argument('-c', '--continue', action='store_true',
                        help="Continue the last-saved Game")
    parser.add_argument('-l', '--listen', default="127.0.0.1:8080",
                        help="The address and port to listen to")
    parser.add_argument(
        '-s',
        '--storage',
        default="examples",
        help="The folder in which the .json files for the questions, teams,
        players etc. are stored and the current gamestate will be saved to.")
    return parser.parse_args()


@eel.expose
def list_teams():
    pass


if __name__ == '__main__':
    config = parse_arguments()

    eel.init('web', allowed_extensions=['.js', '.html'])
    print('Listening on {}'.format(self.config.listen))

    game = GefragtGejagt(config)

    eel.start('index.html')
