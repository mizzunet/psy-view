# -*- coding: utf-8 -*-
"""main module of straditize

**Disclaimer**

Copyright (C) 2020  Philipp S. Sommer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>."""
import sys
import argparse
from textwrap import dedent
import psy_view


def start_app(ds, name=None, plotmethod='mapplot', preset=None):
    from PyQt5 import QtWidgets
    from PyQt5.QtGui import QIcon
    from psyplot_gui import rcParams

    rcParams['help_explorer.use_webengineview'] = False

    from psy_view.ds_widget import DatasetWidget
    from psyplot_gui.common import get_icon

    app = QtWidgets.QApplication(sys.argv)
    ds_widget = DatasetWidget(ds)
    ds_widget.setWindowIcon(QIcon(get_icon('logo.svg')))
    if preset is not None:
        ds_widget.load_preset(preset)
    if name is not None:
        if ds is None:
            raise ValueError("Variable specified but without dataset")
        elif name not in ds_widget.variable_buttons:
            valid = list(ds_widget.variable_buttons)
            raise ValueError(f"{name} is not part of the dataset. "
                             "Possible variables are {valid}.")
        ds_widget.plotmethod = plotmethod
        ds_widget.variable = name
        ds_widget.make_plot()
        ds_widget.refresh()
    ds_widget.show()
    ds_widget.show_current_figure()
    sys.excepthook = ds_widget.excepthook
    sys.exit(app.exec_())


def get_parser():
    parser = argparse.ArgumentParser('psy-view')

    parser.add_argument(
        'input_file', help="The file to visualize", nargs='?', default=None)

    parser.add_argument(
        '-n', '--name',
        help=("Variable name to display. Don't provide a variable to display "
              "the first variable found in the dataset."),
        const=object, nargs="?")

    parser.add_argument(
        '-pm', '--plotmethod', help="The plotmethod to use", default="mapplot",
        choices=["mapplot", "plot2d", "lineplot"])

    parser.add_argument(
        '--preset', help="Apply a preset to the plot")

    parser.add_argument(
        '-V', '--version', action='version', version=psy_view.__version__)

    parser.epilog = dedent("""
    psy-view  Copyright (C) 2020  Philipp S. Sommer

    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under the conditions of the GNU GENERAL PUBLIC LICENSE, Version 3.""")

    return parser


def main():
    import psyplot.project as psy
    parser = get_parser()
    args = parser.parse_known_args()[0]

    if args.input_file is not None:
        try:
            ds = psy.open_dataset(args.input_file)
        except:
            ds = psy.open_dataset(args.input_file, decode_times=False)
    else:
        ds = None

    if args.name is object and ds is not None:
        args.name = list(ds)[0]

    start_app(ds, args.name, args.plotmethod, args.preset)


if __name__ == '__main__':
    main()