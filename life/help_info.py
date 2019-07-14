"""Module help_info."""
__author__ = 'Joan A. Pinol  (japinol)'


class HelpInfo:
    """Manages information used for help purposes."""

    def print_help_keys(self):
        print('  F1: \t show a GUI help screen'
              '   p: \t pause\n'
              ' ESC: cancel or quit\n'
              '      must be pressed 4 times when auto play mode is activated.\n'
              '  Alt + Enter: change full screen / normal screen mode\n'
              '  L_Ctrl + R_Alt + g:  grid\n'
              '  ^h: \t shows this help\n'
              '     \t left,     move selector to the left\n'
              '     \t right,    move selector to the right\n'
              '     \t up,       move selector up\n'
              '     \t down,     move selector down\n'
              '     \t Ctrl+movement key:  move selector several cells\n'
              '     \t c:        clean the universe\n'
              '     \t r:        reset the universe\n'
              '     \t n:        calculate next generation\n'
              '     \t o:        one color\n'
              '     \t s:        cell selector visibility on/off\n'
              '     \t t:        switch between toroidal/flat universe\n'
              '     \t Space:    continue/stop generations\n'
              '     \t Enter:    switch cell between dead/alive\n'
              '     \t           only if cell selector is visible\n'
              '  ^j: \t write generations to output file on/off\n'
              '  ^k: \t write statistics for current generation to output file\n'
              '  ^b: \t save buffer currently pending to write to output file\n'
              '  -------\n'
              '  Note:  Most keys will be deactivated when auto play is activated.\n'
              )
