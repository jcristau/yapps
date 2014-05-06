# grammar.py, part of Yapps 2 - yet another python parser system
# Copyright 1999-2003 by Amit J. Patel <amitp@cs.stanford.edu>
# Enhancements copyright 2003-2004 by Matthias Urlichs <smurf@debian.org>
#
# This version of the Yapps 2 grammar can be distributed under the
# terms of the MIT open source license, either found in the LICENSE
# file included with the Yapps distribution
# <http://theory.stanford.edu/~amitp/yapps/> or at
# <http://www.opensource.org/licenses/mit-license.php>
#

"""Parser for Yapps grammars.

This file defines the grammar of Yapps grammars.  Naturally, it is
implemented in Yapps.  The grammar.py module needed by Yapps is built
by running Yapps on yapps_grammar.g.  (Holy circularity, Batman!)

"""

import sys, re
from yapps import parsetree

######################################################################
def cleanup_choice(rule, lst):
    if len(lst) == 0: return Sequence(rule, [])
    if len(lst) == 1: return lst[0]
    return parsetree.Choice(rule, *tuple(lst))

def cleanup_sequence(rule, lst):
    if len(lst) == 1: return lst[0]
    return parsetree.Sequence(rule, *tuple(lst))

def resolve_name(rule, tokens, id, args):
    if id in [x[0] for x in tokens]:
        # It's a token
        if args:
            print 'Warning: ignoring parameters on TOKEN %s<<%s>>' % (id, args)
        return parsetree.Terminal(rule, id)
    else:
        # It's a name, so assume it's a nonterminal
        return parsetree.NonTerminal(rule, id, args)


# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class ParserDescriptionScanner(runtime.Scanner):
    patterns = [
        ('"rule"', re.compile('rule')),
        ('"ignore"', re.compile('ignore')),
        ('"token"', re.compile('token')),
        ('"option"', re.compile('option')),
        ('":"', re.compile(':')),
        ('"parser"', re.compile('parser')),
        ('[ \t\r\n]+', re.compile('[ \t\r\n]+')),
        ('#.*?\r?\n', re.compile('#.*?\r?\n')),
        ('EOF', re.compile('$')),
        ('ATTR', re.compile('<<.+?>>')),
        ('STMT', re.compile('{{.+?}}')),
        ('ID', re.compile('[a-zA-Z_][a-zA-Z_0-9]*')),
        ('STR', re.compile('[rR]?\'([^\\n\'\\\\]|\\\\.)*\'|[rR]?"([^\\n"\\\\]|\\\\.)*"')),
        ('LP', re.compile('\\(')),
        ('RP', re.compile('\\)')),
        ('LB', re.compile('\\[')),
        ('RB', re.compile('\\]')),
        ('OR', re.compile('[|]')),
        ('STAR', re.compile('[*]')),
        ('PLUS', re.compile('[+]')),
        ('QUEST', re.compile('[?]')),
        ('COLON', re.compile(':')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{'[ \t\r\n]+':None,'#.*?\r?\n':None,},str,*args,**kw)

class ParserDescription(runtime.Parser):
    Context = runtime.Context
    def Parser(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'Parser', [])
        self._scan('"parser"', context=_context)
        ID = self._scan('ID', context=_context)
        self._scan('":"', context=_context)
        Options = self.Options(_context)
        Tokens = self.Tokens(_context)
        Rules = self.Rules(Tokens, _context)
        EOF = self._scan('EOF', context=_context)
        return parsetree.Generator(ID,Options,Tokens,Rules)

    def Options(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'Options', [])
        opt = {}
        while self._peek('"option"', '"token"', '"ignore"', 'EOF', '"rule"', context=_context) == '"option"':
            self._scan('"option"', context=_context)
            self._scan('":"', context=_context)
            Str = self.Str(_context)
            opt[Str] = 1
        return opt

    def Tokens(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'Tokens', [])
        tok = []
        while self._peek('"token"', '"ignore"', 'EOF', '"rule"', context=_context) in ['"token"', '"ignore"']:
            _token = self._peek('"token"', '"ignore"', context=_context)
            if _token == '"token"':
                self._scan('"token"', context=_context)
                ID = self._scan('ID', context=_context)
                self._scan('":"', context=_context)
                Str = self.Str(_context)
                tok.append( (ID,Str) )
            else: # == '"ignore"'
                self._scan('"ignore"', context=_context)
                self._scan('":"', context=_context)
                Str = self.Str(_context)
                ign = ('#ignore',Str)
                if self._peek('STMT', '"token"', '"ignore"', 'EOF', '"rule"', context=_context) == 'STMT':
                    STMT = self._scan('STMT', context=_context)
                    ign = ign + (STMT[2:-2],)
                tok.append( ign )
        return tok

    def Rules(self, tokens, _parent=None):
        _context = self.Context(_parent, self._scanner, 'Rules', [tokens])
        rul = []
        while self._peek('"rule"', 'EOF', context=_context) == '"rule"':
            self._scan('"rule"', context=_context)
            ID = self._scan('ID', context=_context)
            OptParam = self.OptParam(_context)
            self._scan('":"', context=_context)
            ClauseA = self.ClauseA(ID, tokens, _context)
            rul.append( (ID, OptParam, ClauseA) )
        return rul

    def ClauseA(self, rule, tokens, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ClauseA', [rule, tokens])
        ClauseB = self.ClauseB(rule,tokens, _context)
        v = [ClauseB]
        while self._peek('OR', 'RP', 'RB', '"rule"', 'EOF', context=_context) == 'OR':
            OR = self._scan('OR', context=_context)
            ClauseB = self.ClauseB(rule,tokens, _context)
            v.append(ClauseB)
        return cleanup_choice(rule,v)

    def ClauseB(self, rule,tokens, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ClauseB', [rule,tokens])
        v = []
        while self._peek('STR', 'ID', 'LP', 'LB', 'STMT', 'OR', 'RP', 'RB', '"rule"', 'EOF', context=_context) in ['STR', 'ID', 'LP', 'LB', 'STMT']:
            ClauseC = self.ClauseC(rule,tokens, _context)
            v.append(ClauseC)
        return cleanup_sequence(rule, v)

    def ClauseC(self, rule,tokens, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ClauseC', [rule,tokens])
        ClauseD = self.ClauseD(rule,tokens, _context)
        _token = self._peek('PLUS', 'STAR', 'QUEST', 'STR', 'ID', 'LP', 'LB', 'STMT', 'OR', 'RP', 'RB', '"rule"', 'EOF', context=_context)
        if _token == 'PLUS':
            PLUS = self._scan('PLUS', context=_context)
            return parsetree.Plus(rule, ClauseD)
        elif _token == 'STAR':
            STAR = self._scan('STAR', context=_context)
            return parsetree.Star(rule, ClauseD)
        elif _token == 'QUEST':
            QUEST = self._scan('QUEST', context=_context)
            return parsetree.Option(rule, ClauseD)
        else:
            return ClauseD

    def ClauseD(self, rule,tokens, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ClauseD', [rule,tokens])
        _token = self._peek('STR', 'ID', 'LP', 'LB', 'STMT', context=_context)
        if _token == 'STR':
            STR = self._scan('STR', context=_context)
            t = (STR, eval(STR,{},{}))
            if t not in tokens: tokens.insert( 0, t )
            return parsetree.Terminal(rule, STR)
        elif _token == 'ID':
            ID = self._scan('ID', context=_context)
            OptParam = self.OptParam(_context)
            return resolve_name(rule,tokens, ID, OptParam)
        elif _token == 'LP':
            LP = self._scan('LP', context=_context)
            ClauseA = self.ClauseA(rule,tokens, _context)
            RP = self._scan('RP', context=_context)
            return ClauseA
        elif _token == 'LB':
            LB = self._scan('LB', context=_context)
            ClauseA = self.ClauseA(rule,tokens, _context)
            RB = self._scan('RB', context=_context)
            return parsetree.Option(rule, ClauseA)
        else: # == 'STMT'
            STMT = self._scan('STMT', context=_context)
            return parsetree.Eval(rule, STMT[2:-2])

    def OptParam(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'OptParam', [])
        if self._peek('ATTR', '":"', 'PLUS', 'STAR', 'QUEST', 'STR', 'ID', 'LP', 'LB', 'STMT', 'OR', 'RP', 'RB', '"rule"', 'EOF', context=_context) == 'ATTR':
            ATTR = self._scan('ATTR', context=_context)
            return ATTR[2:-2]
        return ''

    def Str(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'Str', [])
        STR = self._scan('STR', context=_context)
        return eval(STR,{},{})


def parse(rule, text):
    P = ParserDescription(ParserDescriptionScanner(text))
    return runtime.wrap_error_reporter(P, rule)

# End -- grammar generated by Yapps
