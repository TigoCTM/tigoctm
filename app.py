from flask import Flask, redirect, request, url_for, render_template
import ConfigParser
import os
# from os import path
# from pathlib import Path
import subprocess
import re
import random
from decimal import Decimal

configParser = ConfigParser.RawConfigParser()
configFilePath = './config.ini'
configParser.read(configFilePath)
app = Flask(__name__)

if 'TIGO_HOME' in os.environ:
    TIGO_HOME = os.environ['TIGO_HOME']
else:
    TIGO_HOME = "/home/tigoctm/"

def tigoRender(path, kwargs=None):
    if kwargs is None:
        kwargs = {}
    kwargs['prices'] = {'BTC': 0, 'DASH': 0}
    search = "P"
    try:
        grep = subprocess.check_output([
            'grep',
            '-r',
            search, '%sledger/prices/*.db' % TIGO_HOME
        ])
        if (grep and len(grep) > 1):
            xgc = Decimal(re.search('XCM[ ]*\$[ 0-9.]*', grep).group(0).replace('XCM', '').replace('$', '').replace(' ', ''))
            kwargs['prices'] = {
                'USD': xgc,
                'BTC': Decimal(re.search('\$ .[ 0-9.]*BTC', grep).group(0).replace('BTC', '').replace('$', '').replace(' ', '')) * xgc,
                'DASH': Decimal(re.search('\$ .[ 0-9.]*DASH', grep).group(0).replace('DASH', '').replace('$', '').replace(' ', '')) * xgc,
                'guld': Decimal(re.search('\$ .[ 0-9.]*guld', grep).group(0).replace('guld', '').replace('$', '').replace(' ', '')) * xgc
            }
            kwargs['prices']['BTC'] = kwargs['prices']['BTC'].quantize(Decimal(0.001))
            kwargs['prices']['DASH'] = kwargs['prices']['DASH'].quantize(Decimal(0.001))
            kwargs['prices']['guld'] = kwargs['prices']['guld'].quantize(Decimal(0.001))
    except Exception as e:
        print(e)
    return render_template(path, **kwargs)

@app.route('/')
def index():
    return tigoRender('index.html')

@app.route('/id/')
def identify():
    return tigoRender('identify.html')

def getAssets(commodity, address):
    ledgerBals = subprocess.check_output([
        '/usr/bin/ledger',
        '-f',
        '%sledger/%s/%s/included.dat' % (TIGO_HOME, commodity, address), 'bal'
    ])
    if (ledgerBals):
        ledgerBals = ledgerBals.split('\n')
    for line in ledgerBals:
        if re.search(' (Assets|Payable):{0,1}\w*$', line):
            return line.replace('Assets', '').replace(commodity, '').replace(' ', '').replace('Payable', '')
    return 0

def getGuldAssets(username):
    ledgerBals = subprocess.check_output([
        '/usr/bin/ledger',
        '-f',
        '%sledger/guld/%s/included.dat' % (TIGO_HOME, username),
        'bal'
    ])
    if (ledgerBals):
        ledgerBals = ledgerBals.split('\n')
    user = ''
    tigos = 0
    users = 0
    for line in ledgerBals:
        if 'tigoctm' in line:
            user = 'tigoctm'
        elif username in line:
            user = username
        if re.search(' (Assets|Payable):{0,1}\w*$', line):
            amount = Decimal(line.replace('Assets', '').replace('guld', '').replace(' ', '').replace('Payable', ''))
            if user == 'tigoctm':
                tigos = amount
            elif user == username:
                users = amount
    return tigos, users

def getAddresses(username, side='deposit'):
    if side == 'deposit':
        search = ';tigoctm:%s' % username
    else:
        search = ';%s:tigoctm' % username
    grep = "";
    try:
        grep = subprocess.check_output([
            'grep',
            '-r',
            search, '%sledger/' % TIGO_HOME
        ])
    except subprocess.CalledProcessError as cpe:
        print(cpe)
    if (grep):
        grep = grep.split('\n')
    addys = {}
    for line in grep:
        if len(line) == 0:
            break
        line = line.replace('%sledger/' % TIGO_HOME, '').split('/')
        assets = Decimal(getAssets(line[0], line[1]))
        if (line[0] in addys):
            addys[line[0]][line[1]] = assets
            addys[line[0]]['sub-total'] = addys[line[0]]['sub-total'] + assets
        else:
            addys[line[0]] = {line[1]: assets, 'sub-total': assets}
    if os.path.exists('%sledger/guld/%s' % (TIGO_HOME, username)):
        gassets = getGuldAssets(username)
        if side == 'deposit':
            addys['guld'] = { username: gassets[0] }
        else:
            addys['guld'] = { username: gassets[1] }

    return addys

def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == os.errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

@app.route('/id/<username>')
def identity(username=None):
    if (username):
        depAddys = getAddresses(username)
        withAddys = getAddresses(username, 'withdraw')
        return tigoRender('identity.html', {'username':username, 'depositAddresses':depAddys, 'withdrawAddresses':withAddys})
    return tigoRender('identify.html')

@app.route('/id/<username>/<faddress>')
def register(username, faddress):
    mkdirp('%speople/%s/' % (TIGO_HOME, username))
    print(username)
    print(faddress)
    if re.match('-----BEGIN PGP PUBLIC KEY BLOCK-----[a-zA-Z1-9 :]*-----END PGP PUBLIC KEY BLOCK-----', faddress):
        imp = subprocess.Popen([
            'gpg2',
            '--import',
        ], stdin=subprocess.PIPE)
        if (imp == 0):
            imp = subprocess.check_output([
                'gpg2',
                '--fingerprint',
                '--with-colons'
            ])
            for line in imp.split('\n'):
                if line.startsWith('fpr'):
                    mkdirp('%skeys/pgp/%s/' % (TIGO_HOME, username))
                    imp = subprocess.Popen([
                        'gpg2',
                        '--export',
                        '-a',
                        '>',
                        '%skeys/pgp/%s/%s.asc' % (TIGO_HOME, username, re.search('\w{4,41}', line).group(0))
                    ])
    elif re.match('0x\w{10,40}', faddress):
        if not os.path.exists('%sledger/XCM/%s/included.dat' % (TIGO_HOME, faddress)):
            mkdirp('%sledger/XCM/%s/' % (TIGO_HOME, faddress))
            ledger = open('%sledger/XCM/%s/included.dat' % (TIGO_HOME, faddress), 'w')
            ledger.write(";%s:tigoctm" % username)
            ledger.close()
    return redirect(url_for('identity', username=username))

@app.route('/address/generate/<commodity>/<username>')
def genaddress(commodity, username):
    addys = getAddresses(username)
    if commodity not in addys or len(addys[commodity]) < 3:
        imp = subprocess.check_output([
            'find',
            '%sledger/%s/' % (TIGO_HOME, commodity),
            '-size',
            '0',
            '-name',
            'included.dat'
        ]).split('included.dat')
        chosen = random.randint(0, len(imp) - 1)
        imp[chosen] = imp[chosen].replace('%sledger/%s' % (TIGO_HOME, commodity), '')
        found = re.search('[^/]\w*[^/]', imp[chosen]).group(0)
        f = open('%sledger/%s/%s/included.dat' % (TIGO_HOME, commodity, found), 'w')
        f.write(';tigoctm:%s' % username)
        f.close()
    return redirect(url_for('identity', username=username))

@app.route('/price/<commodity>')
def price(commodity):
    return tigoRender('price.html')

@app.route('/address/<address>')
def address(address):
    return tigoRender('address.html', {'address': address})

if __name__ == '__main__':
    app.run()
