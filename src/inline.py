import subprocess
from shlex import split

def str_to_list(cmd):
    return split(cmd)

def run_inline_cmd(cmd):
    cmd_list = str_to_list(cmd)
    output   = "Command " + cmd + " completed successfully!"
    try:
        process  = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out, error = process.communicate()
        if process.returncode != 0:
            return str(error)
        else:
            return out
    except OSError as e:
        return "invalid command: " + cmd
    except subprocess.CalledProcessError as e:
        run_inline_cmd(cmd)
    return output


