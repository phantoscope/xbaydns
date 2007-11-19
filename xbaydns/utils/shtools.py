# encoding: utf-8
"""
shtools.py

Created by 黄 冬 on 2007-11-07.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

import logging
import os
import shlex

from xbaydns.utils.command import CommandLine

log = logging.getLogger('perbay.utils.shtools')

def exec_(executable=None, file_=None, output=None, args=None):
    """Execute a program or shell script.
    
    :param executable: name of the executable to run
    :param file\_: name of the script file, relative to the project directory,
                  that should be run
    :param output: name of the file to which the output of the script should be
                   written
    :param args: command-line arguments to pass to the script
    """
    assert executable or file_, \
        'Either "executable" or "file" attribute required'

    returncode = execute(executable=executable, file_=file_,
                         output=output, args=args)

def pipe(executable=None, file_=None, input_=None, output=None,
         args=None):
    """Pipe the contents of a file through a program or shell script.
    
    :param executable: name of the executable to run
    :param file\_: name of the script file, relative to the project directory,
                  that should be run
    :param input\_: name of the file containing the data that should be passed
                   to the shell script on its standard input stream
    :param output: name of the file to which the output of the script should be
                   written
    :param args: command-line arguments to pass to the script
    """
    assert executable or file_, \
        'Either "executable" or "file" attribute required'
    assert input_, 'Missing required attribute "input"'

    returncode = execute(executable=executable, file_=file_,
                         input_=input_, output=output, args=args)

def execute(executable=None, file_=None, input_=None, output=None, args=None):
    """Generic external program execution.
    
    This function is not itself bound to a recipe command, but rather used from
    other commands.
    
    :param executable: name of the executable to run
    :param file\_: name of the script file, relative to the project directory,
                  that should be run
    :param input\_: name of the file containing the data that should be passed
                   to the shell script on its standard input stream
    :param output: name of the file to which the output of the script should be
                   written
    :param args: command-line arguments to pass to the script
    """
    if args:
        if isinstance(args, basestring):
            args = shlex.split(args)
    else:
        args = []

    if executable is None:
        executable = file_
    elif file_:
        args[:0] = [file_]

    if input_:
        input_file = file(input_, 'r')
    else:
        input_file = None

    output_file = None
    if output:
        output_file = file(output, 'w')

    try:
        log.debug('%s excuting args is %s', executable, args)
        cmdline = CommandLine(executable, args, input=input_file)
        for out, err in cmdline.execute():
            if out is not None:
                log.info(out)
                if output:
                    output_file.write(out + os.linesep)
            if err is not None:
                log.error(err)
                if output:
                    output_file.write(err + os.linesep)
    finally:
        if input_:
            input_file.close()
        if output:
            output_file.close()

    return cmdline.returncode