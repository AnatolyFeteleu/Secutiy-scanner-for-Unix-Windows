import importlib
import pymysql
import settings

imported_config = importlib.import_module('get_config')

ssh = importlib.import_module('ssh')
wmi = importlib.import_module('wmi_transport')
sql = importlib.import_module('sql')


class TransportSSH:
    @staticmethod
    def execution_command(command):
        stdin, stdout, stderr = ssh.get_connection().exec_command(command)
        result = []
        if stderr.readlines():
            stdin, stdout, stderr = ssh.get_connection().exec_command(command)
            result.append(stderr.readlines()[0].rstrip())
            return result[0], False
        else:
            for i in stdout.readlines():
                result.append(i.rstrip())
            return result[1:], True

    @staticmethod
    def get_file(remote_path, local_path):
        stdin, stdout, stderr = ssh.get_connection().exec_command('cat %s' % remote_path)
        sftp_client = ssh.open_sftp()
        if not stderr.readlines():
            sftp_client.get(remote_path, local_path)
            contents = []
            for i in stdout:
                contents.append(i)
            return contents, True
        else:
            stdin, stdout, stderr = ssh.get_connection().exec_command('cat %s' % remote_path)
            return stderr.readlines(), False

    @staticmethod
    def file_exists(path):
        sftp_client = ssh.open_sftp()
        try:
            sftp_client.stat(path)
            return settings.STATUSES[1]
        except FileNotFoundError:
            return settings.STATUSES[2]

    @staticmethod
    def get_users():
        result = list()
        for i in TransportSSH.execution_command('cat /etc/passwd'):
            if not isinstance(i, bool):
                for j in i:
                    result.append(j.split(':')[0])
        return result

    @staticmethod
    def identify_device_debian():
        assert TransportSSH.get_os()[0]['Distributor ID'] == 'Debian', 'Only for Debian OS'
        commands = dict(MAC='ip link | grep link/ether', OS_Config='uname -a')
        result = []
        for cmd in commands.values():
            stdin, stdout, stderr = ssh.get_connection().exec_command(cmd)
            if stderr.readlines():
                stdin, stdout, stderr = ssh.get_connection().exec_command(cmd)
                string = stderr.readlines(); string = string.replace('\n', '')
                result.append(string)
            else:
                for i in stdout.readlines():
                    string = i.replace('  ', ''); string = string.replace('\n', '')
                    result.append(string)
        return result, True

    @staticmethod
    def my_conf(input, output):
        global write_to_file
        write_to_file = output
        with open(input) as read_lines, open('%s' % write_to_file, 'w') as write_lines:
            for i in read_lines: write_lines.write(i) if (('#' not in i) and (';' not in i)) else None
        return write_to_file

    @staticmethod
    def get_value_from_conf(key):
        params = {}
        assert write_to_file
        for i in open(write_to_file, 'r'):
            if '!' not in i: i = i.replace(' ', '').rstrip().split('=')
            try:
                if '!' in i[0]:
                    i = str(i).replace('!', '').split(' ')
                    params.update({i[0]: i[1]})
                else:
                    params.update({i[0]: i[1]})
            except IndexError:
                if i[0] and '[' not in i[0]:
                    i.append(None)
                    params.update({i[0]: i[1]})
        return '%s: %s' % (key, params[key])

    @staticmethod
    def check_permissions(path, permissions, user, group):
        permissions = str(permissions); user = user.lower(); group = group.lower()
        check = TransportSSH.execution_command('ls -l %s' % path)
        d = {0: '---', 1: '--x', 2: '-w-', 3: '-wx', 4: 'r--', 5: 'r-x', 6: 'rw-', 7: 'rwx'}
        l = [int(i) for i in permissions]
        m = []
        for num in l:
            m.append(d[num])
        m = ''.join(m)
        stdin, stdout, stderr = ssh.get_connection().exec_command('ls -l %s' % path)
        file_permission = stdout.readlines()
        file_permission = file_permission[0].split(' ')
        file_permission, file_owner, file_group = file_permission[0], file_permission[2], file_permission[3]
        file_permission = file_permission.split('-')
        del file_permission[0]
        file_permission = '-'.join(file_permission)
        if check[1] is True:
            return [file_permission, 'owner: %s' % file_owner, 'group: %s' % file_group], \
                   (m == file_permission and user == file_owner and group == file_group)
        else:
            return 'File not found'

    @staticmethod
    def set_permissions(path, permissions):
        stdin, stdout, stderr = ssh.get_connection().exec_command('chmod %s %s' % (permissions, path))
        if stderr.readlines():
            return False
        else:
            return True

    @staticmethod
    def get_os():
        stdin, stdout, stderr = ssh.get_connection().exec_command('ver')
        os = []
        if not stderr:  # Need test
            os.extend([stdout.readlines().rstrip(), True])
        else:
            stdin, stdout, stderr = ssh.get_connection().exec_command('lsb_release -i')
            try:
                out = stdout.readlines()[0].rstrip()
                out = out.split(':')
                os.append({out[0]: out[1].replace('\t', '')})
            except IndexError:
                return settings.STATUSES[5]
        return os[0], True

    @staticmethod
    def get_installed_pkg():
        pkgs = {}
        try:
            if TransportSSH.get_os()[0]['Distributor ID'] == 'Ubuntu' or 'Debian':
                stdin, stdout, stderr = ssh.get_connection().exec_command("dpkg -l | grep ^ii | awk '{ print $2,$3}'")
                out = stdout.readlines()
                out = ' '.join(out)
                out = out.split(' ')
                pkgs.update({out[i]: out[i+1].rstrip() for i in range(0, len(out)-1, 2)})
            else:
                stdin, stdout, stderr = ssh.get_connection().exec_command("'rpm -qa | grep ^ii | awk '{ print $2,$3}''")
                out = stdout.readlines()
                out = ' '.join(out)
                out = out.split(' ')
                pkgs.update({out[i]: out[i+1].rstrip() for i in range(0, len(out)-1, 2)})
            return pkgs, True
        except:
            return settings.STATUSES[5]


class TransportWMI:
    @staticmethod
    def wmi_exec(command):
        try:
            wmi.get_connection().get.Win32_Process.Create(CommandLine=r"cmd.exe /c IF NOT EXIST 'C:\Windows\temp' mkdir C:\Windows\temp")
            execution = wmi.get_connection().Win32_Process.Create(
                CommandLine=r"cmd.exe /c cd C:\Windows\temp && %s echo >> commands.txt" % command
            )
            return print('Process id: %s' % execution[0])
        except AttributeError:
            return settings.STATUSES[5]

    @staticmethod
    def wmi_query():
        try:
            wql = "select Caption, OSArchitecture, Version from Win32_OperatingSystem"
            os_name, os_architecture, os_version = [None] * 3
            for Computer in wmi.get_connection().query(wql):
                os_name, os_architecture, os_version = Computer.Caption, Computer.OSArchitecture, Computer.Version

            os_name = os_name.split(' '); del os_name[0]; os_name = ' '.join(os_name)
            os_dict = dict({'OSName': os_name, 'OSArchitecture': os_architecture, 'OSVersion': os_version})

            wql = "select Name, DNSHostName, Domain, Workgroup, PartOfDomain from Win32_ComputerSystem"
            net_bios, host_name, domain, workgroup = [None] * 4
            for Computer in wmi.get_connection().query(wql):
                net_bios, host_hame = Computer.Name, Computer.DNSHostName
                if Computer.PartOfDomain:
                    domain = Computer.Domain
                if not Computer.PartOfDomain:
                    workgroup = Computer.Workgroup
            os_net = dict({'NetBIOSName': net_bios, 'HostName': host_name, 'Domain': domain, 'Workgroup': workgroup})
            return os_dict, os_net
        except AttributeError:
            return settings.STATUSES[5]

    @staticmethod
    def get_value(key, path, value):
        query = wmi.get_connection().StdRegProv.GetDWORDValue(hDefKey=settings.WMI_KEYS[key],
                                                              sSubKeyName="%s" % path,
                                                              sValueName="%s" % value)
        return query[1]

    @staticmethod
    def change_value(key, path, value, change_to=1):
        query = wmi.get_connection().StdRegProv.GetDWORDValue(hDefKey=settings.WMI_KEYS[key],
                                                              sSubKeyName="%s" % path,
                                                              sValueName="%s" % value)
        if not query[1]:
            if query[1] == 0:
                wmi.get_connection().StdRegProv.SetStringValue(
                    hDefKey=settings.WMI_KEYS[key],
                    sSubKeyName="%s" % path,
                    sValueName="%s" % value,
                    sValue=hex(change_to)
                )
                return print("Changed to: %s" % change_to)
            else:
                return print("Normal")
        else:
            return settings.STATUSES[5]


class TransportSQL:
    @staticmethod
    def sql_exec(statement):
        with sql.get_connection().cursor() as cursor:
            try:
                cursor.execute(statement)
                result = cursor.fetchone()
                return result
            except pymysql.err.ProgrammingError:
                raise pymysql.MySQLError

    @staticmethod
    def check_db(database):
        return TransportSQL.sql_exec('SHOW DATABASES LIKE "%s";' % database)

    @staticmethod
    def check_table(table):
        return TransportSQL.sql_exec('CHECK TABLE %s;' % table)['Msg_text']

    @staticmethod
    def get_db_version():
        import re
        result = TransportSQL.sql_exec('SELECT variable_value FROM information_schema.global_variables WHERE variable_name = "VERSION";')
        pattern = r'[0-9]+[\.]?[0-9]+[\.]?[0-9]+[\.]?'
        match = re.search(pattern, result['variable_value'])
        return match.group()

    @staticmethod
    def get_global_vars():
        return TransportSQL.sql_exec('SELECT * FROM information_schema.global_variables;')

    @staticmethod
    def max_version(attr_list):
        from operator import itemgetter
        list_with_lists = []
        main_list = []
        for i in attr_list:
            version = str(i).split('.')
            list_with_lists.append([int(i) for i in version])
        sorted_list_with_lists = sorted(list_with_lists, key=itemgetter(0, 1, 2), reverse=True)
        for attr_list in sorted_list_with_lists:
            main_list.append('.'.join(str(item) for item in attr_list))
        return main_list

    @staticmethod
    def checking_current_version(release=None):
        release = '10.0.35'
        current_ver = TransportSQL.get_db_version()
        release_int = release.split('.')
        current_int = current_ver.split('.')
        if release_int < current_int:
            return 'You have a newer version of MariaDB (%s)' % current_ver
        elif release_int == current_int:
            return 'You have a release version of MariaDB (%s)' % release
        else:
            return 'You have an old version of MariaDB.\nCurrent release version is: %s' % release

#class TransportSNMP:
#    def __init__(self): pass
#
#    def get_information(self, mode):
#        global interfaces
#        mode = mode.lower()
#        result = ''
#        interfaces = {}
#        modes = {'interfaces': '1.3.6.1.2.1.2.2.1.2', 'modes': '1.3.6.1.2.1.2.2.1.8', 'users': '1.3.6.1.2.1.25.1.5', 'types': '1.3.6.1.2.1.2.2.1.3', 'ports': '1.3.6.1.4.1.9.9.87.1.4.1.1.24'}
#        if mode in modes.keys():
#            for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
#                    SnmpEngine(),
#                    CommunityData('public', mpModel=0),
#                    UdpTransportTarget(('127.0.0.1', 161)),
#                    ContextData(),
#                    0, 50,  # GETBULK specific: request up to 50 OIDs in a single response
#                    ObjectType(ObjectIdentity(modes[mode])),
#                    lookupMib=False, lexicographicMode=False):
#                if errorIndication:
#                    print(errorIndication)
#                    break
#                elif errorStatus:
#                    print('%s at %s' % (
#                    errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#                    break
#                else:
#                    for varBind in varBinds:
#                        result = ' = '.join([x.prettyPrint() for x in varBind])
#                        interfaces.update({result.split()[0]: result.split()[-1]}) if result.split()[-1] != 'View' else None
#        elif mode == 'sys':
#            errorIndication, errorStatus, errorIndex, varBinds = next(
#                getCmd(SnmpEngine(),
#                       CommunityData('public', mpModel=0),
#                       UdpTransportTarget(('127.0.0.1', 161)),
#                       ContextData(),
#                       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
#                       )
#            )
#            if errorIndication:
#                print(errorIndication)
#            elif errorStatus:
#                print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#            else:
#                for varBind in varBinds:
#                    result = (' = '.join([x.prettyPrint() for x in varBind]))
#                interfaces.update({'OS': result})
#        else:
#            print('Unknown command')
#        return interfaces
